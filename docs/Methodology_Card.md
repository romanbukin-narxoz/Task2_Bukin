# Methodology Passport Card

## Project information
**Title:** Comparative Evaluation of Machine Learning Algorithms for Spam Email Detection  
**Author:** Roman Bukin  
**Work format:** Individual  
**GitHub repository:** TO BE FILLED AFTER CREATING THE PUBLIC REPOSITORY  
**Stage:** Task 2, Weeks 5–6. Measurement pipeline and research protocol; no research conclusions yet.

This study continues Task 1 by comparing Logistic Regression, Multinomial Naive Bayes and Random Forest under the same evaluation conditions. It examines classification quality, false positives and the effect of training-set size.

## Research type
Quantitative experimental research. The algorithm and training-set size are varied, and numerical metrics are measured on the same held-out messages. No interviews or qualitative coding are planned.

## Research questions and hypotheses
The following operational definitions refine the three hypotheses from Task 1.

**RQ1:** How do the algorithms differ in spam classification quality at the full training size?  
**H0₁:** The algorithms have equal population spam-class F1 scores under the specified evaluation protocol.  
**H1₁:** At least one algorithm has a different population spam-class F1 score.

**RQ2:** Which algorithm achieves the best F1 while limiting legitimate emails incorrectly marked as spam?  
**H0₂:** The algorithms have equal population false positive rates at the full training size.  
**H1₂:** At least one algorithm has a different population false positive rate.  
Operational selection rule: compare F1 only among models with observed FPR ≤ 5%. If none meets this guardrail, report that no model meets the requirement; do not label a model safe. The 5% threshold is a proposed course-project criterion, not an industry standard or a production guarantee.

**RQ3:** How does training-set size affect performance for each fixed algorithm?  
**H0₃:** Expected spam-class F1 is equal at 25%, 50% and 100% of the available training pool.  
**H1₃:** At least one training fraction produces a different expected spam-class F1 for that algorithm.

## Variable matrix
| Type | Variable | Operational definition |
|---|---|---|
| Independent | Algorithm | Multinomial Naive Bayes, Logistic Regression, Random Forest |
| Independent | Training fraction | 25%, 50%, 100% of the 80% training pool; actual row counts recorded |
| Dependent | Primary quality | Spam-class F1 score, range 0–1 |
| Dependent | Guardrail | False positive rate FP / (FP + TN), proposed maximum 0.05 |
| Dependent | Secondary quality | Accuracy, spam precision, spam recall and confusion-matrix counts |
| Dependent | Secondary efficiency | Pipeline fit time in ms; batch prediction time divided by test emails, ms/email |
| Controlled | Data and split | Same cleaned email corpus; fixed stratified 80/20 split, split seed 42; identical held-out IDs for all runs |
| Controlled | Text representation | Lowercase word TF-IDF, unigram features, maximum 5000 features, min_df 1; fitted only on the selected training subset |
| Controlled | Model settings | Fixed hyperparameters in config; no test-set tuning; native predict decision rule |
| Controlled | Environment | Same machine and OS for compared runs; Python 3.12.14 and exact package pins; one computational thread |
| Controlled | Randomness | Paired seeds 42–46; identical selected training IDs across models for a seed and fraction |

The test set stays unchanged as training size varies. Class-wise shuffled training lists create nested subsets for each seed. Counts are rounded down with at least one message per class. At 100%, Naive Bayes may produce identical scores across seeds; these are not independent replications. The sample smoke test instead uses a 60/40 split and only the full training size because it contains just ten messages.

## Metrics and baseline
**Primary metric:** F1 = 2TP / (2TP + FP + FN), treating spam as the positive class. It measures the balance of spam precision and recall; accuracy alone can hide poor minority-class detection. Undefined precision or F1 is recorded as zero by the implementation.

**Guardrails:** FPR ≤ 0.05; successful execution without missing/invalid input or fitting errors. FPR is reported alongside FP and the total number of legitimate test messages. A guardrail failure is recorded, not hidden. On the artificial sample it is diagnostic only.

**Secondary metrics:** Accuracy, precision, recall, fit time and prediction ms/email. Fit time includes TF-IDF fitting; prediction time includes transformation. Timing is descriptive and hardware-dependent, not a production latency guarantee.

**Baseline:** Multinomial Naive Bayes with alpha=1.0 using the same TF-IDF representation, training subset and held-out test set as the other models. Logistic Regression uses C=1.0, liblinear, max_iter=1000; Random Forest uses 100 trees, unlimited depth, n_jobs=1. No model receives a separate tuning budget.

## Experimental procedure and analysis plan
1. Before Week 7, select and document a legally usable labelled email corpus in docs/dataset.md. Remove duplicate and near-duplicate leakage and examine related threads before freezing the split. A real corpus was not specified in Task 1 and is not claimed to be present here.
2. Use the fixed 80/20 stratified split, then train all three algorithms at each fraction and seed: 3 algorithms × 3 fractions × 5 seeds = 45 measurement rows.
3. Fit TF-IDF only on each training subset and apply it to the test set through the same pipeline. Save configuration, versions, dataset checksum, split IDs, metrics and per-message predictions.
4. Report seed-wise scores and mean scores, plus baseline differences. Repeated use of one test set does not provide five independent test samples. Do not apply an independent-samples t-test to the seed rows.
5. For the later hypothesis analysis, plan a paired stratified bootstrap over held-out email IDs (10000 resamples, bootstrap seed 2026), reusing each resample across compared models and averaging paired differences over seeds. This estimates test-sample uncertainty conditional on the trained models; it does not cover uncertainty from choosing another corpus or split. For RQ1 compare all three model pairs; for RQ2 compare FPR for all three pairs; for RQ3 compare all three size pairs within each algorithm. Use Bonferroni-adjusted two-sided intervals across the 15 planned contrasts (individual confidence level 99.6667%, family level approximately 95%). An interval excluding zero is evidence against the corresponding equality hypothesis, subject to bootstrap assumptions. Otherwise report insufficient evidence, not proof of equality.
6. Select the highest-F1 model passing the FPR guardrail, and discuss the sample size and uncertainty. Results from the ten artificial examples cannot test any hypothesis.

The Task 2 executable measures metrics and saves predictions. Formal bootstrap analysis is a planned later analysis, not an implemented or completed result. Dataset-dependent evaluation and the bootstrap procedure must be reviewed before drawing final conclusions.

## Reproducibility and limitations
The repository contains exact runtime dependency pins, config.json, an executable src/benchmark.py, ten artificial sample rows, README, .gitignore and MIT LICENSE. The benchmark records its runtime environment automatically. For main-run timing comparisons, additionally record CPU model, RAM and OS details in the experiment notes and keep background load low.

The current deliverable establishes a working measurement pipeline. Real dataset selection, the main experiment and statistical conclusions remain for later research stages. The public repository URL must be inserted before Task 2 submission.

## Implementation reference
Scikit-learn documentation, Common pitfalls and recommended practices, data leakage: https://scikit-learn.org/stable/common_pitfalls.html
