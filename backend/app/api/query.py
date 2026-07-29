from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embeddings import get_embeddings
from app.rag.vector_store import search_chunks
from app.services.llm import generate_answer

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query(request: QueryRequest):

    # Convert question into embedding
    query_embedding = get_embeddings([request.question])[0]

    # Search ChromaDB
    results = search_chunks(query_embedding, n_results=3)

    # Extract text chunks
    context = "\n\n".join(results["documents"][0])

    # Generate answer
    answer = generate_answer(request.question, context)

    return {
        "question": request.question,
        "answer": answer,
        "context": results["documents"][0]
    }