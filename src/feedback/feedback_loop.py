from pathlib import Path
import pandas as pd
from src.executor.comparator import compare_runs

def decide_accept(baseline_csv: str, new_csv: str):
    df0 = pd.read_csv(baseline_csv) if Path(baseline_csv).exists() else pd.DataFrame()
    df1 = pd.read_csv(new_csv) if Path(new_csv).exists() else pd.DataFrame()
    result = compare_runs(df0, df1)
    return result["is_better"], result
