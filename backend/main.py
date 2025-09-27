from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "✅ AgentOps backend is running!"}


@app.get("/metrics/history")
def get_metrics_history():
    """Return all historical optimization cycles from CSV."""
    if not os.path.exists("data/optimization_history.csv"):
        return []
    df = pd.read_csv("data/optimization_history.csv")
    return df.to_dict(orient="records")


@app.get("/strategy/leaderboard")
def get_strategy_leaderboard():
    """Aggregate optimization history into a leaderboard of strategies."""
    if not os.path.exists("data/optimization_history.csv"):
        return []

    df = pd.read_csv("data/optimization_history.csv")

    # Expect columns: change, accuracy_after, f1_after, accepted
    if not {"change", "accuracy_after", "f1_after", "accepted"}.issubset(df.columns):
        return []

    leaderboard = (
        df.groupby("change")
        .agg(
            times_used=("change", "count"),
            avg_accuracy=("accuracy_after", "mean"),
            avg_f1=("f1_after", "mean"),
            win_rate=("accepted", "mean"),
        )
        .reset_index()
    )

    leaderboard = leaderboard.rename(columns={"change": "name"})
    return leaderboard.to_dict(orient="records")

import subprocess

@app.post("/optimize/run")
def run_optimization():
    """
    Runs the full optimization pipeline by calling optimize.py
    """
    try:
        result = subprocess.run(
            ["python", "optimize.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "success": True,
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": e.stderr
        }

