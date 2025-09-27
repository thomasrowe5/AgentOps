import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path
from src.executor.comparator import compare_runs

BASELINE_PATH = Path("data/metrics.csv")
NEW_PATH = Path("data/metrics_new.csv")

# ⚖️ How much runtime should influence the score (tune this)
ALPHA = 0.1

def evaluate_change():
    if not BASELINE_PATH.exists() or not NEW_PATH.exists():
        print("❌ Metrics files not found. Run both workflows first.")
        return

    df_before = pd.read_csv(BASELINE_PATH)
    df_after = pd.read_csv(NEW_PATH)

    # ✅ Compute quality metrics
    acc_before = accuracy_score(df_before["true_label"], df_before["pred_label"])
    acc_after = accuracy_score(df_after["true_label"], df_after["pred_label"])

    prec_before = precision_score(df_before["true_label"], df_before["pred_label"], pos_label="Compliant")
    prec_after = precision_score(df_after["true_label"], df_after["pred_label"], pos_label="Compliant")

    rec_before = recall_score(df_before["true_label"], df_before["pred_label"], pos_label="Compliant")
    rec_after = recall_score(df_after["true_label"], df_after["pred_label"], pos_label="Compliant")

    f1_before = f1_score(df_before["true_label"], df_before["pred_label"], pos_label="Compliant")
    f1_after = f1_score(df_after["true_label"], df_after["pred_label"], pos_label="Compliant")

    # ✅ Runtime comparison
    results = compare_runs(df_before, df_after)
    runtime_before = results['before_avg_s']
    runtime_after = results['after_avg_s']

    # ⚖️ Compute smart scores
    smart_before = f1_before - ALPHA * runtime_before
    smart_after = f1_after - ALPHA * runtime_after

    # 📊 Print results
    print("\n📊 QUALITY COMPARISON:")
    print(f"Accuracy:  {acc_before:.2f} → {acc_after:.2f}")
    print(f"Precision: {prec_before:.2f} → {prec_after:.2f}")
    print(f"Recall:    {rec_before:.2f} → {rec_after:.2f}")
    print(f"F1 Score:  {f1_before:.2f} → {f1_after:.2f}")

    print("\n📈 PERFORMANCE COMPARISON:")
    print(f"Before Avg Runtime: {runtime_before:.6f}s")
    print(f"After Avg Runtime:  {runtime_after:.6f}s")
    print(f"Δ Runtime:         {results['delta_s']:.6f}s")

    print("\n⚖️ SMART SCORE:")
    print(f"Before SmartScore: {smart_before:.4f}")
    print(f"After SmartScore:  {smart_after:.4f}")

    # ✅ Decide based on smart score
    if smart_after > smart_before:
        print("✅ Change accepted — composite score improved.")
    else:
        print("❌ Change rejected — performance trade-off not worth it.")

