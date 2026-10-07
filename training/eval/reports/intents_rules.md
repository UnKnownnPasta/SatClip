# Intent parsing: rules

Data: `training/data/intents/test.jsonl` (1500 questions).

| Slice | n | Valid JSON | Intent | District | Dates | Full match |
|---|---|---|---|---|---|---|
| all | 1500 | 1.000 | 0.973 | 0.925 | 1.000 | 0.898 |
| en | 837 | 1.000 | 0.951 | 0.920 | 1.000 | 0.872 |
| hinglish | 391 | 1.000 | 1.000 | 0.923 | 1.000 | 0.923 |
| hi | 272 | 1.000 | 1.000 | 0.941 | 1.000 | 0.941 |

Refusal precision 0.821, recall 1.0.
