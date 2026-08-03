import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_answer(question: str, context: str, history: list = None):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = """
You are an AI assistant for Retrieval-Augmented Generation (RAG).

Rules:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not present in the context, reply exactly:
   "I couldn't find that information in the uploaded documents."
4. Do not guess or hallucinate.
5. Mention the page number(s) whenever the context includes them.
6. If multiple pages support the answer, cite all relevant pages.
7. Use the previous conversation only to understand follow-up questions.
8. Never answer using chat history alone. The retrieved context is the source of truth.
9. Keep answers concise, factual, and well-structured.
"""

    user_prompt = f"""
Context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    payload = {
        "model": "openrouter/free",
        "messages": messages,
        "temperature": 0.0,
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

    except requests.exceptions.RequestException as e:
        return f"LLM Error: {e}"

    except (KeyError, IndexError):
        return "LLM Error: Invalid response received from the model."