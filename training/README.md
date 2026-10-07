# SatClip training, evaluation and calibration (M5)

SatClip has two learned parts, and they are trained very differently because they carry different risks.

| Part | What it does | Can it produce a number on the card? | How it is trained | Where |
|---|---|---|---|---|
| Confidence calibration | Maps an instrument's raw quality score to the probability that its area answer is within 20% of a reference map | No, it only decides how sure the card is and whether it abstains | Fitted on labelled maps: Sen1Floods11 for water extent, Kuro Siwo for water change; crop change not yet (no open labels) | `calibration/` |
| Language layer (LoRA on an open VLM) | Turns English, Hinglish or Hindi questions with any date style into the intent JSON; explains the card; answers simple follow-ups about the shown image; refuses counts | No, by design: its JSON goes through the same gazetteer and date rules as the rule parser | LoRA or QLoRA on Qwen2-VL-2B-Instruct, on a GPU (Colab) | `lora/`, `colab/` |

## 1. Calibration (runs on CPU; water extent fitted in run 6 and refitted for v1.1 in run 7, water change fitted in run 7)

```bash
pip install -e "backend[geo]" matplotlib
python training/calibration/cache_sen1floods11.py     # once: 446 hand-labelled chips, VV + VH + label at 20 m, about 90 MB
python training/calibration/tune_water_vh.py          # chooses the VH bounds on the train split (report: sar_water_vh_tuning.md)
python training/calibration/fit_water.py --from-cache # refits sar_water_otsu (v1.1); --pols vv reproduces v1.0
python training/calibration/fit_change.py             # streams about 1.5 GB of Kuro Siwo, fits sar_logratio_change
```

Each script runs the production instrument code (`classify_sar_water`, `classify_sar_change`) on labelled chips, marks a chip correct when its area is within 20% of the label (the event the card confidence claims to predict), chooses an isotonic or Platt map without touching the evaluation data, and writes `config/calibration/<instrument>.json` with a fit ledger. Reports: [sar_water_otsu.md](calibration/reports/sar_water_otsu.md), [sar_logratio_change.md](calibration/reports/sar_logratio_change.md), [sar_water_vh_tuning.md](calibration/reports/sar_water_vh_tuning.md); the v1.0 water report is kept as [sar_water_otsu_v1.0.md](calibration/reports/sar_water_otsu_v1.0.md).

**Water extent, v1.0 (run 6, VV only):** the uncalibrated score was overconfident; after the fit the card published only 11% of held-out chips (33% error) and the instrument missed most Indian flood water (median IoU 0.03), because Indian hand labels include flooded vegetation and rough water that stay bright in VV.

**Water extent, v1.1 (run 7, VV or VH):** a pixel is water if VV is below its fitted threshold or VH is below its own fitted threshold (VH fit rejected above -18 dB gamma0, default -22 dB; bounds chosen on the train split only). On the untouched test split:

| Evaluation set | Share correct v1.0 -> v1.1 | ECE after | Coverage at 0.60 | Error when published | Median IoU |
|---|---|---|---|---|---|
| Held-out test split (82 chips) | 0.44 -> 0.55 | 0.088 -> 0.074 | 0.11 -> 0.43 | 0.33 -> 0.26 | 0.15 -> 0.31 |
| Bolivia, country never seen (14) | 0.29 -> 0.57 | 0.217 -> 0.323 | 0.00 -> 0.43 | none -> 0.00 | 0.18 -> 0.48 |
| India, fit made without India (64) | 0.23 -> 0.36 | 0.357 -> 0.227 | 0.12 -> 0.52 | 0.63 -> 0.55 | 0.03 -> 0.09 |

VH roughly quadruples how often the card can answer at the same or lower error, but India stays the weak spot: with a fit that never saw India, more than half of the published Indian chip answers are still wrong. The shipped map is fitted on train plus valid, which includes 50 Indian chips; on the 14 Indian test chips summed as one district card it publishes at 0.64 and is within 20%. Live, Barpeta on 11 July 2024 now publishes 905 sq km at 0.62 (it abstained at 0.46 under v1.0).

**Water change (run 7, Kuro Siwo, archive A041):** 848 samples from 22 flood events, 5-fold cross-validated with folds grouped by event (the webdataset's train and test parts share events). The raw score barely separates right from wrong (AUROC 0.52), because two kinds of answer are mixed: "no meaningful new water" answers are right 68% of the time, "X sq km of new water" answers only 27% (75% of flood chips are undercounted by more than 20%). One map per answer regime cuts ECE from 0.214 (borrowed water map) to 0.041. The calibration file now has `"method": "regimes"`; the change card abstains on positive change answers until the instrument improves (live Barpeta flood change: 466 sq km at 0.23, abstained).

**Crop change (`ndvi_difference`): not fitted, by decision.** Calibration needs a reference map of crop decline per pixel or field between two dates. No open labelled set exists for Indian districts (YES-TECH and FASAL outputs are not public at pixel level; global crop-type maps do not label decline). Its placeholder stays, and every crop card says "placeholder (not yet fitted)". Candidate later: a Sentinel-2 NDVI decline reference built from harvest calendars plus field photos, or a partner dataset from a state agriculture department.

## 2. Language layer data

| Builder | Output | Size | Notes |
|---|---|---|---|
| `lora/build_intent_data.py` | `data/intents/{train,val,test}.jsonl` | 12,000 / 1,500 / 1,500 | 735 districts split 80/10/10 by hash, so test districts are unseen; English, Hinglish, Hindi; DD/MM/YYYY and other Indian date styles; typos; missing details; refusals (counting, forecast, identity, other) |
| `lora/build_rsvqa.py --download` | `data/rsvqa_lr/{split}.jsonl` and PNGs | RSVQA-LR, 772 Sentinel-2 tiles | count questions become a refusal in training, kept as labels for evaluation |
| `lora/build_bigearthnet.py` | `data/bigearthnet/{split}.jsonl` | any subset of BigEarthNet v2 | optical true colour and radar false colour (R = VV, G = VH, B = VV - VH, fixed stretch, `lora/images.py`); questions generated from the 19-class labels |
| `lora/build_india_qa.py` | `data/india_qa/{train,val,test}.jsonl` and PNGs | about 10 pairs per chip (optical plus radar); an 8-district, 16-chip smoke run gave 154 pairs | Indian chips (2.56 km, 10 m) inside district outlines, Sentinel-2 true colour from the 2021 dry season plus optional Sentinel-1 false colour, labels from ESA WorldCover 2021 (CC BY 4.0); only clear-cut answers are written; unseen-district split; optional positive-only OSM named-water questions. OSM land use was tested first and rejected as a label source: a 35 x 33 km box in rural Barpeta has 85 landuse or natural features, 5 of them farmland. Bhuvan layers not used (redistribution terms unclear) |

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

Baselines (reports in [eval/reports/](eval/reports/)):

| Test | Baseline | Result |
|---|---|---|
| Intent parsing, 1,500 generated questions, unseen districts | rule parser of run 6 (ISO dates, English keywords) | full match 0.163; intent 0.569; district 0.925; dates 0.197; refusal precision 0.257 |
| same | rule parser of run 7 (Indian date formats, common Hindi and Hinglish words, two dates make a water question a change question) | full match 0.898 (English 0.872, Hinglish 0.923, Hindi 0.941); intent 0.973; dates 1.000; refusal precision 0.821, recall 1.0 |
| Intent parsing, 44 hand-written questions (`eval/data/intents_handwritten.jsonl`, written in run 7 without the templates, never used for tuning) | rule parser of run 7 | full match 0.682 (English 0.750, Hinglish 0.583, Hindi 0.625); district 1.000; dates 0.864; refusal precision 0.409, recall 0.9 |
| RSVQA-LR test, 1,600 questions stratified by type | majority answer per type from the train split | overall 0.562; presence 0.754; comparison 0.700; rural or urban 0.560; count 0.234 |
| VRSBench VQA, 37,409 questions (converter verified on the real file in run 7) | most frequent answer per type, taken from the eval file itself (an optimistic floor) | 0.345 overall; 83% of yes/no answers are "yes", so existence accuracy must be read against a 0.82 always-yes floor ([report](eval/reports/vqa_vrsbench_prior.md)) |

**The generated intent test set is too easy.** Its questions come from the same templates as the training set (only the districts are unseen), so a rule parser with a few dozen keywords reaches 0.90. On 44 hand-written questions the same parser drops to 0.68, failing on paraphrases ("plant health", "green cover", "what you see", "kheti ka nuksaan") and over-refusing. The adapter should be judged on the hand-written set (and a larger one collected from real users), with the generated set as a sanity check only. Do not tune the rule parser on the hand-written set; it is a test set.

VQA yes or no answers also get a confidence from the first-token probabilities, so the same risk-coverage reporting used for the instruments applies to the language layer.
