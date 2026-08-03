import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def rewrite_query(question: str, history: list = None):

    if not history:
        return question

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = """
You rewrite follow-up questions into standalone questions.

Rules:
1. Use the conversation history.
2. Preserve the user's intent.
3. Do not answer the question.
4. Return ONLY the rewritten standalone question.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    payload = {
        "model": "openrouter/free",
        "messages": messages,
        "temperature": 0,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return question