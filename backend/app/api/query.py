
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.rag.embeddings import get_embeddings
from app.rag.hybrid_retriever import retrieve
from app.services.llm import generate_answer
from app.services.query_rewriter import rewrite_query
from app.services.logger import log_query
from app.services.feedback_scorer import load_feedback_scores

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    history: list = Field(default_factory=list)


@router.post("/query")
async def query(request: QueryRequest):

    # -----------------------------
    # Query rewriting
    # -----------------------------
    print("\n===== QUERY REWRITING =====")
    print(f"Original Question: {request.question}")
    print(f"History Received: {request.history}")

    rewritten_question = rewrite_query(
        request.question,
        request.history,
    )

    print(f"Rewritten Question: {rewritten_question}")
    print("===========================\n")

    # -----------------------------
    # Create embedding
    # -----------------------------
    query_embedding = get_embeddings(
        [rewritten_question]
    )[0]

    # -----------------------------
    # Hybrid retrieval
    # -----------------------------
    results = retrieve(
        rewritten_question,
        query_embedding,
        top_k=5,
    )

    if not results:
        return {
            "question": request.question,
            "rewritten_question": rewritten_question,
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "context": [],
        }

    # -----------------------------
    # Apply feedback learning
    # -----------------------------
    feedback_scores = load_feedback_scores()

    for result in results:

        metadata = result["metadata"]

        key = (
            metadata["filename"],
            metadata["page_number"],
            metadata["chunk_number"],
        )

        feedback_score = feedback_scores.get(key, 0)

        result["feedback_score"] = feedback_score

        result["score"] += feedback_score

    # Sort after feedback boost
    results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    print("\n===== SELF-IMPROVED RANKING =====")

    for i, result in enumerate(results, start=1):

        metadata = result["metadata"]

        print(
            f"{i}. "
            f"Page {metadata['page_number']} "
            f"Chunk {metadata['chunk_number']} "
            f"Score={result['score']:.3f} "
            f"Feedback={result['feedback_score']}"
        )

    print("===============================\n")

    # -----------------------------
    # Build context
    # -----------------------------
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

    # -----------------------------
    # Generate answer
    # -----------------------------
    answer = generate_answer(
        request.question,
        context,
        request.history,
    )

    # -----------------------------
    # Save log
    # -----------------------------
    timestamp = log_query(
        question=request.question,
        rewritten_question=rewritten_question,
        answer=answer,
        context=results,
    )

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "timestamp": timestamp,
        "question": request.question,
        "rewritten_question": rewritten_question,
        "answer": answer,
        "context": results,
    }
