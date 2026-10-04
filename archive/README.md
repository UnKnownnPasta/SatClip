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

Total papers: **75**

| Category | Count |
|---|---|
| change-detection | 8 |
| data-infrastructure | 4 |
| efficient-inference | 6 |
| eo-agents | 2 |
| eo-foundation | 10 |
| historical | 1 |
| human-factors | 6 |
| indian-context | 5 |
| object-detection | 5 |
| rs-benchmark | 7 |
| rs-vlm | 9 |
| sar-optical-fusion | 4 |
| trust-calibration | 8 |

### change-detection

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 034 | [A Theoretical Framework for Unsupervised Change Detection Based on Change Vector Analysis in the Polar Domain](papers/034-cva-polar.md) ([source](https://doi.org/10.1109/TGRS.2006.885408)) | 2007 | historical | Formal basis for optical change vector analysis: magnitude says whether something changed, direction says what kind; use it as the transparent Sentinel-2 change instrument instead of a black-box network |
| 035 | [Urban Change Detection for Multispectral Earth Observation Using Convolutional Neural Networks](papers/035-oscd.md) ([source](https://arxiv.org/abs/1810.08468)) | 2018 | historical | OSCD is the small but standard Sentinel-2 urban change benchmark (24 pairs, 13 bands, pixel labels); use it to calibrate optical change thresholds, not to train large models |
| 036 | [An unsupervised approach based on the generalized Gaussian model to automatic change detection in multitemporal SAR images](papers/036-sar-logratio-gg.md) ([source](https://doi.org/10.1109/TGRS.2004.842441)) | 2005 | historical | Canonical SAR change recipe (despeckle, log-ratio, automatic threshold from a fitted two-class model); adopt it nearly as-is for Sentinel-1 change with the fitted model doubling as a confidence source |
| 037 | [A Spatial-Temporal Attention-Based Method and a New Dataset for Remote Sensing Image Change Detection](papers/037-levir-cd-stanet.md) ([source](https://www.mdpi.com/2072-4292/12/10/1662)) | 2020 | recent | LEVIR-CD (637 pairs, 0.5 m, Texas buildings) became the default CD benchmark; useful for language templates and model comparison but not for calibrating 10 m Sentinel instruments |
| 038 | [Remote Sensing Image Change Detection with Transformers](papers/038-bit-transformer-cd.md) ([source](https://arxiv.org/abs/2103.00208)) | 2021 | recent | Strong, small (about 3.5M params) learned CD baseline at 89.3 F1 on LEVIR-CD but only 69.3 on DSIFN; a cross-check at most, never the source of SatClip's number |
| 039 | [xBD: A Dataset for Assessing Building Damage from Satellite Imagery](papers/039-xbd.md) ([source](https://arxiv.org/abs/1911.09296)) | 2019 | historical | Largest pre/post building damage set (850k polygons, 19 events, sub-0.8 m); its baseline damage F1 of about 0.27 shows per-building damage is out of reach for 10 m Sentinel, so SatClip should abstain on it |
| 040 | [Remote Sensing Image Change Captioning With Dual-Branch Transformers: A New Method and a Large Scale Dataset](papers/040-levir-cc-rsiccformer.md) ([source](https://doi.org/10.1109/TGRS.2022.3218921)) | 2022 | recent | LEVIR-CC (10,077 pairs, 50,385 captions, half no-change) is the standard change-captioning set; good template data for SatClip's explanation layer, but captions carry no measured quantities |
| 041 | [Kuro Siwo: 33 billion m² under the water. A global multi-temporal satellite dataset for rapid flood mapping](papers/041-kuro-siwo.md) ([source](https://arxiv.org/abs/2311.12056)) | 2024 | recent | Expert-labelled Sentinel-1 pre/post flood set (43 events, CC BY, separates flood from permanent water); the best calibration set for SatClip's SAR flood change instrument, though Asia is underrepresented |

### data-infrastructure

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 047 | [Google Earth Engine: Planetary-scale geospatial analysis for everyone](papers/047-google-earth-engine.md) ([source](https://doi.org/10.1016/j.rse.2017.06.031)) | 2017 | historical | The reference cloud EO platform: a hosted multi-sensor catalogue with lazy, tile-parallel evaluation; most Indian SAR flood papers run on it, but it is closed and code-centric, so SatClip should match its ergonomics on open STAC plus COG |
| 048 | [The Australian Geoscience Data Cube - Foundations and lessons learned](papers/048-australian-geoscience-data-cube.md) ([source](https://doi.org/10.1016/j.rse.2017.03.015)) | 2017 | historical | Open Data Cube foundations: analysis-ready, provenance-tracked data plus a light index and open (Apache 2.0) code make time series trustworthy; SatClip should copy the provenance discipline, not the heavy ingest |
| 049 | [OGC Cloud Optimized GeoTIFF Standard](papers/049-ogc-cloud-optimized-geotiff.md) ([source](https://docs.ogc.org/is/21-026/21-026.html)) | 2023 | recent | COG 1.0 formalises tiled GeoTIFFs with overviews and headers up front, served over HTTP range requests; this is what lets SatClip read only the district window from a Sentinel scene on a CPU worker |
| 050 | [SpatioTemporal Asset Catalog (STAC) Specification](papers/050-stac-spec.md) ([source](https://stacspec.org/en)) | 2024 | recent | STAC is the common search language of public EO catalogues (Item, Catalog, Collection, API); SatClip should search with STAC API and record STAC Item IDs and hrefs in every receipt |

### efficient-inference

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 059 | [LoRA: Low-Rank Adaptation of Large Language Models](papers/059-lora.md) ([source](https://arxiv.org/abs/2106.09685)) | 2021 | recent | The adapter method behind SatClip's VLM fine-tuning pipeline; merge adapters for zero-latency CPU inference and keep the base weights frozen and versioned |
| 060 | [QLoRA: Efficient Finetuning of Quantized LLMs](papers/060-qlora.md) ([source](https://arxiv.org/abs/2305.14314)) | 2023 | recent | 4-bit base plus LoRA adapters makes VLM fine-tuning fit on one consumer or free-tier GPU; SatClip's LoRA pipeline should offer a QLoRA mode |
| 061 | [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](papers/061-awq.md) ([source](https://arxiv.org/abs/2306.00978)) | 2024 | recent | Calibration-light 4-bit weight quantization that preserves accuracy and works for multimodal models; a strong way to shrink SatClip's VLM after LoRA merge |
| 062 | [MobileCLIP: Fast Image-Text Models through Multi-Modal Reinforced Training](papers/062-mobileclip.md) ([source](https://arxiv.org/abs/2311.17049)) | 2024 | recent | Small, fast CLIP models via reinforced training; a CPU-friendly alternative encoder for SatClip's zero-shot land cover instrument if licence and accuracy on Sentinel-2 check out |
| 063 | [SmolVLM: Redefining small and efficient multimodal models](papers/063-smolvlm.md) ([source](https://arxiv.org/abs/2504.05299)) | 2025 | recent | Fully open 256M to 2.2B VLMs built for edge devices; the most realistic CPU base for SatClip's question parser and explainer, fine-tuned with LoRA |
| 064 | [Distilling the Knowledge in a Neural Network](papers/064-hinton-knowledge-distillation.md) ([source](https://arxiv.org/abs/1503.02531)) | 2015 | historical | Classic recipe for training a small student model on a large teacher's softened outputs; SatClip can use it to shrink a CLIP land-cover head or a question parser so it runs fast on CPU |

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
| 051 | [SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery](papers/051-satmae.md) ([source](https://arxiv.org/abs/2207.08051)) | 2022 | recent | The founding MAE recipe for multispectral and temporal satellite data; treat it as background and baseline, not as a SatClip runtime component |
| 052 | [Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications](papers/052-prithvi-eo-2.md) ([source](https://arxiv.org/abs/2412.02732)) | 2024 | recent | Open NASA/IBM multi-temporal HLS model with flood and crop fine-tune recipes; best GPU candidate for a learned second opinion next to SatClip's optical instruments, not a CPU default |
| 053 | [SkySense: A Multi-Modal Remote Sensing Foundation Model Towards Universal Interpretation for Earth Observation Imagery](papers/053-skysense.md) ([source](https://arxiv.org/abs/2312.10115)) | 2024 | recent | Billion-parameter optical plus SAR plus time model showing fusion helps; a ceiling to cite, but non-commercial weights and size rule it out for SatClip |
| 054 | [SSL4EO-S12: A Large-Scale Multi-Modal, Multi-Temporal Dataset for Self-Supervised Learning in Earth Observation](papers/054-ssl4eo-s12.md) ([source](https://arxiv.org/abs/2211.07044)) | 2023 | recent | Open Sentinel-1/2 pretraining corpus with small ResNet50 and ViT-S weights in TorchGeo; the most CPU-friendly source of Sentinel-native features for SatClip experiments |
| 055 | [CROMA: Remote Sensing Representations with Contrastive Radar-Optical Masked Autoencoders](papers/055-croma.md) ([source](https://arxiv.org/abs/2311.00566)) | 2023 | recent | MIT-licensed radar plus optical encoder trained on Sentinel-1/2; best candidate for a learned SAR feature cross-check next to SatClip's Otsu water instrument |
| 056 | [Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation](papers/056-dofa.md) ([source](https://arxiv.org/abs/2403.15356)) | 2024 | recent | One encoder for any band set via wavelength conditioning (DOFA); lets SatClip use a single learned backbone for both Sentinel-1 and Sentinel-2 in experiments |
| 057 | [Clay Foundation Model](papers/057-clay-foundation-model.md) ([source](https://clay-foundation.github.io/model/)) | 2024 | recent | Apache-licensed multi-sensor embedding model with precomputed embeddings; useful for similarity search and change hints in SatClip, never as the source of reported numbers |
| 058 | [SpectralGPT: Spectral Remote Sensing Foundation Model](papers/058-spectralgpt.md) ([source](https://arxiv.org/abs/2311.07113)) | 2024 | recent | 3D spatial-spectral MAE for Sentinel-2 with change detection results; reference for spectral-aware features, but GPL licence and size keep it out of SatClip core |

### historical

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 016 | [Exploring Models and Data for Remote Sensing Image Caption Generation](papers/016-rsicd-captioning.md) ([source](https://arxiv.org/abs/1712.07835)) | 2018 | historical | Use its caption annotation rules as SatClip's caption style guide; do not trust BLEU or CIDEr without a grounding check |

### human-factors

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 065 | [Trust in Automation: Designing for Appropriate Reliance](papers/065-lee-see-trust-in-automation.md) ([source](https://doi.org/10.1518/hfes.46.1.50_30392)) | 2004 | historical | Foundational review arguing that trust should match automation capability (calibrated trust), not be maximised; SatClip should design the evidence card to expose when and why instruments are reliable |
| 066 | [Guidelines for Human-AI Interaction](papers/066-amershi-human-ai-guidelines.md) ([source](https://doi.org/10.1145/3290605.3300233)) | 2019 | historical | 18 validated design guidelines for AI products; SatClip should use them as a checklist for its chat UI and evidence card, especially setting expectations, scoping when unsure and supporting correction |
| 067 | [Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance](papers/067-bansal-explanations-team-performance.md) ([source](https://arxiv.org/abs/2006.14779)) | 2021 | recent | Explanations made people accept AI answers more often whether right or wrong, adding nothing over showing confidence alone; SatClip's VLM explanations must not make wrong numbers more persuasive |
| 068 | [NL4DV: A Toolkit for Generating Analytic Specifications for Data Visualization from Natural Language Queries](papers/068-nl4dv-natural-language-vis.md) ([source](https://doi.org/10.1109/TVCG.2020.3030378)) | 2021 | recent | Python toolkit that turns a natural-language data question into a structured JSON of attributes, tasks and charts, with explicit ambiguity flags; SatClip's question parser should emit a similar inspectable spec |
| 069 | [Earth observation tools and services to increase the effectiveness of humanitarian assistance](papers/069-lang-eo-humanitarian-services.md) ([source](https://doi.org/10.1080/22797254.2019.1684208)) | 2019 | historical | Field report on delivering EO information to MSF and other NGOs, stressing that trust, reliability and workflow fit, not algorithms, limit uptake; SatClip should design around delivery and trust for non-expert responders |
| 070 | [Effect of Confidence and Explanation on Accuracy and Trust Calibration in AI-Assisted Decision Making](papers/070-zhang-confidence-trust-calibration.md) ([source](https://doi.org/10.1145/3351095.3372852)) | 2020 | recent | Showing a confidence score helped people rely on AI more when it was confident, but did not raise joint accuracy, and SHAP explanations did not help calibration; SatClip should show calibrated confidence and treat it as a reliance aid, not an accuracy fix |

### indian-context

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 042 | [Flood inundation mapping- Kerala 2018; Harnessing the power of SAR, automatic threshold detection method and Google Earth Engine](papers/042-kerala-2018-otsu-gee.md) ([source](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237324)) | 2020 | recent | Otsu on Sentinel-1 VV (Lee 5x5) mapped the Kerala August 2018 flood at about 94.7% OA (kappa 0.87 to 0.88) against Sentinel-2; a ready Indian validation event and baseline for our SAR water instrument |
| 043 | [Google Earth Engine-Based Identification of Flood Extent and Flood-Affected Paddy Rice Fields Using Sentinel-2 MSI and Sentinel-1 SAR Data in Bihar State, India](papers/043-bihar-2020-flood-paddy.md) ([source](https://doi.org/10.1007/s12524-021-01487-3)) | 2022 | recent | Bihar monsoon 2020: S1 plus S2 in GEE mapped about 7,019 sq km submerged and water standing on paddy for 50 to 65 days; a model for flood-on-crop questions, but method details sit behind a paywall |
| 044 | [High resolution paddy rice maps in cloud-prone Bangladesh and Northeast India using Sentinel-1 data](papers/044-singha-paddy-ne-india.md) ([source](https://doi.org/10.1038/s41597-019-0036-3)) | 2019 | historical | Sentinel-1 VH time series plus random forest mapped 2017 paddy at 10 m in Northeast India and Bangladesh per season (Boro, Aus, Aman) at 94 to 98% OA; reuse as a crop mask and adopt VH time series for rice questions |
| 045 | [Radar versus optical: The impact of cloud cover when mapping seasonal surface water for health applications in monsoon-affected India](papers/045-radar-vs-optical-monsoon.md) ([source](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314033)) | 2025 | recent | In Western Ghats districts, July to August cloud cover averaged about 90%, leaving roughly a quarter of surface water unmapped in the optical JRC product; Sentinel-1 VV recovered it, so monsoon questions must default to SAR |
| 046 | [Flood Affected Area Atlas of India - Satellite based study](papers/046-nrsc-flood-atlas.md) ([source](https://ndem.nrsc.gov.in/documents/downloads/allindia_flood_techdoc.pdf)) | 2023 | recent | The official Indian baseline: 25 years (1998 to 2022) of IRS and foreign optical/SAR flood layers, SAR water by variable thresholding, validated by state agencies; SatClip should complement it, not compete |

### object-detection

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 071 | [DOTA: A Large-scale Dataset for Object Detection in Aerial Images](papers/071-dota-aerial-detection.md) ([source](https://arxiv.org/abs/1711.10398)) | 2018 | historical | The standard oriented-box benchmark for aerial object detection (15 classes, very high resolution); useful context but its objects are mostly below Sentinel-2's 10 m pixel, so SatClip should not promise object counts |
| 072 | [xView: Objects in Context in Overhead Imagery](papers/072-xview-overhead-objects.md) ([source](https://arxiv.org/abs/1802.07856)) | 2018 | historical | Over 1 million objects in 60 classes from 0.3 m WorldView-3 imagery, with a weak SSD baseline; shows how hard fine-grained small-object detection is even at 0.3 m, reinforcing that SatClip should not count objects in Sentinel data |
| 073 | [Object Detection in Optical Remote Sensing Images: A Survey and A New Benchmark](papers/073-dior-optical-rs-detection.md) ([source](https://arxiv.org/abs/1909.00133)) | 2020 | recent | Survey plus the DIOR benchmark (23,463 images, 20 classes, 0.5 to 30 m); a reference for mixed-resolution detection, but SatClip should cite it only to justify scoping out object-level questions |
| 074 | [Oriented R-CNN for Object Detection](papers/074-oriented-rcnn.md) ([source](https://arxiv.org/abs/2108.05699)) | 2021 | recent | Simple, fast two-stage rotated-box detector (75.87% mAP on DOTA, 96.50% on HRSC2016, 15.1 FPS on a GPU); a strong baseline if SatClip ever adds ship detection, but its GPU speed does not translate to our CPU budget |
| 075 | [xView3-SAR: Detecting Dark Fishing Activity Using Synthetic Aperture Radar Imagery](papers/075-xview3-sar-dark-vessels.md) ([source](https://arxiv.org/abs/2206.00897)) | 2022 | recent | Large Sentinel-1 VV/VH ship detection benchmark (991 scenes, 243,018 labelled objects); the closest object-detection work to SatClip's own data, useful for SAR preprocessing and as a model for honest, partially reliable labels |

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

### trust-calibration

| ID | Paper | Year | Era | Takeaway for SatClip |
|---|---|---|---|---|
| 026 | [On Calibration of Modern Neural Networks](papers/026-calibration-modern-nets.md) ([source](https://arxiv.org/abs/1706.04599)) | 2017 | historical | Modern deep nets are overconfident; fit one temperature on held-out data to calibrate any score, report ECE and a reliability diagram, accuracy is unchanged |
| 027 | [Selective Classification for Deep Neural Networks](papers/027-selective-classification.md) ([source](https://arxiv.org/abs/1705.08500)) | 2017 | historical | Pick the abstention threshold from a target risk with a statistical guarantee on held-out data; trading coverage for reliability (2% ImageNet top-5 error at about 60% coverage) |
| 028 | [Uncertainty Sets for Image Classifiers using Conformal Prediction](papers/028-raps-conformal.md) ([source](https://arxiv.org/abs/2009.14193)) | 2021 | recent | RAPS wraps any classifier to output label sets with a finite-sample coverage guarantee (for example 90%), with sets often 5 to 10 times smaller than a Platt-scaling baseline |
| 029 | [Evaluating Object Hallucination in Large Vision-Language Models](papers/029-pope.md) ([source](https://arxiv.org/abs/2305.10355)) | 2023 | recent | LVLMs often claim objects that are not there, especially frequent or co-occurring ones; POPE's yes/no probing with adversarial negatives is a cheap template for SatClip's hallucination tests |
| 030 | [Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly](papers/030-reliable-vqa.md) ([source](https://arxiv.org/abs/2204.13631)) | 2022 | recent | Softmax-thresholded VQA models answer under 7.5% of questions at 1% risk; a learned multimodal selector raises coverage from 6.8% to 15.6%, and Effective Reliability penalises wrong answers more than abstentions |
| 031 | [Enabling Calibration In The Zero-Shot Inference of Large Vision-Language Models](papers/031-clip-zero-shot-calibration.md) ([source](https://arxiv.org/abs/2303.12748)) | 2023 | recent | CLIP zero-shot scores are miscalibrated; one temperature learned per CLIP model on an auxiliary set transfers across prompts and datasets, so calibrate RemoteCLIP once and reuse |
| 032 | [Spatial-Aware Conformal Prediction for Trustworthy Hyperspectral Image Classification](papers/032-sacp-hyperspectral-conformal.md) ([source](https://arxiv.org/abs/2409.01236)) | 2024 | recent | Conformal prediction works for per-pixel RS classification, and smoothing non-conformity scores over spatial neighbours gives smaller sets at the same guaranteed coverage; apply it to SatClip masks |
| 033 | [RSHallu: Dual-Mode Hallucination Evaluation for Remote-Sensing Multimodal Large Language Models with Domain-Tailored Mitigation](papers/033-rshallu.md) ([source](https://arxiv.org/abs/2602.10799)) | 2026 | upcoming | RS VLMs answer hallucination-free only about 36% to 69% of the time on RSHalluEval, including errors about modality and resolution; strong evidence that SatClip's VLM must not produce measurements |

<!-- CATALOG:END -->
