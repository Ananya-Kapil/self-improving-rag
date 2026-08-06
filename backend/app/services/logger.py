import json
import os
from datetime import datetime

LOG_FILE = "data/logs/query_logs.json"


def log_query(
    question,
    rewritten_question,
    answer,
    context,
):
    """
    Save every query and return its timestamp.
    """

    timestamp = datetime.now().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "question": question,
        "rewritten_question": rewritten_question,
        "answer": answer,
        "feedback": None,
        "context": [
            {
                "filename": chunk["metadata"]["filename"],
                "page": chunk["metadata"]["page_number"],
                "chunk": chunk["metadata"]["chunk_number"],
            }
            for chunk in context
        ],
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    # Return the timestamp so the frontend can use it later
    return timestamp