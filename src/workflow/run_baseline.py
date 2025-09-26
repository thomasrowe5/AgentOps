from pathlib import Path
from time import perf_counter
from src.workflow.base_workflow import classify_document
from src.monitor.logger import append_metrics

DOCS = Path("data/test_docs.txt").read_text().strip().splitlines()
CSV = "data/metrics.csv"

def main():
    for i, text in enumerate(DOCS):
        start = perf_counter()
        result = classify_document(text, threshold=0.5)
        total = perf_counter() - start
        row = {
            "iteration": i,
            "text_len": len(text),
            "label": result["label"],
            "score": result["score"],
            "runtime": result["runtime"],
            "total_time": total
        }
        append_metrics(CSV, row)
    print("Baseline runs logged to", CSV)

if __name__ == "__main__":
    main()
