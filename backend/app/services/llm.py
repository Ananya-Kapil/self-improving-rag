import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_answer(question: str, context: str):
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
7. Keep answers concise, factual, and well-structured.
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

    payload = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
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