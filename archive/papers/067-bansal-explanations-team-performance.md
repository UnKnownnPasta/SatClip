---
id: 067
title: "Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance"
authors: "Gagan Bansal, Tongshuang Wu, Joyce Zhou, Raymond Fok, Besmira Nushi, Ece Kamar, Marco Tulio Ribeiro, Daniel S. Weld"
year: 2021
venue: "CHI 2021"
link: https://arxiv.org/abs/2006.14779
code: none
category: human-factors
era: recent
tags: [explanations, human-ai-teams, complementary-performance, over-reliance, confidence, user-study, chi]
verified: "2026-10-04 via https://arxiv.org/abs/2006.14779 and https://ar5iv.labs.arxiv.org/html/2006.14779"
takeaway: "Explanations made people accept AI answers more often whether right or wrong, adding nothing over showing confidence alone; SatClip's VLM explanations must not make wrong numbers more persuasive"
---

# Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance

## Problem
Earlier studies showing explanations help human-AI teams often used AI that was much more accurate than people, so the AI alone would have done better. The real question is whether explanations help a team beat both the human and the AI when the two are comparably accurate.

## Approach
Large crowdsourced experiments where AI accuracy was deliberately set close to human accuracy. Conditions included human alone, team with AI prediction plus confidence only, and teams with different explanation styles: highlighting evidence for the top class, highlighting evidence for the top two classes, and an adaptive version that switched style based on AI confidence. Explanations came from LIME (for sentiment) or from experts.

## Data and benchmarks
- Sentiment classification of beer reviews and Amazon book reviews (50 examples each; AI accuracy set to 84%).
- LSAT logical reasoning questions (20 examples; AI about 65% versus humans about 67%).
- Roughly 1,600 Mechanical Turk participants recruited in total, about 100 per condition after filtering (figures as summarised from the paper).

## Key results
- Teams showed complementary performance: for beer reviews the team reached about 89% versus 84% AI and 82% human.
- Adding explanations gave no significant improvement over showing confidence alone, on any of the three tasks.
- Explanations raised acceptance of the AI's recommendation regardless of correctness: they helped when the AI was right and hurt when it was wrong.
- Adaptive explanations reduced blind agreement somewhat on low-confidence items but did not significantly lift final accuracy.

## Limitations
- Lay crowdworkers on short text tasks, not domain experts on high-stakes spatial decisions.
- Small item sets (20 to 50 examples) and specific explanation methods (LIME highlights).
- We did not access the ACM DL version; venue taken from the arXiv comment "CHI'21".

## What it means for SatClip
- Avoid persuasive VLM prose: the explanation layer should describe how a number was measured and its limits, not argue that the number is right. Fluent text increases acceptance of wrong answers.
- Lead with calibrated confidence and the evidence (mask overlay, scene date), since confidence alone did as well as explanations in this study.
- When confidence is low, change the presentation (show the uncertainty and alternatives, or abstain) rather than add more explanation, echoing the adaptive condition.
- In our user test, measure agreement on cases where SatClip is wrong, not just overall satisfaction, to detect over-reliance.
