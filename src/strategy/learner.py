import csv
import random
import math
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# -------- Paths / schema --------
MEM_PATH = Path("data/strategy_memory.csv")
FIELDS = ["action", "attempts", "successes", "success_rate", "last_applied_utc"]

# -------- Memory IO --------
def _load_memory() -> Dict[str, dict]:
    mem = {}
    if MEM_PATH.exists():
        with MEM_PATH.open("r") as f:
            reader = csv.DictReader(f)
            for r in reader:
                mem[r["action"]] = {
                    "attempts": int(r["attempts"]),
                    "successes": int(r["successes"]),
                    "success_rate": float(r["success_rate"]),
                    "last_applied_utc": r.get("last_applied_utc", "")
                }
    return mem

def _save_memory(mem: Dict[str, dict]) -> None:
    with MEM_PATH.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for a, v in mem.items():
            attempts = max(0, int(v.get("attempts", 0)))
            successes = max(0, int(v.get("successes", 0)))
            sr = (successes / attempts) if attempts > 0 else 0.0
            w.writerow({
                "action": a,
                "attempts": attempts,
                "successes": successes,
                "success_rate": sr,
                "last_applied_utc": v.get("last_applied_utc", "")
            })

# -------- Public API: update memory --------
def record_attempt(applied: List[str]) -> None:
    mem = _load_memory()
    now = datetime.utcnow().isoformat()
    for a in applied:
        if a not in mem:
            mem[a] = {"attempts": 0, "successes": 0, "success_rate": 0.0, "last_applied_utc": ""}
        mem[a]["attempts"] += 1
        mem[a]["last_applied_utc"] = now
    _save_memory(mem)

def record_outcome(applied: List[str], improved: bool) -> None:
    mem = _load_memory()
    for a in applied:
        if a not in mem:
            mem[a] = {"attempts": 0, "successes": 0, "success_rate": 0.0, "last_applied_utc": ""}
        if improved:
            mem[a]["successes"] += 1
    _save_memory(mem)

# -------- Ranking / Stats --------
def ranked_actions() -> List[str]:
    """Return actions ranked by success_rate desc, then attempts desc."""
    mem = _load_memory()
    items = sorted(
        mem.items(),
        key=lambda kv: (kv[1]["success_rate"], kv[1]["attempts"]),
        reverse=True
    )
    return [a for a, _ in items]

def total_attempts() -> int:
    mem = _load_memory()
    return sum(v.get("attempts", 0) for v in mem.values())

# -------- Dynamic epsilon policy --------
def dynamic_epsilon(
    start_eps: float = 0.30,
    min_eps: float = 0.05,
    k: float = 0.10
) -> float:
    """
    Exponential decay: eps(t) = max(min_eps, start_eps * exp(-k * t))
    where t = total optimization attempts recorded.
    """
    t = total_attempts()
    eps = start_eps * math.exp(-k * t)
    return max(min_eps, eps)

def choose_action_epsilon_greedy(epsilon: float = None) -> str:
    """
    Epsilon-greedy selector with optional dynamic epsilon.
    If epsilon is None, compute dynamic epsilon from memory.
    """
    mem = _load_memory()
    if not mem:
        return None

    actions = list(mem.keys())
    eps = dynamic_epsilon() if epsilon is None else max(0.0, min(1.0, epsilon))

    # Exploration
    if random.random() < eps:
        return random.choice(actions)

    # Exploitation
    ranked = ranked_actions()
    return ranked[0] if ranked else random.choice(actions)

# -------- Utility for external modules --------
def bandit_status() -> dict:
    mem = _load_memory()
    return {
        "epsilon": dynamic_epsilon(),
        "known_actions": list(mem.keys()),
        "ranking": ranked_actions(),
        "total_attempts": total_attempts(),
    }

