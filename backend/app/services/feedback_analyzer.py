
import json
import os
from collections import Counter


LOG_FILE = "data/logs/query_logs.json"


def analyze_feedback():
    """
    Analyze query logs and user feedback.
    """

    if not os.path.exists(LOG_FILE):
        return {
            "total_queries": 0,
            "positive": 0,
            "negative": 0,
            "feedback_rate": 0,
            "helpfulness_rate": 0,
            "feedback_chunks": 0,
            "positive_chunks": 0,
            "negative_chunks": 0,
            "top_pages": [],
        }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)

    except (json.JSONDecodeError, OSError):
        return {
            "total_queries": 0,
            "positive": 0,
            "negative": 0,
            "feedback_rate": 0,
            "helpfulness_rate": 0,
            "feedback_chunks": 0,
            "positive_chunks": 0,
            "negative_chunks": 0,
            "top_pages": [],
        }

    positive = 0
    negative = 0

    page_counter = Counter()

    feedback_chunks = set()
    positive_chunks = set()
    negative_chunks = set()

    for log in logs:

        feedback = log.get("feedback")

        if feedback == "positive":
            positive += 1

        elif feedback == "negative":
            negative += 1

        for chunk in log.get("context", []):

            page = chunk.get("page")

            if page is not None:
                page_counter[page] += 1

            filename = chunk.get("filename")
            chunk_number = chunk.get("chunk")

            if filename is not None and page is not None and chunk_number is not None:

                key = (
                    filename,
                    page,
                    chunk_number,
                )

                if feedback in ["positive", "negative"]:
                    feedback_chunks.add(key)

                if feedback == "positive":
                    positive_chunks.add(key)

                elif feedback == "negative":
                    negative_chunks.add(key)

    total_queries = len(logs)
    total_feedback = positive + negative

    feedback_rate = (
        (total_feedback / total_queries) * 100
        if total_queries > 0
        else 0
    )

    helpfulness_rate = (
        (positive / total_feedback) * 100
        if total_feedback > 0
        else 0
    )

    return {
        "total_queries": total_queries,
        "positive": positive,
        "negative": negative,
        "feedback_rate": round(feedback_rate, 1),
        "helpfulness_rate": round(helpfulness_rate, 1),
        "feedback_chunks": len(feedback_chunks),
        "positive_chunks": len(positive_chunks),
        "negative_chunks": len(negative_chunks),
        "top_pages": page_counter.most_common(5),
    }

