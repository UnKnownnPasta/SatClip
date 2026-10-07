# VRSBench VQA: converter check and answer-prior floor

Converted `VRSBench_EVAL_vqa.json` (Hugging Face xiang709/VRSBench, fetched 2026-10-07) with `eval_vqa.py --convert-vrsbench`: 37409 questions, all converted. Images (`Images_val.zip`, about 4 GB) were not downloaded in run 7, so no model was scored.

Answer-prior floor: answering the most frequent answer of each question type, with the prior taken from this same eval file (an optimistic oracle floor, since a real baseline would learn it from the train split): **0.345** overall.

| Type | n | Most frequent answer | Share |
|---|---|---|---|
| object existence | 7789 | yes | 0.818 |
| object quantity | 6374 | 2 | 0.319 |
| object position | 5828 | yes | 0.199 |
| object category | 5434 | ship | 0.093 |
| object color | 3550 | green | 0.194 |
| scene type | 3197 | yes | 0.108 |
| object shape | 1423 | rectangular | 0.163 |
| image | 1129 | grayscale | 0.578 |
| object size | 1011 | small | 0.276 |
| reasoning | 902 | yes | 0.439 |
| object direction | 477 | east-west | 0.233 |
| rural or urban | 295 | rural | 0.420 |

Yes/no balance: 9003 yes against 1883 no (0.83 yes). A model that always says yes to existence questions scores 0.82 on them, so SatClip should report VRSBench existence accuracy next to this prior, not alone.
