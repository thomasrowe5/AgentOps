# AgentOps
Self-optimizing workflow automation engine:
- Monitors a target workflow
- Uses an LLM to propose improvements
- Executes experiments
- Accepts/rejects changes based on metrics

## Quickstart
1) `python3 -m venv .venv && source .venv/bin/activate`
2) `pip install -r requirements.txt`
3) Put your API key in `.env`
4) `python src/main.py`
