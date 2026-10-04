# SatClip research archive

A verified, annotated archive of research that shapes SatClip. One file per paper in [`papers/`](papers/), each saying what the paper is and what it means for this project (what to adopt, avoid or beat). The machine-readable index is [`index.csv`](index.csv).

## Rules

- Every paper is real. Title, authors, year and link are checked against the source page before an entry is written; the `verified` field records the date and URL. Details that could not be confirmed are flagged inside the entry.
- File name: `NNN-short-slug.md`, with `NNN` a zero-padded running number.
- Front matter: `id, title, authors, year, venue, link, code, category, era, tags, verified, takeaway`.
- Sections: Problem, Approach, Data and benchmarks, Key results, Limitations, What it means for SatClip.
- Own words only, no long quotes, no PDFs committed (links only).
- `era`: historical (before 2020), recent (2020 to 2026, published), upcoming (2026 preprints, challenges, announced datasets).
- After adding papers, run `python tools/build_index.py` to regenerate `index.csv` and the catalog below. It fails on duplicate IDs or titles.

## Categories

| Key | Scope |
|---|---|
| rs-vlm | Remote sensing vision-language models and assistants |
| rs-benchmark | RS VQA, captioning, grounding datasets and benchmarks |
| eo-foundation | Scene classification and EO foundation models (CLIP-style, MAE, multimodal) |
| change-detection | Optical and SAR change detection |
| sar-optical-fusion | SAR-optical fusion, SAR analytics, cloud removal |
| object-detection | Object detection in remote sensing |
| trust-calibration | Hallucination, calibration, uncertainty, selective prediction and abstention |
| eo-agents | Retrieval-augmented and tool-using agents for EO |
| data-infrastructure | STAC, COG, Copernicus, tiling, job queues |
| efficient-inference | LoRA, quantization, edge and offline inference |
| indian-context | ISRO, Bhuvan, monsoon, Indian disaster management and agriculture |
| human-factors | UX of GIS, conversational analytics, decision support |
| historical | Foundations before 2020 |
| upcoming | 2026 preprints, challenges, announced datasets |

## Catalog

<!-- CATALOG:START -->

Total papers: **25**

| Category | Count |
|---|---|
| eo-agents | 2 |
| eo-foundation | 2 |
| historical | 1 |
| rs-benchmark | 7 |
| rs-vlm | 9 |
| sar-optical-fusion | 4 |

### eo-agents

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 023 | [Remote Sensing ChatGPT: Solving Remote Sensing Tasks with ChatGPT and Visual Models](papers/023-remote-sensing-chatgpt.md) ([source](https://arxiv.org/abs/2401.09083)) | 2024 | recent | Simple LLM plan-and-call-tools loop with no quantitative evaluation; copy the loop with an open CPU LLM and add confidence propagation and abstention |
| 024 | [GeoLLM-Engine: A Realistic Environment for Building Geospatial Copilots](papers/024-geollm-engine.md) ([source](https://arxiv.org/abs/2404.15500)) | 2024 | recent | GPT-4 agent success fell as tool chains grew longer; keep SatClip plans short and fixed and track tool-call correctness |

### eo-foundation

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 008 | [RemoteCLIP: A Vision Language Foundation Model for Remote Sensing](papers/008-remoteclip.md) ([source](https://arxiv.org/abs/2306.11029)) | 2024 | recent | Default CPU zero-shot and retrieval backbone; validate on Indian Sentinel-2 and calibrate its similarity scores before abstention |
| 009 | [RS5M and GeoRSCLIP: A Large Scale Vision-Language Dataset and A Large Vision-Language Model for Remote Sensing](papers/009-rs5m-georsclip.md) ([source](https://arxiv.org/abs/2306.11300)) | 2024 | recent | Bake off GeoRSCLIP against RemoteCLIP; its PEFT results back the LoRA plan, but keep eval captions human-written |

### historical

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 016 | [Exploring Models and Data for Remote Sensing Image Caption Generation](papers/016-rsicd-captioning.md) ([source](https://arxiv.org/abs/1712.07835)) | 2018 | historical | Use its caption annotation rules as SatClip's caption style guide; do not trust BLEU or CIDEr without a grounding check |

### rs-benchmark

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 010 | [SkyScript: A Large and Semantically Diverse Vision-Language Dataset for Remote Sensing](papers/010-skyscript.md) ([source](https://arxiv.org/abs/2312.12856)) | 2024 | recent | Reuse the OSM-to-caption trick for Indian training pairs, watching for sparse rural OSM coverage; add SkyCLIP to the backbone bake-off |
| 011 | [RSVQA: Visual Question Answering for Remote Sensing Data](papers/011-rsvqa.md) ([source](https://arxiv.org/abs/2003.07333)) | 2020 | recent | Sentinel-2 VQA baseline to evaluate on first; copy OSM-template QA generation and always run a blind (no-image) baseline to expose language bias |
| 012 | [VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding](papers/012-vrsbench.md) ([source](https://arxiv.org/abs/2406.12384)) | 2024 | recent | Reference LoRA recipe and human-verified QA design, but VHR optical only and grounding about 57% at IoU 0.5, so masks need a dedicated segmenter |
| 013 | [Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data](papers/013-vleo-bench.md) ([source](https://arxiv.org/abs/2401.17600)) | 2024 | recent | Let the VLM caption and explain but route counts, boxes and damage to dedicated instruments; GPT-4V got about 0.16 mIoU on localization |
| 014 | [GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks](papers/014-geobench-vlm.md) ([source](https://arxiv.org/abs/2411.19325)) | 2024 | recent | Best open VLM reaches only about 42% MCQ accuracy on geospatial tasks, which justifies tool grounding plus abstention; reuse its task taxonomy |
| 015 | [FloodNet: A High Resolution Aerial Imagery Dataset for Post Flood Scene Understanding](papers/015-floodnet.md) ([source](https://arxiv.org/abs/2012.02951)) | 2021 | recent | Borrow the flood question taxonomy rescaled to 10 m Sentinel, and guard against flood versus permanent water confusion with a reference layer |
| 017 | [BigEarthNet-MM: A Large Scale Multi-Modal Multi-Label Benchmark Archive for Remote Sensing Image Classification and Retrieval](papers/017-bigearthnet-mm.md) ([source](https://arxiv.org/abs/2105.07921)) | 2021 | recent | Use BigEarthNet-pretrained S1/S2 encoders next to RemoteCLIP, expose only labels separable at 10 m, and measure the Europe-to-India domain gap |

### rs-vlm

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 001 | [GeoChat: Grounded Large Vision-Language Model for Remote Sensing](papers/001-geochat.md) ([source](https://arxiv.org/abs/2311.15826)) | 2024 | recent | Baseline RS chat model (RGB only, 7B); reuse its task-token routing and dataset-to-instruction recipe, but do not trust VLM-emitted boxes (about 10.6% referring detection acc@0.5) |
| 002 | [EarthGPT: A Universal Multi-modal Large Language Model for Multi-sensor Image Comprehension in Remote Sensing Domain](papers/002-earthgpt.md) ([source](https://arxiv.org/abs/2401.16822)) | 2024 | recent | MMRS-1M (optical, SAR, infrared) is a ready seed for LoRA data; its pixel-level weakness supports keeping masks in a separate, non-LLM head |
| 003 | [EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues](papers/003-earthdial.md) ([source](https://arxiv.org/abs/2412.15190)) | 2025 | recent | Closest prior work (4B, open weights, Sentinel-1 VH plus S2 plus change); top LoRA base candidate, and SatClip must beat it on provenance, calibration and abstention |
| 004 | [SkyEyeGPT: Unifying Remote Sensing Vision-Language Tasks via Instruction Tuning with Large Language Model](papers/004-skyeyegpt.md) ([source](https://arxiv.org/abs/2401.09712)) | 2025 | recent | Lean frozen-encoder plus linear-projector design suits a CPU-first prototype; expect degradation from aerial to 10 m Sentinel resolution |
| 005 | [LHRS-Bot: Empowering Remote Sensing with VGI-Enhanced Large Multimodal Language Model](papers/005-lhrs-bot.md) ([source](https://arxiv.org/abs/2402.02544)) | 2024 | recent | Copy the OpenStreetMap/VGI auto-captioning trick for cheap Indian training pairs and multiple-choice evals; check rural OSM sparsity |
| 006 | [RSGPT: A Remote Sensing Vision Language Model and Benchmark](papers/006-rsgpt.md) ([source](https://arxiv.org/abs/2307.15266)) | 2025 | recent | Copy RSICap's rich human-caption style and build a small Indian RSIEval-like test set; beat it on grounding and confidence |
| 007 | [TEOChat: A Large Vision-Language Assistant for Temporal Earth Observation Data](papers/007-teochat.md) ([source](https://arxiv.org/abs/2410.06234)) | 2025 | recent | Use its temporal task taxonomy for before/after queries; too heavy for CPU and has no SAR or calibration, which SatClip adds |
| 021 | [SARChat-Bench-2M: A Multi-Task Vision-Language Benchmark for SAR Image Interpretation](papers/021-sarchat.md) ([source](https://arxiv.org/abs/2502.08168)) | 2025 | recent | About 2M SAR image-text pairs and released checkpoints give a SAR baseline, but imagery is mostly high-res targets, so test on Indian Sentinel-1 |
| 025 | [RS-LLaVA: A Large Vision-Language Model for Joint Captioning and Question Answering in Remote Sensing Imagery](papers/025-rs-llava.md) ([source](https://www.mdpi.com/2072-4292/16/9/1477)) | 2024 | recent | LoRA recipe and released 7B checkpoint are a fine-tune starting point; its ungrounded, confidence-free output is the gap SatClip fills |

### sar-optical-fusion

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 018 | [SEN12MS: A Curated Dataset of Georeferenced Multi-Spectral Sentinel-1/2 Imagery for Deep Learning and Data Fusion](papers/018-sen12ms.md) ([source](https://arxiv.org/abs/1906.07789)) | 2019 | historical | Paired global S1/S2 data plus a recipe for building an Indian SAR-optical set; its coarse MODIS labels suit weak supervision only |
| 019 | [Multisensor Data Fusion for Cloud Removal in Global and All-Season Sentinel-2 Imagery](papers/019-sen12ms-cr.md) ([source](https://arxiv.org/abs/2009.07683)) | 2021 | recent | SEN12MS-CR is the monsoon cloud-gap test set; use cloud masks to choose between optical, SAR and abstaining, never present filled pixels as observed |
| 020 | [Cloud removal in Sentinel-2 imagery using a deep residual neural network and SAR-optical data fusion](papers/020-dsen2-cr.md) ([source](https://doi.org/10.1016/j.isprsjprs.2020.05.013)) | 2020 | recent | Baseline for SAR-guided cloud filling; flag reconstructed areas and skip indices there; too heavy for per-query CPU use |
| 022 | [Sen1Floods11: A Georeferenced Dataset to Train and Test Deep Learning Flood Algorithms for Sentinel-1](papers/022-sen1floods11.md) ([source](https://openaccess.thecvf.com/content_CVPRW_2020/html/w11/Bonafilia_Sen1Floods11_A_Georeferenced_Dataset_to_Train_and_Test_Deep_Learning_CVPRW_2020_paper.html)) | 2020 | recent | Standard Sentinel-1 flood baseline (11 events, none in India); keep an Otsu VH threshold as a sanity check and build an Indian held-out test |

<!-- CATALOG:END -->
