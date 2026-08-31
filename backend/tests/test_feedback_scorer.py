
import json

from app.services.feedback_scorer import load_feedback_scores


def test_positive_feedback_increases_score(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    logs = [
        {
            "feedback": "positive",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 1,
                }
            ],
        }
    ]

    log_file.write_text(json.dumps(logs), encoding="utf-8")

    monkeypatch.setattr(
        "app.services.feedback_scorer.LOG_FILE",
        str(log_file),
    )

    scores = load_feedback_scores()

    assert scores[("test.pdf", 1, 1)] == 1


def test_negative_feedback_decreases_score(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    logs = [
        {
            "feedback": "negative",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 1,
                }
            ],
        }
    ]

    log_file.write_text(json.dumps(logs), encoding="utf-8")

    monkeypatch.setattr(
        "app.services.feedback_scorer.LOG_FILE",
        str(log_file),
    )

    scores = load_feedback_scores()

    assert scores[("test.pdf", 1, 1)] == -1


def test_positive_and_negative_feedback_cancel_out(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    logs = [
        {
            "feedback": "positive",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 1,
                }
            ],
        },
        {
            "feedback": "negative",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 1,
                }
            ],
        },
    ]

    log_file.write_text(json.dumps(logs), encoding="utf-8")

    monkeypatch.setattr(
        "app.services.feedback_scorer.LOG_FILE",
        str(log_file),
    )

    scores = load_feedback_scores()

    assert scores[("test.pdf", 1, 1)] == 0

