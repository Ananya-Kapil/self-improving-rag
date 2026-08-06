import json
import os
from collections import Counter

LOG_FILE = "data/logs/query_logs.json"


def analyze_feedback():
    """
    Analyze user feedback stored in query_logs.json.
    """

    if not os.path.exists(LOG_FILE):
        return {
            "total_queries": 0,
            "positive": 0,
            "negative": 0,
            "top_pages": [],
        }

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    positive = 0
    negative = 0
    page_counter = Counter()

    for log in logs:

        if log["feedback"] == "positive":
            positive += 1

        elif log["feedback"] == "negative":
            negative += 1

        for chunk in log["context"]:
            page_counter[chunk["page"]] += 1

    return {
        "total_queries": len(logs),
        "positive": positive,
        "negative": negative,
        "top_pages": page_counter.most_common(5),
    }