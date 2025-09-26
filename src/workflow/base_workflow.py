import time
from random import random

def classify_document(text: str, threshold: float = 0.5):
    """
    Dummy classifier: returns 'Compliant' if random score >= threshold.
    Replace with real LLM logic later.
    """
    start = time.time()
    score = random()
    label = "Compliant" if score >= threshold else "Non-compliant"
    runtime = time.time() - start
    return {"label": label, "score": score, "runtime": runtime}
