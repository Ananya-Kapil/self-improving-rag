import json
import os

LOG_FILE = "data/logs/query_logs.json"


def load_feedback_scores():
    """
    Returns a dictionary:
    {
        (filename, page, chunk): score
    }

    Positive feedback = +1
    Negative feedback = -1
    """

    scores = {}

    if not os.path.exists(LOG_FILE):
        return scores

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    for log in logs:

        feedback = log.get("feedback")

        if feedback not in ["positive", "negative"]:
            continue

        value = 1 if feedback == "positive" else -1

        for chunk in log["context"]:

            key = (
                chunk["filename"],
                chunk["page"],
                chunk["chunk"],
            )

            scores[key] = scores.get(key, 0) + value

    return scores