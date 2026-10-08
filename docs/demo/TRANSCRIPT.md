# SatClip scripted demo (full mode)

Generated 2026-10-08 22:50 UTC by `tools/demo.py` against the live public catalogues (Planetary Computer Sentinel-1 RTC, Earth Search Sentinel-2). Every number below was measured in this run.

### Flood extent, published

**Question:** How much of Barpeta was under water on 2024-07-11?

- Understood as: water extent in Barpeta, Assam, 2024-07-05..2024-07-17
- Result: **Answer**. About 914 sq km of Barpeta, Assam under water, 39% of the 2,335 sq km measured (low confidence, 0.62).
- Tiles: 117 of 117 measured, 77.06 s
- Confidence: 0.622 (low), calibration: fitted
- Details: measured_km2 2334.86
- Scenes (1): S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc (2024-07-11)
- Receipt: `5d27fcc87150f848`

### Did the flood spread

**Question:** Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?

- Understood as: water change in Barpeta, Assam, 2024-05-30..2024-06-11 vs 2024-07-05..2024-07-17
- Result: **Not enough evidence**. Insufficient evidence: confidence is below the publication threshold.
- Tiles: 117 of 117 measured, 97.92 s
- Confidence: 0.231 (low), calibration: fitted
- Why: low_confidence
- What would help: Change areas are the least reliable number SatClip measures. Check the water extent on each date instead (buttons below); each is measured and calibrated on its own.
- Details: measured_km2 2334.86, water_before_km2 432.71, water_after_km2 914.48, receded_km2 1.11
- Scenes (2): S1A_IW_GRDH_1SDV_20240605T115717_20240605T115742_054188_06970B_rtc (2024-06-05); S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc (2024-07-11)
- Offered next: Water before: 2024-06-05; Water after: 2024-07-11
- Receipt: `4b761f62146d6e6d`

### Did the flood spread, follow-up: Water before: 2024-06-05

**Question:** How much of Barpeta, Assam was under water on 2024-06-05?

- Understood as: water extent in Barpeta, Assam, 2024-05-30..2024-06-11
- Result: **Answer**. About 413 sq km of Barpeta, Assam under water, 18% of the 2,335 sq km measured (moderate confidence, 0.73).
- Tiles: 117 of 117 measured, 54.04 s
- Confidence: 0.731 (moderate), calibration: fitted
- Details: measured_km2 2334.86
- Scenes (1): S1A_IW_GRDH_1SDV_20240605T115717_20240605T115742_054188_06970B_rtc (2024-06-05)
- Receipt: `3af7eb6ef03ed33a`

### Did the flood spread, follow-up: Water after: 2024-07-11

**Question:** How much of Barpeta, Assam was under water on 2024-07-11?

- Understood as: water extent in Barpeta, Assam, 2024-07-05..2024-07-17
- Result: **Answer**. About 914 sq km of Barpeta, Assam under water, 39% of the 2,335 sq km measured (low confidence, 0.62).
- Tiles: 117 of 117 measured, 0.54 s
- Confidence: 0.622 (low), calibration: fitted
- Details: measured_km2 2334.86
- Scenes (1): S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc (2024-07-11)
- Receipt: `066c86bc6262dd46`

### Crop change

**Question:** Did the crop decline in Darbhanga between 2024-03-01 and 2024-04-25?

- Understood as: vegetation change in Darbhanga, Bihar, 2024-02-24..2024-03-07 vs 2024-04-19..2024-05-01
- Result: **Answer**. About 1,544 sq km of Darbhanga, Bihar with a clear fall in greenness, 63% of the 2,463 sq km measured (high confidence, 0.89).
- Tiles: 128 of 128 measured, 54.28 s
- Confidence: 0.893 (high), calibration: placeholder (not yet fitted on labelled data)
- Details: measured_km2 2462.91, vegetated_before_km2 2221.95, gain_km2 34.08
- Scenes (8): S2A_45RUJ_20240302_0_L2A (2024-03-02); S2A_45RVJ_20240302_0_L2A (2024-03-02); S2B_45RUK_20240307_0_L2A (2024-03-07) ...
- Receipt: `09ece4ffefbcb19f`

### Ambiguous district

**Question:** How much of Aurangabad was under water on 2024-08-10?

- Understood as: water extent in an unspecified area, 2024-08-04..2024-08-16
- Result: **Needs one detail**. I can't answer this yet.
- Tiles: 0 of 0 measured, 0.01 s
- Why: ambiguous_area
- What would help: Several districts share this name: Aurangabad, Bihar; Aurangabad, Maharashtra. Add the state to your question.
- Receipt: `26894ed78153a997`

### Out of scope

**Question:** Count the boats in Ernakulam

- Understood as: a question outside what SatClip can measure
- Result: **Needs one detail**. I can't answer this yet.
- Tiles: 0 of 0 measured, 0.01 s
- Why: out_of_scope
- What would help: Try a supported question, for example: 'How much of Barpeta was under water on 2024-07-11?'
- Receipt: `d4ebf61c83e8dfaa`

### Hindi question

**Question:** Barpeta में 11 जुलाई 2024 को कितना इलाका पानी में डूबा था?

- Understood as: water extent in Barpeta, Assam, 2024-07-05..2024-07-17
- Result: **Answer**. About 914 sq km of Barpeta, Assam under water, 39% of the 2,335 sq km measured (low confidence, 0.62).
- Tiles: 117 of 117 measured, 0.55 s
- Confidence: 0.622 (low), calibration: fitted
- Details: measured_km2 2334.86
- Scenes (1): S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc (2024-07-11)
- Receipt: `a956e4c3744b8e11`

### Warm cache: question 1 again

**Question:** How much of Barpeta was under water on 2024-07-11?

- Understood as: water extent in Barpeta, Assam, 2024-07-05..2024-07-17
- Result: **Answer**. About 914 sq km of Barpeta, Assam under water, 39% of the 2,335 sq km measured (low confidence, 0.62).
- Tiles: 117 of 117 measured, 0.56 s
- Confidence: 0.622 (low), calibration: fitted
- Details: measured_km2 2334.86
- Scenes (1): S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc (2024-07-11)
- Receipt: `5d27fcc87150f848`
