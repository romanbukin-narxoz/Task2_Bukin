"""Publication-format outputs; sample status remains visible in each plot."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from process_data import ROOT,process,bootstrap_mean
COLORS=["#0072B2","#D55E00","#009E73"]
NAMES={"naive_bayes":"Naive Bayes (baseline)","logistic_regression":"Logistic Regression","random_forest":"Random Forest"}

def plots(frame,summary):
    out=ROOT/"reports/figures";out.mkdir(parents=True,exist_ok=True)
    banner="Synthetic smoke test only" if frame["mode"].iloc[0]=="smoke" else "Fixed-holdout experiment"
    models=list(NAMES)
    def save(fig,name):
        fig.tight_layout()
        for ext in ["png","pdf"]: fig.savefig(out/f"{name}.{ext}",dpi=300,bbox_inches="tight")
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5))
    for i,model in enumerate(models):
        s=summary[summary.model.eq(model)].sort_values("train_fraction")
        x=s.train_fraction.to_numpy()*100;y=s.predict_ms_per_email_mean.to_numpy()
        low=s.predict_ms_per_email_ci_low.to_numpy();high=s.predict_ms_per_email_ci_high.to_numpy()
        ax.errorbar(x,y,yerr=[y-low,high-y],color=COLORS[i],marker=["o","s","^"][i],linestyle=["-","--",":"][i],capsize=4,label=NAMES[model])
    ax.set(xlabel="Training pool used (%)",ylabel="Prediction time (ms/email)",title=f"{banner}\nMean with 95% seed-bootstrap CI")
    vals=summary.predict_ms_per_email_mean
    if vals.max()/vals.min()>=100: ax.set_yscale("log")
    ax.legend();ax.grid(alpha=.2);save(fig,"fig1_latency_vs_load")
    fig,ax=plt.subplots(figsize=(8,5));rng=np.random.default_rng(42)
    data=[frame.loc[frame.model.eq(m)&frame.train_fraction.eq(1),"fit_ms"].to_numpy() for m in models]
    box=ax.boxplot(data,patch_artist=True,tick_labels=[NAMES[m].replace(" (baseline)","\n(baseline)") for m in models])
    for i,(patch,x) in enumerate(zip(box["boxes"],data)):
        patch.set_facecolor(COLORS[i]);patch.set_alpha(.35)
        lo,hi=bootstrap_mean(x,rng);mean=x.mean()
        ax.errorbar(i+1,mean,yerr=[[mean-lo],[hi-mean]],fmt="D",color="black",capsize=5)
        ax.scatter(np.full(len(x),i+1)+np.linspace(-.05,.05,len(x)),x,color=COLORS[i],s=18,zorder=3)
    if max(map(max,data))/min(map(min,data))>=10: ax.set_yscale("log")
    ax.set(xlabel="Classifier (100% training pool)",ylabel="Training time (ms)",title=f"{banner}\nSeed distribution and mean 95% bootstrap CI")
    save(fig,"fig2_distribution_boxplot")
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    for ax,metric,label in zip(axes,["f1","false_positive_rate"],["Spam F1 (unitless)","False positive rate (fraction)"]):
        for i,model in enumerate(models):
            s=summary[summary.model.eq(model)].sort_values("train_fraction")
            y=s[f"{metric}_mean"].to_numpy();lo=s[f"{metric}_ci_low"].to_numpy();hi=s[f"{metric}_ci_high"].to_numpy()
            ax.errorbar(s.train_fraction*100,y,yerr=[y-lo,hi-y],marker=["o","s","^"][i],linestyle=["-","--",":"][i],color=COLORS[i],capsize=4,label=NAMES[model])
        ax.set(xlabel="Training pool used (%)",ylabel=label,ylim=(-.03,1.03));ax.grid(alpha=.2)
        if metric=="false_positive_rate": ax.axhline(.05,color="black",linestyle="--",label="FPR limit 0.05")
    axes[1].legend(fontsize=7);fig.suptitle(banner+" — mean and 95% seed-bootstrap CI")
    save(fig,"fig3_quality")
    print("Exported 3 figures as vector PDF and 300 DPI PNG.")
if __name__=="__main__": plots(*process())
