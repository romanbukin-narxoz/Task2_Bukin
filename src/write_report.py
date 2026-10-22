from pathlib import Path
import pandas as pd
from process_data import ROOT

def write_report():
    s=pd.read_csv(ROOT/"data/processed/metrics_summary.csv")
    mode=s["mode"].iloc[0]
    table=["| Model | Spam F1 mean [95% CI] | FPR mean [95% CI] | Fit ms mean ± SD | Prediction ms/email mean ± SD |", "|---|---|---|---|---|"]
    for _,v in s[s.train_fraction.eq(1)].iterrows():
        name=v.model+(" (baseline)" if v.model=="naive_bayes" else "")
        table.append(f"| {name} | {v.f1_mean:.3f} [{v.f1_ci_low:.3f}, {v.f1_ci_high:.3f}] | {v.false_positive_rate_mean:.3f} [{v.false_positive_rate_ci_low:.3f}, {v.false_positive_rate_ci_high:.3f}] | {v.fit_ms_mean:.3f} ± {v.fit_ms_sd:.3f} | {v.predict_ms_per_email_mean:.3f} ± {v.predict_ms_per_email_sd:.3f} |")
    status=("Only the 10 artificial emails supplied in Task 2 were available. All numerical results below are smoke-test results, not evidence of real-world spam detection quality. A real-corpus experiment remains incomplete." if mode=="smoke" else "Research configuration executed. Check dataset documentation, licensing, deduplication and holdout design before interpreting these results.")
    full=s[s.train_fraction.eq(1)]
    failed=int((~full.fpr_guardrail_pass_all_runs.astype(bool)).sum())
    observation=f"At full training size, {failed} of {len(full)} models fail the observed FPR guardrail in at least one seed run. This is a failed guardrail check, not successful validation of the threshold."
    report=f"""# Task 3 Research results and data analysis

Roman Bukin. Comparative Evaluation of Machine Learning Algorithms for Spam Email Detection.

## Scope and data

{status}

## Method

Continue the Task 2 TF-IDF pipeline and compare Multinomial Naive Bayes (baseline), Logistic Regression and Random Forest. Use a fixed stratified holdout, paired seeds 42–46, and training fractions 25%, 50%, 100%. TF-IDF is fitted only on training emails. The sample uses the original 60/40 smoke split, not the planned 80/20 research split. Actual sample training sizes are 2, 2, 6; 25% and 50% select the same number of emails.

One complete warm-up pass with seed 42 is recorded separately. Nine warm-up rows are excluded; 45 benchmark rows remain. Timing values come from actual executions in the supplied runtime, not the student's PC. The manifest records the environment and input checksum. Re-running locally changes timing measurements.

## Results & Discussion

Full-training-pool results (five seed runs each):

{chr(10).join(table)}

{observation}

Confidence intervals use 5000 seed-level bootstrap resamples with seed 42. The processed CSV also reports medians, p95, SD and classification error rate. CI values describe variability between runs on the same holdout. They are not confidence intervals for population generalization or formal evidence that one algorithm is better. The p95 is across run-level batch averages, not individual-email latency.

The sample contains only four test emails, including two ham emails. Therefore the false-positive guardrail is reported descriptively; it cannot establish a population FPR below 5%. Identical predictions can produce zero SD and zero-width bootstrap intervals. Five repeated seeds do not create five independent test sets. These results verify that the data-processing and export pipeline works. No real-world ranking or statistical superiority claim is made.

## Figures

Figure 1 shows prediction time against the fraction of the training pool, not concurrent server load. Figure 2 shows training-time distributions at 100% of the training pool; diamonds and error bars indicate bootstrap means and intervals. Figure 3 shows F1 and FPR. All figures have 300 DPI PNG and vector PDF versions, labeled units, distinguishable markers/line styles, and a colorblind-safe palette. Zero-width intervals may be hidden by markers.

## Domain model

See docs/domain_model.md for the training objective, model definitions, F1, FPR and variables.

## Reproducibility and remaining work

Raw data: data/raw/test_run.jsonl. Aggregates: data/processed/metrics_summary.csv. Environment and checksum: data/processed/run_manifest.json. Analysis: notebooks/01_data_analysis.ipynb. Repeat with python src/run_task3.py. The build host used fresh-process sequential IPython execution because local kernel sockets are unavailable; all code cells ran in order and their actual outputs were saved. Before submission, rerun with the standard Jupyter kernel on your computer to meet the Restart and Run All requirement.

To complete the research, obtain and document a permitted real email corpus, remove duplicates and prevent thread leakage, store id,text,label CSV locally in data/private/emails.csv, then run python src/run_task3.py --config configs/research.json. Review regenerated results and report. No email text should be published without permission. No new literature review was fabricated; Task 1 references should be retained in the existing repository.
"""
    (ROOT/"reports/Task3_Report.md").write_text(report,encoding="utf-8")
    readme=report.replace("# Task 3 Research results and data analysis","# Spam detection research Tasks 2 and 3")
    readme+="\n## Plots\n\n"+"\n".join(f"![Figure {i}](reports/figures/{name}.png)\n" for i,name in enumerate(["fig1_latency_vs_load","fig2_distribution_boxplot","fig3_quality"],1))
    readme+="\n[Domain model](docs/domain_model.md) · [Executed notebook](notebooks/01_data_analysis.ipynb) · [Report for LMS](reports/Task3_Report.md) · [Russian instructions](START_TASK3_RU.md) · [Original Task 2 README](docs/README_Task2.md)\n"
    (ROOT/"README.md").write_text(readme,encoding="utf-8")
    print("Updated report and README.")
if __name__=="__main__": write_report()
