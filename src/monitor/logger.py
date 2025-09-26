import csv
from pathlib import Path

def append_metrics(csv_path, row: dict):
    p = Path(csv_path)
    exists = p.exists()
    with p.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(row)
