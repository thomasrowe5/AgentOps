import os, json, pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

def suggest_improvements(metrics_csv: str, suggestions_path: str):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    df = pd.read_csv(metrics_csv).tail(10) if Path(metrics_csv).exists() else pd.DataFrame()
    summary = df.describe(include='all').to_string() if not df.empty else "No data yet."

    prompt = f"""
You are optimizing a classification workflow. Here are the last runs' metrics:
{summary}

Propose 3 specific, testable changes to improve either accuracy, runtime, or consistency.
Return JSON with fields: changes[], rationale.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    text = resp.choices[0].message.content
    out = {"raw": text}
    Path(suggestions_path).write_text(json.dumps(out, indent=2))
    print("Suggestions written to", suggestions_path)
