"""LoRA / QLoRA fine-tuning of an open VLM for SatClip's language layer.

One script, any mix of the chat JSONL files made by the builders in this folder:
  training/data/intents/train.jsonl        question -> intent JSON (text only)      build_intent_data.py
  training/data/rsvqa_lr/train.jsonl       optical VQA, counts mapped to a refusal   build_rsvqa.py
  training/data/bigearthnet/train.jsonl    optical and radar land-cover Q&A          build_bigearthnet.py
  training/data/india_qa/train.jsonl       Indian OSM land-use Q&A (planned)         build_india_qa.py

Defaults target Qwen2-VL-2B-Instruct (archive A149) with LoRA r=16 on the language model's attention
and MLP projections (A059); `--qlora` loads the base in 4-bit NF4 (A060) so it fits a free Colab T4;
`--dora` switches to weight-decomposed LoRA (A148). The vision tower stays frozen: SatClip never asks
the model for pixels or numbers, only for language, so adapting the LLM side is enough and cheaper.
Loss is computed on the assistant reply only.

    python training/lora/train_lora.py --data training/data/intents/train.jsonl --out training/runs/intent-lora
    python training/lora/train_lora.py --data training/data/intents/train.jsonl training/data/rsvqa_lr/train.jsonl \
        --qlora --epochs 1 --out training/runs/satclip-lora

After training: `python training/eval/eval_intents.py --predictor hf --adapter training/runs/intent-lora`
and `python training/eval/eval_vqa.py --adapter ...`. Merge for CPU serving with --merge (then quantise,
for example to GGUF or AWQ, archive A061, A146).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def load_rows(paths: list[Path], max_per_file: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    rows = []
    for p in paths:
        rs = [json.loads(line) for line in open(p, encoding="utf-8")]
        rng.shuffle(rs)
        rows += rs[: max_per_file or None]
        print(f"{p}: {min(len(rs), max_per_file or len(rs))} rows")
    rng.shuffle(rows)
    return rows


def to_chat(row: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalise message content to the list-of-parts form that VLM chat templates expect."""
    msgs = []
    for m in row["messages"]:
        c = m["content"]
        msgs.append({"role": m["role"], "content": c if isinstance(c, list) else [{"type": "text", "text": c}]})
    return msgs


class Collator:
    """Tokenise prompt + reply with the processor's chat template; mask everything but the reply."""

    def __init__(self, processor, max_len: int, image_size: int):
        self.p, self.max_len, self.image_size = processor, max_len, image_size

    def _images(self, row):
        from PIL import Image
        out = []
        for path in row.get("images", []):
            im = Image.open(ROOT / path).convert("RGB")
            out.append(im.resize((self.image_size, self.image_size)) if self.image_size else im)
        return out or None

    def __call__(self, batch: list[dict[str, Any]]) -> dict[str, Any]:
        import torch
        seqs: list[dict[str, Any]] = []
        pix, grids = [], []
        for row in batch:
            msgs = to_chat(row)
            images = self._images(row)
            full = self.p.apply_chat_template(msgs, tokenize=False)
            prompt = self.p.apply_chat_template(msgs[:-1], tokenize=False, add_generation_prompt=True)
            enc_full = self.p(text=[full], images=images, return_tensors="pt")
            n_prompt = self.p(text=[prompt], images=images, return_tensors="pt")["input_ids"].shape[1]
            L = enc_full["input_ids"].shape[1]
            keep = L if images else min(L, self.max_len)  # never cut through image tokens
            # every per-token tensor the processor returns (input_ids, attention_mask, mm_token_type_ids, ...)
            per_tok = {k: v[0][:keep] for k, v in enc_full.items()
                       if hasattr(v, "shape") and v.dim() == 2 and v.shape == (1, L)}
            y = per_tok["input_ids"].clone()
            y[:n_prompt] = -100
            per_tok["labels"] = y
            seqs.append(per_tok)
            if "pixel_values" in enc_full:
                pix.append(enc_full["pixel_values"])
                if "image_grid_thw" in enc_full:
                    grids.append(enc_full["image_grid_thw"])
        pad = getattr(self.p.tokenizer, "pad_token_id", None) or 0
        n = max(len(s["input_ids"]) for s in seqs)
        out: dict[str, Any] = {}
        for k in seqs[0]:
            fill = -100 if k == "labels" else pad if k == "input_ids" else 0
            t = torch.full((len(seqs), n), fill, dtype=seqs[0][k].dtype)
            for i, s_ in enumerate(seqs):
                t[i, : len(s_[k])] = s_[k]
            out[k] = t
        if pix:
            out["pixel_values"] = torch.cat(pix)
            if grids:
                out["image_grid_thw"] = torch.cat(grids)
        return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, nargs="+", required=True)
    ap.add_argument("--model", default="Qwen/Qwen2-VL-2B-Instruct")
    ap.add_argument("--out", type=Path, default=ROOT / "training/runs/satclip-lora")
    ap.add_argument("--max-per-file", type=int, default=0)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--max-len", type=int, default=1024)
    ap.add_argument("--image-size", type=int, default=448, help="resize images to N x N (0 keeps native size)")
    ap.add_argument("--qlora", action="store_true")
    ap.add_argument("--dora", action="store_true")
    ap.add_argument("--merge", action="store_true", help="also save a merged full model for CPU serving")
    ap.add_argument("--max-steps", type=int, default=-1, help="for smoke tests")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    import torch
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoProcessor, Trainer, TrainingArguments
    try:
        from transformers import AutoModelForImageTextToText as AutoVLM
    except ImportError:  # older transformers
        from transformers import AutoModelForVision2Seq as AutoVLM

    processor = AutoProcessor.from_pretrained(args.model)
    if getattr(processor, "tokenizer", None) is None:  # text-only checkpoints
        processor.tokenizer = processor
    import inspect

    import transformers
    dtype_key = "dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"
    kw: dict[str, Any] = {dtype_key: torch.bfloat16 if torch.cuda.is_available() else torch.float32}
    if args.qlora:
        from transformers import BitsAndBytesConfig
        kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                       bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
        kw["device_map"] = "auto"
    model = AutoVLM.from_pretrained(args.model, **kw)
    if args.qlora:
        model = prepare_model_for_kbit_training(model)
    names = {n.split(".")[-1] for n, _ in model.named_modules()}
    targets = [t for t in TARGETS if t in names]
    # Only adapt the language model: skip modules under the vision tower ("visual", "vision_model").
    target_regex = r"^(?!.*(visual|vision_model|vision_tower)).*\.(" + "|".join(targets) + r")$"
    cfg = LoraConfig(r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05, target_modules=target_regex,
                     use_dora=args.dora, task_type="CAUSAL_LM")
    model = get_peft_model(model, cfg)
    model.print_trainable_parameters()

    rows = load_rows(args.data, args.max_per_file, args.seed)
    steps = args.max_steps if args.max_steps > 0 else int(len(rows) / (args.batch * args.grad_accum) * args.epochs) + 1
    warm = {"warmup_ratio": 0.03} if "warmup_ratio" in inspect.signature(TrainingArguments).parameters \
        else {"warmup_steps": max(1, int(0.03 * steps))}
    targs = TrainingArguments(
        output_dir=str(args.out), num_train_epochs=args.epochs, max_steps=args.max_steps, learning_rate=args.lr,
        per_device_train_batch_size=args.batch, gradient_accumulation_steps=args.grad_accum, **warm,
        lr_scheduler_type="cosine", logging_steps=10, save_strategy="epoch", save_total_limit=1,
        bf16=torch.cuda.is_available(), gradient_checkpointing=torch.cuda.is_available(), remove_unused_columns=False,
        report_to=[], seed=args.seed, dataloader_num_workers=2 if torch.cuda.is_available() else 0)
    trainer = Trainer(model=model, args=targs, train_dataset=rows,
                      data_collator=Collator(processor, args.max_len, args.image_size))
    trainer.train()
    model.save_pretrained(args.out)
    processor.save_pretrained(args.out)
    (args.out / "satclip_training.json").write_text(json.dumps(
        {"base": args.model, "data": [str(p) for p in args.data], "rows": len(rows), "rank": args.rank,
         "alpha": args.alpha, "qlora": args.qlora, "dora": args.dora, "epochs": args.epochs, "lr": args.lr}, indent=1))
    if args.merge and not args.qlora:
        merged = model.merge_and_unload()
        merged.save_pretrained(args.out / "merged")
        processor.save_pretrained(args.out / "merged")
    print("saved adapter to", args.out)


if __name__ == "__main__":
    sys.exit(main())
