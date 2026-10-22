"""Collect real timed executions; synthetic input is explicitly labelled smoke."""
import argparse, csv, json, tempfile
from pathlib import Path
from datetime import datetime, timezone
from benchmark import run, ROOT

def collect(path):
    cfg = json.loads(path.read_text(encoding="utf-8"))
    records = []
    # One complete unreported warm-up pass precedes measured runs.
    for phase in ["warmup", "benchmark"]:
        current = dict(cfg)
        if phase == "warmup": current["seeds"] = [cfg["seeds"][0]]
        current["output_dir"] = cfg["output_dir"] + "/" + phase
        with tempfile.TemporaryDirectory() as tmp:
            cp = Path(tmp) / "config.json"
            cp.write_text(json.dumps(current), encoding="utf-8")
            run(cp)
        output = ROOT / current["output_dir"]
        for row in csv.DictReader((output / "metrics.csv").open(encoding="utf-8")):
            row["phase"] = phase
            records.append(row)
        if phase == "benchmark":
            manifest = json.loads((output / "run_manifest.json").read_text())
    target = ROOT / "data/raw/test_run.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(x)+"\n" for x in records), encoding="utf-8")
    manifest.update(collected_at_utc=datetime.now(timezone.utc).isoformat(), warmup_policy="One full pass with first seed, excluded from analysis", raw_log=str(target.relative_to(ROOT)))
    (ROOT / "data/processed/run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Saved {len(records)} rows to {target}")

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--config", type=Path, default=ROOT/"configs/task3_smoke.json")
    collect(p.parse_args().config)
