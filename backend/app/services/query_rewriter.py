
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

Use the conversation history to understand what the user is referring to.

Rules:
1. Resolve references like "it", "its", "they", "this", and "that".
2. Preserve the user's intent.
3. Do not answer the question.
4. Return ONLY the rewritten question.
5. If the question is already standalone, return it unchanged.

Example:

Previous conversation:
User: What is the main topic of this document?
Assistant: The document discusses renewable energy.

Current question:
What are its advantages?

Output:
What are the advantages of renewable energy?
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    for message in history:
        if isinstance(message, dict):
            role = message.get("role")
            content = message.get("content")

            if role in ["user", "assistant"] and content:
                messages.append({
                    "role": role,
                    "content": str(content),
                })

    messages.append({
        "role": "user",
        "content": question,
    })

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

        rewritten = data["choices"][0]["message"]["content"].strip()

        return rewritten if rewritten else question

    except Exception as e:
        print(f"Query rewriting failed: {e}")
        return question