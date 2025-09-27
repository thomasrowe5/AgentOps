import pandas as pd
from pathlib import Path
from time import perf_counter
import yaml
from src.workflow.base_workflow import classify_document
from src.monitor.logger import append_metrics

# ✅ Output location for the new metrics
CSV_OUT = "data/metrics_new.csv"

# ✅ Load the labeled test data
df = pd.read_csv("data/test_data.csv")

# ✅ Load updated config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

threshold = cfg["workflow"].get("threshold", 0.5)

def main():
    print("🚀 Running new baseline workflow with updated parameters + quality metrics...\n")
    for i, row in df.iterrows():
        text = row["text"]
        true_label = row["label"]

        # Measure total runtime
        start = perf_counter()
        result = classify_document(text, threshold=threshold)
        total = perf_counter() - start

        # ✅ Make sure we log BOTH true_label and pred_label here
        metrics_row = {
            "iteration": i,
            "text_len": len(text),
            "true_label": true_label,
            "pred_label": result["label"],
            "score": result["score"],
            "runtime": result["runtime"],
            "total_time": total,
            "threshold": threshold
        }

        append_metrics(CSV_OUT, metrics_row)

    print("📊 New baseline run complete — results saved to data/metrics_new.csv")

if __name__ == "__main__":
    main()

