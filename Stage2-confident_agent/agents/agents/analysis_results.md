# Results: baseline vs Confident Agent

Prompts analysed: **76**

## 1. Hallucination rate (paired, primary analysis)

| System | Hallucinated | Rate | 95% Wilson CI |
|---|---|---|---|
| Baseline | 36/76 | 47.4% | 36.5% to 58.4% |
| Confident Agent | 22/76 | 28.9% | 20.0% to 40.0% |

- Absolute reduction: **18.4 percentage points** (paired bootstrap 95% CI 9.2 to 28.9)
- Relative reduction: **38.9%**
- Discordant pairs: prevented (baseline hallucinated, agent not) = 16; introduced (agent hallucinated, baseline not) = 2
- McNemar exact test: **p = 0.0013** (significant at 0.05)

## 2. Side effects and trade-offs

| Metric | Value |
|---|---|
| Withheld (flagged) answers | 9/76 (11.8%) |
| **False rejection rate** (correct baseline answers withheld) | 2/37 (5.4%, CI 1.5% to 17.7%) |
| Degradation rate (correct baseline answer replaced by an incorrect one) | 0/37 (0.0%) |
| Flag precision (withheld answers that were hallucinated in the baseline) | 6/9 (66.7%) |
| Baseline correct-answer rate | 37/76 (48.7%) |
| Agent correct-answer rate (answers shown and correct) | 41/76 (53.9%) |

**What happened to the baseline's hallucinations** (n = 36):

- withheld by the agent: 6
- repaired (regenerated/filtered answer is correct): 6
- replaced by an answer that is not hallucinated but not fully correct: 4
- missed (still hallucinated): 20

## 3. Pipeline decisions

| Status | Count |
|---|---|
| ACCEPTED | 41 |
| ACCEPTED_AFTER_REGEN | 22 |
| FLAGGED | 9 |
| ACCEPTED_FILTERED | 4 |

## 4. By category

| Group | n | Baseline HR | Agent HR | Prevented | Introduced | Withheld |
|---|---|---|---|---|---|---|
| A_Lesson | 18 | 44.4% (8) | 50.0% (9) | 0 | 1 | 0 |
| B_Obscure | 10 | 80.0% (8) | 50.0% (5) | 3 | 0 | 0 |
| C_QuizKey | 15 | 13.3% (2) | 13.3% (2) | 0 | 0 | 1 |
| D_CodeReasoning | 8 | 50.0% (4) | 37.5% (3) | 2 | 1 | 1 |
| E_Trap | 10 | 70.0% (7) | 30.0% (3) | 4 | 0 | 2 |
| F_Materials | 15 | 46.7% (7) | 0.0% (0) | 7 | 0 | 5 |

## 5. By obscurity level

| Group | n | Baseline HR | Agent HR | Prevented | Introduced | Withheld |
|---|---|---|---|---|---|---|
| level 1 | 16 | 18.8% (3) | 25.0% (4) | 0 | 1 | 1 |
| level 2 | 32 | 46.9% (15) | 31.2% (10) | 6 | 1 | 2 |
| level 3 | 28 | 64.3% (18) | 28.6% (8) | 10 | 0 | 6 |

## 6. By course

| Group | n | Baseline HR | Agent HR | Prevented | Introduced | Withheld |
|---|---|---|---|---|---|---|
| COMP200 | 24 | 58.3% (14) | 29.2% (7) | 8 | 1 | 4 |
| COMP301 | 52 | 42.3% (22) | 28.8% (15) | 8 | 1 | 5 |

## 7. Cost and latency

| | Baseline | Confident Agent |
|---|---|---|
| Mean seconds per prompt | 32.6 | 124.9 (generation 32.6 + validation 92.3) |
| Mean LLM calls per prompt | 1 | 9.3 |
| Slow-down factor | 1.0x | 3.8x |

## 8. Scorer agreement and sensitivity

Baseline answers re-scored blind: 26
- Agreement on 'hallucination': 92.3% (Cohen's kappa = 0.75)
- Agreement on 'correct': 88.5% (Cohen's kappa = 0.60)
- Sensitivity (using the blind re-score for those baseline answers): baseline HR 47.4%, agent HR 28.9%, McNemar p = 0.0026
