from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embeddings import get_embeddings
from app.rag.vector_store import search_chunks
from app.services.llm import generate_answer


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


def choose_results_count(question: str):
    """
    Dynamically choose retrieval size.
    """

    words = len(question.split())

    if words <= 5:
        return 3

    elif words <= 12:
        return 5

    else:
        return 8


@router.post("/query")
async def query(request: QueryRequest):

    # Convert question into embedding
    query_embedding = get_embeddings([request.question])[0]

    # Dynamically retrieve chunks
    n_results = choose_results_count(request.question)

    results = search_chunks(
        query_embedding,
        n_results=n_results,
    )

    # No relevant chunks found
    if not results:
        return {
            "question": request.question,
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "context": [],
        }

    # Build context with metadata
    context_parts = []

    for result in results:

        metadata = result["metadata"]

        context_parts.append(
            f"""Source: {metadata['filename']}
Page: {metadata['page_number']}
Chunk: {metadata['chunk_number']}

{result['text']}"""
        )

    context = "\n\n------------------------\n\n".join(
        context_parts
    )

    # Generate answer
    answer = generate_answer(
        request.question,
        context,
    )

    return {
        "question": request.question,
        "answer": answer,
        "context": results,
    }