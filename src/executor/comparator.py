import pandas as pd

def compare_runs(df_before: pd.DataFrame, df_after: pd.DataFrame):
    # Simple comparison on runtime; expand with accuracy once you add labels
    before = df_before["total_time"].mean() if not df_before.empty else float("inf")
    after = df_after["total_time"].mean() if not df_after.empty else float("inf")
    improvement = before - after
    return {"before_avg_s": before, "after_avg_s": after, "delta_s": improvement, "is_better": after < before}
