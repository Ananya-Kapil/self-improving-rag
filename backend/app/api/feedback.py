from fastapi import APIRouter
from pydantic import BaseModel
import json

LOG_FILE = "data/logs/query_logs.json"

router = APIRouter()


class FeedbackRequest(BaseModel):
    timestamp: str
    feedback: str


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    for log in logs:
        if log["timestamp"] == request.timestamp:
            log["feedback"] = request.feedback
            break

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    return {
        "message": "Feedback saved successfully."
    }