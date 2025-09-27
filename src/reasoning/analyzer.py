import os
import json
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

from src.strategy.learner import ranked_actions, choose_action_epsilon_greedy, bandit_status

def suggest_improvements(metrics_csv: str, suggestions_path: str):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Load metrics
    df = pd.read_csv(metrics_csv) if Path(metrics_csv).exists() else pd.DataFrame()
    summary = df.describe(include='all').to_string() if not df.empty else "No data available yet."

    # Multi-armed bandit (dynamic epsilon)
    status = bandit_status()
    preferred_actions = status.get("ranking", [])
    current_eps = status.get("epsilon", 0.2)
    bandit_choice = choose_action_epsilon_greedy()  # uses dynamic epsilon internally

    # Bias text to steer the LLM
    bias_text = ""
    if preferred_actions:
        bias_text += (
            "Based on historical performance, prioritize the following actions in order of past success: "
            + ", ".join(preferred_actions) + ".\n"
        )
    if bandit_choice:
        bias_text += (
            f"⚡ Multi-Armed Bandit (epsilon ≈ {current_eps:.2f}) suggests focusing on: '{bandit_choice}' "
            "this iteration. This action has either shown strong results or needs exploration.\n"
        )

    prompt = f"""
You are an AI optimization agent. Improve the classification workflow by proposing
3 concrete, testable changes. Consider both model quality (F1/accuracy/precision/recall)
and runtime. Output **ONLY** valid JSON matching the schema below.

{bias_text}

JSON schema:
{{
  "changes": [
    {{
      "change": "Concrete, testable change (e.g., 'Increase threshold by 0.05')",
      "rationale": "Why this should improve SmartScore (F1 - alpha*runtime)"
    }},
    {{
      "change": "Second change",
      "rationale": "Reason"
    }},
    {{
      "change": "Third change",
      "rationale": "Reason"
    }}
  ]
}}

Latest metrics summary:
{summary}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an optimization strategist. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    raw_output = response.choices[0].message.content.strip()

    # Ensure JSON-only output in file (store raw JSON string in "raw")
    try:
        parsed = json.loads(raw_output)
        result = {"raw": json.dumps(parsed, indent=2)}
    except json.JSONDecodeError:
        result = {"raw": raw_output}

    Path(suggestions_path).write_text(json.dumps(result, indent=2))
    print(f"✅ Suggestions written to {suggestions_path}")

if __name__ == "__main__":
    suggest_improvements("data/metrics.csv", "data/suggestions.json")

