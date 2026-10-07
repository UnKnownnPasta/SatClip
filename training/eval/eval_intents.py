"""Evaluate a question parser on the held-out intent set (training/data/intents/test.jsonl).

Predictors
  rules   SatClip's shipped rule parser (backend/satclip/parser.py), the baseline any model must beat.
  hf      a Hugging Face causal LM or VLM, optionally with a LoRA adapter, decoding the JSON of schema.py
          and resolved through the same deterministic code (schema.resolve).

Metrics: JSON validity, intent accuracy, district accuracy (resolved gazetteer key), date accuracy, full
match (intent + district + dates all right, the event that matters for the user), refusal precision and
recall, and the breakdown by language style. Writes training/eval/reports/intents_<name>.json and .md.

    python training/eval/eval_intents.py --predictor rules
    python training/eval/eval_intents.py --predictor hf --model Qwen/Qwen2-VL-2B-Instruct --adapter runs/intent-lora
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from typing import Any, Callable, Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "training" / "lora"))

from schema import parse_output, resolve  # noqa: E402

REPORTS = ROOT / "training" / "eval" / "reports"


def gold_of(row: dict[str, Any]) -> dict[str, Any]:
    t = row["target"]
    region = row["meta"]["district"].lower() if t["place"] else None
    return {"intent": t["intent"], "region": region, "dates": t["dates"]}


def from_parsed(parsed) -> dict[str, Any]:
    dates = [(w.start + timedelta(days=(w.end - w.start).days // 2)).isoformat() for w in parsed.windows]
    return {"intent": parsed.intent.value, "region": parsed.region, "dates": dates,
            "ambiguous": bool(parsed.candidates)}


def rules_predictor() -> Callable[[str], Optional[dict[str, Any]]]:
    from satclip.models import QueryRequest
    from satclip.parser import parse
    return lambda text: from_parsed(parse(QueryRequest(text=text)))


def hf_predictor(model_id: str, adapter: Optional[str], max_new_tokens: int = 96) -> Callable[[str], Optional[dict[str, Any]]]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import transformers
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): "auto"}
    tok = AutoTokenizer.from_pretrained(model_id)
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, **kw)
    except ValueError:  # vision-language checkpoints (Qwen2-VL, SmolVLM) load through AutoModelForImageTextToText
        from transformers import AutoModelForImageTextToText
        model = AutoModelForImageTextToText.from_pretrained(model_id, **kw)
    if torch.cuda.is_available():
        model = model.to("cuda")
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter)
    model.eval()
    from schema import SYSTEM_PROMPT

    def run(text: str) -> Optional[dict[str, Any]]:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]
        enc = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt", return_dict=True)
        enc = {k: v.to(model.device) for k, v in enc.items()}
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
        reply = tok.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        obj = parse_output(reply)
        if obj is None:
            return None
        return from_parsed(resolve(obj, text))
    return run


def score(rows: list[dict[str, Any]], predict: Callable[[str], Optional[dict[str, Any]]]) -> dict[str, Any]:
    tot: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    refuse_tp = refuse_fp = refuse_fn = 0
    examples = []
    for row in rows:
        text = row["messages"][1]["content"]
        g, p = gold_of(row), predict(text)
        style = row["meta"]["style"]
        for bucket in ("all", style):
            t = tot[bucket]
            t["n"] += 1
            if p is None:
                continue
            t["valid"] += 1
            t["intent"] += p["intent"] == g["intent"]
            t["district"] += p["region"] == g["region"]
            t["dates"] += p["dates"] == g["dates"]
            full = p["intent"] == g["intent"] and p["region"] == g["region"] and (p["dates"] == g["dates"] or g["intent"] == "unsupported")
            t["full"] += full
        if p is not None:
            refuse_tp += p["intent"] == "unsupported" and g["intent"] == "unsupported"
            refuse_fp += p["intent"] == "unsupported" and g["intent"] != "unsupported"
            refuse_fn += p["intent"] != "unsupported" and g["intent"] == "unsupported"
            if not (p["intent"] == g["intent"] and p["region"] == g["region"]) and len(examples) < 12:
                examples.append({"text": text, "gold": g, "pred": p})
    out = {b: {k: (round(v / t["n"], 3) if k != "n" else int(v)) for k, v in t.items()} for b, t in tot.items()}
    out["refusal"] = {"precision": round(refuse_tp / max(refuse_tp + refuse_fp, 1), 3),
                      "recall": round(refuse_tp / max(refuse_tp + refuse_fn, 1), 3)}
    out["examples_of_errors"] = examples
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictor", choices=["rules", "hf"], default="rules")
    ap.add_argument("--model", default="Qwen/Qwen2-VL-2B-Instruct")
    ap.add_argument("--adapter")
    ap.add_argument("--data", type=Path, default=ROOT / "training/data/intents/test.jsonl")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--name")
    args = ap.parse_args()
    rows = [json.loads(line) for line in open(args.data, encoding="utf-8")]
    if args.limit:
        rows = rows[: args.limit]
    predict = rules_predictor() if args.predictor == "rules" else hf_predictor(args.model, args.adapter)
    res = score(rows, predict)
    name = args.name or args.predictor
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"intents_{name}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    lines = [f"# Intent parsing: {name}", "", f"Data: `{args.data.resolve().relative_to(ROOT)}` ({len(rows)} questions).", "",
             "| Slice | n | Valid JSON | Intent | District | Dates | Full match |", "|---|---|---|---|---|---|---|"]
    for b in ("all", "en", "hinglish", "hi"):
        if b in res:
            r = res[b]
            lines.append(f"| {b} | {r['n']} | {r.get('valid', 0):.3f} | {r.get('intent', 0):.3f} | {r.get('district', 0):.3f} | "
                         f"{r.get('dates', 0):.3f} | {r.get('full', 0):.3f} |")
    lines += ["", f"Refusal precision {res['refusal']['precision']}, recall {res['refusal']['recall']}.", ""]
    (REPORTS / f"intents_{name}.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
