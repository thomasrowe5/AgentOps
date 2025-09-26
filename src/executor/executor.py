import json, re
from pathlib import Path

def parse_changes(suggestions_path: str):
    # naive parse: try to find parameter-like hints in the raw text
    raw = json.loads(Path(suggestions_path).read_text())["raw"]
    # super simple examples: look for "threshold", "temperature", "chunk size"
    candidates = []
    for line in raw.splitlines():
        if any(k in line.lower() for k in ["threshold","temperature","chunk","prompt"]):
            candidates.append(line.strip())
    return candidates[:3]

def apply_change(change: str, current_cfg: dict):
    # naive mapping: adjust threshold/temperature/chunk size if mentioned
    l = change.lower()
    if "threshold" in l:
        current_cfg["workflow"]["threshold"] = max(0.0, min(1.0, current_cfg["workflow"].get("threshold", 0.5) + 0.1))
    if "temperature" in l:
        current_cfg["model"]["temperature"] = max(0.0, min(1.0, current_cfg["model"].get("temperature", 0.3) + 0.1))
    if "chunk" in l:
        current_cfg["workflow"]["initial_chunk_size"] = current_cfg["workflow"].get("initial_chunk_size",1000) + 200
    return current_cfg
