# Comparative Evaluation of Machine Learning Algorithms for Spam Email Detection

## Authors
Roman Bukin. Individual project for Research Methods, Task 2.

## Overview
This repository continues Task 1 and provides a runnable measurement pipeline for Logistic Regression, Multinomial Naive Bayes and Random Forest. It measures spam-class F1, false positives and secondary metrics. The included artificial sample checks execution only. It does not establish algorithm quality.

## Research Question
How do algorithm choice and training-set size affect spam email classification performance and false positive rate under controlled conditions?

## System Requirements
Python 3.12 (tested with 3.12.14); Windows, Linux or macOS; internet access for initial dependency installation. A modest laptop is sufficient for the ten-row smoke test. Resource requirements for the full corpus depend on its size. All runtime packages, including transitive dependencies, are pinned in requirements.txt. Pip is the installer, not a benchmark dependency. A requirements-based environment is used under the rubric's allowed alternative; no Docker build is claimed.

## Quickstart Guide
Download and extract the repository, open a terminal in its root folder, and run these three commands on Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src\benchmark.py
```

Linux and macOS:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/benchmark.py
```

Expected success message: `OK: 3 benchmark rows saved to .../results/smoke` followed by the synthetic-sample warning. Output files: metrics.csv, predictions.csv, run_manifest.json. Outputs are local and ignored by Git. Re-running replaces the configured output files; choose a new output_dir to preserve a run. Exit code 0 means measurement completed; it does not mean all FPR guardrails passed. Check fpr_guardrail_pass in metrics.csv.

## Repository Structure
```text
.
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
├── requirements.txt
├── config.json
├── configs/
│   └── research.json
├── src/
│   └── benchmark.py
├── data/
│   └── sample/
│       ├── emails.csv
│       └── README.md
└── docs/
    ├── Methodology_Card.md
    ├── dataset.md
    ├── verification.md
    └── START_HERE_RU.md
```

## Planned Benchmarks
| Benchmark | Algorithms | Training fractions | Seeds | Data | Purpose |
|---|---|---|---|---|---|
| Smoke test | NB, LR, RF | 100% of training pool | 42 | 10 artificial emails, 60/40 split | Verify execution; 3 metric rows |
| Main experiment | NB, LR, RF | 25%, 50%, 100% | 42–46 | Licensed email corpus, fixed 80/20 split | Compare quality and training size; 45 metric rows |

## Main Experiment
Select and register the corpus using docs/dataset.md before Week 7. Put a cleaned CSV with id,text,label columns in data/private/emails.csv. Valid labels are ham and spam. Do not publish the private data. Run from the root:

```powershell
.venv\Scripts\python.exe src\benchmark.py --config configs\research.json
```

The research configuration is prepared but cannot run until the real CSV exists. The same holdout is reused across models, fractions and seeds. TF-IDF is fitted only on training data. Exact normalized duplicates are rejected; near-duplicate and thread handling must be completed during dataset preparation. The methodology card defines the hypotheses, baseline, guardrails and later inference plan. Formal significance tests are not part of this measurement skeleton.

## Citation and License
Suggested citation: Bukin, R. (2026). Comparative Evaluation of Machine Learning Algorithms for Spam Email Detection. Research Methods course project. Add the public repository URL and exact commit when citing a run.

Code and artificial sample: MIT, see LICENSE. A future research corpus retains its original licence. Methodological implementation reference: https://scikit-learn.org/stable/common_pitfalls.html
