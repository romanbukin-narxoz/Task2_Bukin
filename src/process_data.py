"""Descriptive seed-level bootstrap; not population-level inference."""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
METRICS=["f1", "false_positive_rate", "accuracy", "fit_ms", "predict_ms_per_email"]
def load_data(path=ROOT/"data/raw/test_run.jsonl"):
    raw=pd.read_json(path, lines=True)
    required={"phase", "mode", "model", "seed", "train_fraction", "n_train", "n_test", *METRICS}
    if not required <= set(raw): raise ValueError(f"Missing columns: {required-set(raw)}")
    if not set(raw.phase)<= {"warmup", "benchmark"}: raise ValueError("Unknown phase")
    frame=raw.loc[raw.phase.eq("benchmark")].copy()
    if frame.empty: raise ValueError("No benchmark rows")
    for col in ["seed", "train_fraction", "n_train", "n_test", "tn", "fp", "fn", "tp", *METRICS]:
        frame[col]=pd.to_numeric(frame[col], errors="raise")
        if not np.isfinite(frame[col]).all(): raise ValueError(f"Nonfinite {col}")
    if frame.duplicated(["mode","model","train_fraction","seed"]).any(): raise ValueError("Duplicate runs")
    if len(frame["mode"].unique())!=1: raise ValueError("Do not mix smoke and research")
    frame["classification_error_rate"]=(frame.fp+frame.fn)/frame.n_test
    return raw, frame

def bootstrap_mean(values, rng, n_boot=5000):
    x=np.asarray(values,dtype=float)
    means=rng.choice(x,size=(n_boot,len(x)),replace=True).mean(axis=1)
    return np.quantile(means,[.025,.975])

def summarize(frame):
    rng=np.random.default_rng(42)
    rows=[]
    for (mode,model,fraction), group in frame.groupby(["mode","model","train_fraction"],sort=True):
        row=dict(mode=mode,model=model,train_fraction=fraction,n_train=int(group.n_train.iloc[0]),n_test=int(group.n_test.iloc[0]),n_runs=len(group))
        for metric in METRICS+["classification_error_rate"]:
            x=group[metric].to_numpy(dtype=float)
            lo,hi=bootstrap_mean(x,rng)
            for suffix,value in {"mean":x.mean(),"sd":x.std(ddof=1) if len(x)>1 else 0.,"median":np.median(x),"p95":np.percentile(x,95),"ci_low":lo,"ci_high":hi}.items():
                row[f"{metric}_{suffix}"]=float(value)
        row["fpr_guardrail_pass_all_runs"]=bool((group.false_positive_rate<=.05).all())
        rows.append(row)
    return pd.DataFrame(rows)

def process():
    raw,frame=load_data()
    summary=summarize(frame)
    (ROOT/"data/processed").mkdir(parents=True,exist_ok=True)
    summary.to_csv(ROOT/"data/processed/metrics_summary.csv",index=False)
    print(f"Excluded {len(raw)-len(frame)} warm-up rows; retained {len(frame)} benchmark rows.")
    return frame,summary
if __name__=="__main__": process()
