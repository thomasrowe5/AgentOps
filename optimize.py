import os
import subprocess
import json
import csv
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "data" / "optimization_history.csv"
SUGGESTIONS_FILE = BASE_DIR / "data" / "suggestions.json"
APPLIED_FILE = BASE_DIR / "data" / "applied_actions.json"

os.chdir(BASE_DIR)

def run_command(cmd, label):
    print(f"\n🔧 [{label}] Running: {cmd}\n" + "-"*60)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ {label} failed. Stopping pipeline.")
        exit(1)
    print(f"✅ {label} completed successfully.\n" + "-"*60)

def extract_suggestions_text():
    if not SUGGESTIONS_FILE.exists():
        return "N/A"
    try:
        data = json.loads(SUGGESTIONS_FILE.read_text())
        raw = data.get("raw", "")
        try:
            parsed = json.loads(raw)
            suggestions = [c["change"] for c in parsed.get("changes", [])]
            return " | ".join(suggestions)
        except json.JSONDecodeError:
            return raw[:300]
    except Exception:
        return "N/A"

def extract_applied_actions():
    if not APPLIED_FILE.exists():
        return []
    try:
        data = json.loads(APPLIED_FILE.read_text())
        return data.get("applied", [])
    except Exception:
        return []

def append_to_history(result_summary, applied_actions):
    header = [
        "timestamp",
        "suggestions",
        "applied_actions",
        "before_avg_runtime",
        "after_avg_runtime",
        "delta_runtime",
        "improved"
    ]
    file_exists = LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "suggestions": extract_suggestions_text(),
            "applied_actions": ",".join(applied_actions),
            "before_avg_runtime": result_summary.get("before_avg_s", "N/A"),
            "after_avg_runtime": result_summary.get("after_avg_s", "N/A"),
            "delta_runtime": result_summary.get("delta_s", "N/A"),
            "improved": result_summary.get("is_better", "N/A")
        }
        writer.writerow(row)
        print("📊 Logged optimization cycle to data/optimization_history.csv")

def read_feedback_results():
    import pandas as pd
    from src.executor.comparator import compare_runs
    baseline_path = BASE_DIR / "data" / "metrics.csv"
    new_path = BASE_DIR / "data" / "metrics_new.csv"
    df_before = pd.read_csv(baseline_path)
    df_after = pd.read_csv(new_path)
    return compare_runs(df_before, df_after)

def main():
    print("\n🚀 Starting AgentOps Optimization Pipeline with Strategy Memory...\n")

    # 1) Baseline
    run_command("python -m src.workflow.run_baseline", "Baseline Run")

    # 2) Analyzer
    #   (later we’ll bias analyzer with ranked actions)
    run_command(
        "python -c \"from src.reasoning.analyzer import suggest_improvements; "
        "suggest_improvements('data/metrics.csv','data/suggestions.json')\"",
        "Analyzer (Suggestions)"
    )

    # 3) Executor (apply + write applied_actions.json)
    run_command(
        "python -c \"from src.executor.executor import run_executor; run_executor()\"",
        "Executor (Apply Changes)"
    )
    applied = extract_applied_actions()

    # 3b) Record attempt in strategy memory
    run_command(
        "python -c \"from src.strategy.learner import record_attempt; "
        "import json; from pathlib import Path; "
        "d=json.loads(Path('data/applied_actions.json').read_text()); "
        "record_attempt(d.get('applied', []))\"",
        "Strategy Memory (Record Attempt)"
    )

    # 4) New baseline with updated params
    run_command("python -m src.workflow.run_new_baseline", "New Baseline Run")

    # 5) Feedback loop (quality & runtime printed)
    run_command(
        "python -c \"from src.feedback.feedback_loop import evaluate_change; evaluate_change()\"",
        "Feedback Loop"
    )

    # 6) Read results and log
    try:
        results = read_feedback_results()
        append_to_history(results, applied)
    except Exception as e:
        print("⚠️ Could not log history:", e)

    # 7) Record outcome in strategy memory
    improved = False
    try:
        improved = bool(results.get("is_better", False))
    except Exception:
        pass
    # Push improved flag
    run_command(
        "python -c \"from src.strategy.learner import record_outcome; "
        "import json; from pathlib import Path; "
        "d=json.loads(Path('data/applied_actions.json').read_text()); "
        "record_outcome(d.get('applied', []), True if "+("1" if improved else "0")+ " else False)\"",
        "Strategy Memory (Record Outcome)"
    )

    print("\n✅ AgentOps Optimization Cycle Complete + Strategy Memory Updated!\n")

if __name__ == "__main__":
    main()

