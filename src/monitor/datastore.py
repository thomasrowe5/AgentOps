import pandas as pd
from pathlib import Path

def read_metrics(csv_path):
    p = Path(csv_path)
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)
