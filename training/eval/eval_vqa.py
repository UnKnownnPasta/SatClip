"""Evaluate the language layer on remote sensing VQA, with selective-prediction metrics.

Sets (chat JSONL with "images" and meta.answer, as written by the builders):
  rsvqa_lr   training/data/rsvqa_lr/test.jsonl  (build_rsvqa.py --split test)
  vrsbench   training/data/vrsbench/test.jsonl  (convert_vrsbench below; VRSBench VQA, archive A012)

Predictors
  majority   the most frequent training answer per question type (needs build_rsvqa.py --download), the floor
  hf         a VLM plus optional LoRA adapter; greedy answer, and for yes/no questions a confidence
             max(P(yes), P(no)) from the first-token logits, so the harness can draw a risk-coverage
             curve and report accuracy at the 0.60 publication threshold (archive A027, A030, A112)

Scoring: normalised exact match (lower case, strip punctuation; numbers compared as integers). Count
questions are reported twice: accuracy against the label, and the share answered with a refusal, which is
what SatClip wants from the language layer.

    python training/eval/eval_vqa.py --set rsvqa_lr --predictor majority
    python training/eval/eval_vqa.py --set rsvqa_lr --predictor hf --model Qwen/Qwen2-VL-2B-Instruct --adapter training/runs/satclip-lora
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Optional

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "training" / "eval" / "reports"
REFUSAL = re.compile(r"cannot count|can't count|not able to count|unable to count", re.I)


def norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", "", s)
    words = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5"}
    return words.get(s, s)


def majority_predictor() -> Callable[[dict[str, Any]], tuple[str, Optional[float]]]:
    cache = ROOT / "training/.cache/rsvqa_lr"
    q = json.loads((cache / "LR_split_train_questions.json").read_text())["questions"]
    a = json.loads((cache / "LR_split_train_answers.json").read_text())["answers"]
    ans = {x["question_id"]: x["answer"] for x in a if x.get("active")}
    by: dict[str, Counter] = defaultdict(Counter)
    for x in q:
        if x.get("active") and x["id"] in ans:
            by[x["type"]][str(ans[x["id"]])] += 1
    best = {t: c.most_common(1)[0][0] for t, c in by.items()}
    return lambda row: (best.get(row["meta"].get("type", ""), "yes"), None)


def hf_predictor(model_id: str, adapter: Optional[str]) -> Callable[[dict[str, Any]], tuple[str, Optional[float]]]:
    import torch
    import transformers
    from PIL import Image
    from transformers import AutoProcessor
    try:
        from transformers import AutoModelForImageTextToText as AutoVLM
    except ImportError:
        from transformers import AutoModelForVision2Seq as AutoVLM
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): "auto"}
    proc = AutoProcessor.from_pretrained(adapter or model_id)
    model = AutoVLM.from_pretrained(model_id, **kw)
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter)
    if torch.cuda.is_available():
        model = model.to("cuda")
    model.eval()
    tok = proc.tokenizer
    yes_ids = [tok.encode(w, add_special_tokens=False)[0] for w in ("yes", "Yes")]
    no_ids = [tok.encode(w, add_special_tokens=False)[0] for w in ("no", "No")]

    def run(row: dict[str, Any]) -> tuple[str, Optional[float]]:
        msgs = []
        for m in row["messages"][:-1]:
            c = m["content"]
            msgs.append({"role": m["role"], "content": c if isinstance(c, list) else [{"type": "text", "text": c}]})
        prompt = proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        images = [Image.open(ROOT / p).convert("RGB") for p in row.get("images", [])] or None
        enc = proc(text=[prompt], images=images, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=24, do_sample=False, output_scores=True, return_dict_in_generate=True)
        text = proc.batch_decode(out.sequences[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
        p = torch.softmax(out.scores[0][0].float(), -1)
        py, pn = float(p[yes_ids].sum()), float(p[no_ids].sum())
        conf = max(py, pn) / (py + pn) if norm(row["meta"]["answer"]) in ("yes", "no") and (py + pn) > 0 else None
        return text, conf
    return run


def score(rows: list[dict[str, Any]], predict) -> dict[str, Any]:
    acc: dict[str, list[int]] = defaultdict(list)
    refusals: list[int] = []
    sel: list[tuple[float, int]] = []
    for row in rows:
        pred, conf = predict(row)
        gold = str(row["meta"]["answer"])
        t = row["meta"].get("type", "all")
        ok = int(norm(pred) == norm(gold))
        acc[t].append(ok)
        acc["all"].append(ok)
        if t == "count":
            refusals.append(int(bool(REFUSAL.search(pred))))
        if conf is not None:
            sel.append((conf, ok))
    res: dict[str, Any] = {t: {"n": len(v), "accuracy": round(sum(v) / len(v), 3)} for t, v in acc.items()}
    if refusals:
        res["count"]["refusal_rate"] = round(sum(refusals) / len(refusals), 3)
    if sel:
        sel.sort(key=lambda x: -x[0])
        risks, err = [], 0
        for i, (_, ok) in enumerate(sel, 1):
            err += 1 - ok
            risks.append(err / i)
        kept = [ok for c, ok in sel if c >= 0.60]
        res["yes_no_selective"] = {"n": len(sel), "aurc": round(sum(risks) / len(risks), 4),
                                   "coverage_at_0.60": round(len(kept) / len(sel), 3),
                                   "accuracy_at_0.60": round(sum(kept) / len(kept), 3) if kept else None}
    return res


def convert_vrsbench(src: Path, image_dir: Path) -> Path:
    """VRSBench VQA eval file (list of dicts with question, ground truth answer, image id; key names
    differ between releases, so several are accepted) -> chat JSONL in training/data/vrsbench/test.jsonl."""
    data = json.loads(src.read_text())
    out = ROOT / "training/data/vrsbench/test.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(out, "w") as f:
        for d in data:
            q = d.get("question") or d.get("Question")
            a = d.get("ground_truth") or d.get("answer") or d.get("gt")
            img = d.get("image_id") or d.get("image")
            if not (q and a and img):
                continue
            img_path = image_dir / (img if str(img).endswith((".png", ".jpg")) else f"{img}.png")
            f.write(json.dumps({"messages": [{"role": "system", "content": "Answer briefly."},
                                             {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": q}]},
                                             {"role": "assistant", "content": str(a)}],
                                "images": [str(img_path)], "meta": {"answer": str(a), "type": d.get("type", "vqa")}}) + "\n")
            n += 1
    print(f"{n} VRSBench questions -> {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="rsvqa_lr")
    ap.add_argument("--predictor", choices=["majority", "hf"], default="majority")
    ap.add_argument("--model", default="Qwen/Qwen2-VL-2B-Instruct")
    ap.add_argument("--adapter")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--name")
    ap.add_argument("--convert-vrsbench", nargs=2, type=Path, metavar=("EVAL_JSON", "IMAGE_DIR"))
    args = ap.parse_args()
    if args.convert_vrsbench:
        convert_vrsbench(*args.convert_vrsbench)
        return
    path = ROOT / "training/data" / args.set / "test.jsonl"
    rows = [json.loads(x) for x in open(path)]
    if args.limit:
        rows = rows[: args.limit]
    predict = majority_predictor() if args.predictor == "majority" else hf_predictor(args.model, args.adapter)
    res = score(rows, predict)
    name = args.name or f"{args.set}_{args.predictor}"
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"vqa_{name}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
