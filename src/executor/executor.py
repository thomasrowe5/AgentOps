import json
import re
from pathlib import Path
from src.executor.config_manager import load_config, save_config

SUGGESTIONS_PATH = Path("data/suggestions.json")
APPLIED_PATH = Path("data/applied_actions.json")

def parse_suggestions():
    if not SUGGESTIONS_PATH.exists():
        print("❌ No suggestions found.")
        return ""
    data = json.loads(SUGGESTIONS_PATH.read_text())
    raw_text = data.get("raw", "")

    # Extract JSON inside code block if present
    json_match = re.search(r"\{[\s\S]*\}", raw_text)
    if json_match:
        try:
            parsed_json = json.loads(json_match.group(0))
            changes = [c["change"] for c in parsed_json.get("changes", [])]
            raw_text += " " + " ".join(changes)
        except json.JSONDecodeError:
            pass
    return raw_text.lower()

def apply_suggestions(raw_text: str):
    cfg = load_config()
    applied = []

    if "threshold" in raw_text:
        old = cfg["workflow"].get("threshold", 0.5)
        cfg["workflow"]["threshold"] = round(min(1.0, old + 0.05), 2)
        print(f"✅ Increased threshold: {old} → {cfg['workflow']['threshold']}")
        applied.append("increase_threshold")

    if "temperature" in raw_text:
        old = cfg["model"].get("temperature", 0.3)
        cfg["model"]["temperature"] = round(min(1.0, old + 0.1), 2)
        print(f"✅ Increased temperature: {old} → {cfg['model']['temperature']}")
        applied.append("increase_temperature")

    if "chunk" in raw_text or "chunk size" in raw_text:
        old = cfg["workflow"].get("initial_chunk_size", 1000)
        cfg["workflow"]["initial_chunk_size"] = old + 200
        print(f"✅ Increased chunk size: {old} → {cfg['workflow']['initial_chunk_size']}")
        applied.append("increase_chunk_size")

    # Non-parameter hints (still record as actions)
    if "cross-validation" in raw_text:
        print("⚙️ Suggestion: add cross-validation (not implemented).")
        applied.append("consider_cross_validation")

    if "hyperparameter" in raw_text or "grid search" in raw_text:
        print("⚙️ Suggestion: hyperparameter tuning (not implemented).")
        applied.append("consider_hparam_tuning")

    if "dataset" in raw_text or "data set" in raw_text:
        print("⚙️ Suggestion: expand dataset (not implemented).")
        applied.append("consider_expand_dataset")

    if applied:
        save_config(cfg)

    # persist applied actions for the optimizer to log
    APPLIED_PATH.write_text(json.dumps({"applied": applied}, indent=2))
    return applied

def run_executor():
    text = parse_suggestions()
    if not text:
        APPLIED_PATH.write_text(json.dumps({"applied": []}, indent=2))
        return []
    return apply_suggestions(text)

