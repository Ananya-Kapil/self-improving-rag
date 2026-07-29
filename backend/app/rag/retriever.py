from sentence_transformers import SentenceTransformer
from app.rag.vector_store import collection

# Load the same embedding model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query: str, top_k: int = 3):
    """
    Retrieve the most relevant document chunks from ChromaDB.
    """

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results["documents"][0]