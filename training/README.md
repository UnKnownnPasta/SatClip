# SatClip training, evaluation and calibration (M5)

SatClip has two learned parts, and they are trained very differently because they carry different risks.

| Part | What it does | Can it produce a number on the card? | How it is trained | Where |
|---|---|---|---|---|
| Confidence calibration | Maps an instrument's raw quality score to the probability that its area answer is within 20% of a reference map | No, it only decides how sure the card is and whether it abstains | Fitted on labelled maps (Sen1Floods11 now; Kuro Siwo and Indian events next) | `calibration/` |
| Language layer (LoRA on an open VLM) | Turns English, Hinglish or Hindi questions with any date style into the intent JSON; explains the card; answers simple follow-ups about the shown image; refuses counts | No, by design: its JSON goes through the same gazetteer and date rules as the rule parser | LoRA or QLoRA on Qwen2-VL-2B-Instruct, on a GPU (Colab) | `lora/`, `colab/` |

## 1. Calibration (runs on CPU, done in run 6)

```bash
pip install -e "backend[geo]" matplotlib
python training/calibration/fit_water.py            # streams 446 Sen1Floods11 chips, about 5 minutes
python training/calibration/fit_water.py --rows training/calibration/reports/sar_water_otsu_chips.csv   # refit only
```

The script runs the production water code (`classify_sar_water`) on each hand-labelled chip, marks the chip correct when its water area is within 20% of the hand label, chooses an isotonic or Platt map on the valid split, refits on train plus valid, and writes `config/calibration/sar_water_otsu.json` with a fit ledger. The report with reliability and risk-coverage plots is in [calibration/reports/sar_water_otsu.md](calibration/reports/sar_water_otsu.md).

**What the first fit found (2026-10-07):** the uncalibrated score was overconfident. At the 0.60 publication line it would have published 79% of held-out chips with a 55% error rate. After the fit, expected calibration error on the held-out split fell from 0.30 to 0.09, and the card publishes 11% of chips with a 33% error rate, abstaining on the rest. On the 64 usable Indian chips (fit made without them) the instrument is much weaker (median IoU 0.03): Indian hand labels include flooded vegetation and rough water whose VV backscatter (median about -13 dB) sits above any VV water threshold, while VH still separates them. The next instrument version must use VH. Until then, SatClip abstains on most flood questions, which is the honest result.

`sar_logratio_change` borrows this map until it is fitted on its own before and after labels (`"method": "inherit"` in its calibration file; the card says "borrowed").

## 2. Language layer data

| Builder | Output | Size | Notes |
|---|---|---|---|
| `lora/build_intent_data.py` | `data/intents/{train,val,test}.jsonl` | 12,000 / 1,500 / 1,500 | 735 districts split 80/10/10 by hash, so test districts are unseen; English, Hinglish, Hindi; DD/MM/YYYY and other Indian date styles; typos; missing details; refusals (counting, forecast, identity, other) |
| `lora/build_rsvqa.py --download` | `data/rsvqa_lr/{split}.jsonl` and PNGs | RSVQA-LR, 772 Sentinel-2 tiles | count questions become a refusal in training, kept as labels for evaluation |
| `lora/build_bigearthnet.py` | `data/bigearthnet/{split}.jsonl` | any subset of BigEarthNet v2 | optical true colour and radar false colour (R = VV, G = VH, B = VV - VH, fixed stretch, `lora/images.py`); questions generated from the 19-class labels |
| `lora/build_india_qa.py` | `data/india_qa/` | planned (run 7) | Indian land-use Q&A from OSM layers over Sentinel-2 chips; Bhuvan WMS layers if licence allows |

The target JSON and its validator are in [lora/schema.py](lora/schema.py). `schema.JSON_SCHEMA` can drive constrained decoding (Outlines, archive A150), so the served model can only emit allowed values.

## 3. Training (GPU)

Open [colab/satclip_lora.ipynb](colab/satclip_lora.ipynb) in Colab with a T4 GPU, or run:

```bash
pip install -e "backend[geo]" "transformers>=4.49" peft accelerate bitsandbytes
python training/lora/train_lora.py --data training/data/intents/train.jsonl training/data/rsvqa_lr/train.jsonl \
    --qlora --epochs 1 --out training/runs/satclip-lora
```

Defaults: Qwen2-VL-2B-Instruct, LoRA rank 16, alpha 32, dropout 0.05 on the language model's attention and MLP projections (the vision tower stays frozen), loss on the assistant reply only, cosine schedule, learning rate 2e-4. `--dora` uses DoRA (A148), `--merge` saves a merged model for CPU serving and quantisation (A061, A146). The script was smoke-tested end to end on CPU with a tiny random Qwen2-VL (mixed text-only and image batches, 4 steps); it has not yet been run on a real GPU.

## 4. Evaluation

```bash
python training/eval/eval_intents.py --predictor rules                      # baseline, CPU, about 1 minute
python training/eval/eval_intents.py --predictor hf --adapter training/runs/satclip-lora
python training/eval/eval_vqa.py --set rsvqa_lr --predictor majority        # floor
python training/eval/eval_vqa.py --set rsvqa_lr --predictor hf --adapter training/runs/satclip-lora
python training/eval/eval_vqa.py --convert-vrsbench VRSBench_EVAL_vqa.json VRSBench_images/   # then --set vrsbench
```

Baselines measured in run 6 (reports in [eval/reports/](eval/reports/)):

| Test | Baseline | Result |
|---|---|---|
| Intent parsing, 1,500 questions, unseen districts | shipped rule parser | full match 0.163 (English 0.196, Hinglish 0.153, Hindi 0.077); intent 0.569; district 0.925; dates 0.197; refusal precision 0.257, recall 0.957 |
| RSVQA-LR test, 1,600 questions stratified by type | majority answer per type from the train split | overall 0.562; presence 0.754; comparison 0.700; rural or urban 0.560; count 0.234 |

The rule parser understands only ISO dates and English keywords, which is why it misses most Hinglish and Hindi questions and most date styles. An adapter is worth shipping only if it beats these numbers on unseen districts. A deterministic multi-format date parser would close part of the date gap without any model, and should be tried first (run 7).

VQA yes or no answers also get a confidence from the first-token probabilities, so the same risk-coverage reporting used for the instruments applies to the language layer.
