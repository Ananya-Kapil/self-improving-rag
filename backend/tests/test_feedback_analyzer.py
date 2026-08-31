id="v5m7q2"
import json

from app.services.feedback_analyzer import analyze_feedback


def test_analytics_with_no_log_file(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    monkeypatch.setattr(
        "app.services.feedback_analyzer.LOG_FILE",
        str(log_file),
    )

    result = analyze_feedback()

    assert result["total_queries"] == 0
    assert result["positive"] == 0
    assert result["negative"] == 0
    assert result["feedback_rate"] == 0
    assert result["helpfulness_rate"] == 0
    assert result["top_pages"] == []


def test_analytics_calculates_feedback_rates(tmp_path, monkeypatch):
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
            "feedback": "positive",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 2,
                }
            ],
        },
        {
            "feedback": "negative",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 2,
                    "chunk": 1,
                }
            ],
        },
    ]

    log_file.write_text(
        json.dumps(logs),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.services.feedback_analyzer.LOG_FILE",
        str(log_file),
    )

    result = analyze_feedback()

    assert result["total_queries"] == 3
    assert result["positive"] == 2
    assert result["negative"] == 1

    assert result["feedback_rate"] == 100.0
    assert result["helpfulness_rate"] == 66.7


def test_analytics_counts_feedback_chunks(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    logs = [
        {
            "feedback": "positive",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 1,
                },
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 2,
                },
            ],
        },
        {
            "feedback": "negative",
            "context": [
                {
                    "filename": "test.pdf",
                    "page": 1,
                    "chunk": 2,
                },
                {
                    "filename": "test.pdf",
                    "page": 2,
                    "chunk": 1,
                },
            ],
        },
    ]

    log_file.write_text(
        json.dumps(logs),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.services.feedback_analyzer.LOG_FILE",
        str(log_file),
    )

    result = analyze_feedback()

    assert result["feedback_chunks"] == 3
    assert result["positive_chunks"] == 2
    assert result["negative_chunks"] == 2


def test_analytics_returns_top_pages(tmp_path, monkeypatch):
    log_file = tmp_path / "query_logs.json"

    logs = [
        {
            "feedback": None,
            "context": [
                {"filename": "test.pdf", "page": 1, "chunk": 1},
                {"filename": "test.pdf", "page": 1, "chunk": 2},
                {"filename": "test.pdf", "page": 2, "chunk": 1},
            ],
        }
    ]

    log_file.write_text(
        json.dumps(logs),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.services.feedback_analyzer.LOG_FILE",
        str(log_file),
    )

    result = analyze_feedback()

    assert result["top_pages"][0] == (1, 2)
    assert result["top_pages"][1] == (2, 1)

