
from app.services.query_rewriter import rewrite_query


def test_empty_history_returns_original_question():
    question = "What are the advantages?"

    result = rewrite_query(question, [])

    assert result == question


def test_none_history_returns_original_question():
    question = "What are the advantages?"

    result = rewrite_query(question, None)

    assert result == question


def test_follow_up_question_uses_conversation_history(monkeypatch):
    question = "What are its advantages?"

    history = [
        {
            "role": "user",
            "content": "What is the main topic of this document?",
        },
        {
            "role": "assistant",
            "content": "The main topic is Big Data.",
        },
    ]

    def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "What are the advantages of Big Data?"
                            }
                        }
                    ]
                }

        return MockResponse()

    monkeypatch.setattr(
        "app.services.query_rewriter.requests.post",
        mock_post,
    )

    result = rewrite_query(question, history)

    assert result == "What are the advantages of Big Data?"

