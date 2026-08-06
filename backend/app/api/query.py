from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embeddings import get_embeddings
from app.rag.hybrid_retriever import retrieve
from app.services.llm import generate_answer
from app.services.query_rewriter import rewrite_query
from app.services.logger import log_query

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    history: list = []


@router.post("/query")
async def query(request: QueryRequest):

    # Rewrite follow-up question
    rewritten_question = rewrite_query(
        request.question,
        request.history,
    )

    print(f"\nOriginal Question: {request.question}")
    print(f"Rewritten Question: {rewritten_question}\n")

    # Create embedding
    query_embedding = get_embeddings(
        [rewritten_question]
    )[0]

    # Hybrid retrieval
    results = retrieve(
        rewritten_question,
        query_embedding,
        top_k=5,
    )

    if not results:
        return {
            "question": request.question,
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "context": [],
        }

    # Build context
    context_parts = []

    for result in results:

        metadata = result["metadata"]

        context_parts.append(
            f"""
Source: {metadata['filename']}
Page: {metadata['page_number']}
Chunk: {metadata['chunk_number']}

{result['text']}
"""
        )

    context = "\n\n------------------------\n\n".join(
        context_parts
    )

    # Generate answer
    answer = generate_answer(
        request.question,
        context,
        request.history,
    )

    # Save log and get its timestamp
    timestamp = log_query(
        question=request.question,
        rewritten_question=rewritten_question,
        answer=answer,
        context=results,
    )

    return {
        "timestamp": timestamp,
        "question": request.question,
        "rewritten_question": rewritten_question,
        "answer": answer,
        "context": results,
    }