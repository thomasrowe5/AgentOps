import os
from dotenv import load_dotenv
import yaml
from pathlib import Path

def load_config():
    with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in .env")
    cfg = load_config()
    print("AgentOps starting...")
    print("Model:", cfg["model"]["name"])
    print("Workflow:", cfg["workflow"]["name"])
    # For now, just a smoke test
    print("✅ Environment OK")

if __name__ == "__main__":
    main()
