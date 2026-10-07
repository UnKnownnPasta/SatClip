# Intent parsing: rules

Data: `training/data/intents/test.jsonl` (1500 questions, districts unseen in training).

| Slice | n | Valid JSON | Intent | District | Dates | Full match |
|---|---|---|---|---|---|---|
| all | 1500 | 1.000 | 0.569 | 0.925 | 0.197 | 0.163 |
| en | 837 | 1.000 | 0.865 | 0.920 | 0.219 | 0.196 |
| hinglish | 391 | 1.000 | 0.276 | 0.923 | 0.220 | 0.153 |
| hi | 272 | 1.000 | 0.081 | 0.941 | 0.099 | 0.077 |

Refusal precision 0.257, recall 0.957.
