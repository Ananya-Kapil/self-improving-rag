
from app.rag.vector_store import search_chunks
from app.rag.bm25 import bm25_search
from app.rag.reranker import rerank
from app.services.feedback_scorer import load_feedback_scores


def retrieve(query, query_embedding, top_k=5):
    """
    Hybrid Retrieval Pipeline

    1. Retrieve semantic + BM25 candidates
    2. Fuse both retrieval methods
    3. Apply feedback-based score adjustment
    4. Cross-encoder reranks the candidates
    5. Return the best top_k chunks

    Feedback:
    Positive feedback boosts a chunk.
    Negative feedback penalizes a chunk.
    """

    semantic_results = search_chunks(
        query_embedding,
        n_results=10,
    )

    keyword_results = bm25_search(
        query,
        top_k=10,
    )

    fused = {}

    # ---------------- Semantic Retrieval ----------------

    for result in semantic_results:

        key = (
            result["metadata"]["filename"],
            result["metadata"]["page_number"],
            result["metadata"]["chunk_number"],
        )

        similarity = max(
            0,
            2.0 - result["distance"],
        ) / 2.0

        fused[key] = {
            "text": result["text"],
            "metadata": result["metadata"],
            "score": similarity * 0.7,
        }

    # ---------------- BM25 Retrieval ----------------

    if keyword_results:

        max_score = max(
            r["score"] for r in keyword_results
        )

        if max_score > 0:

            for result in keyword_results:

                key = (
                    result["metadata"]["filename"],
                    result["metadata"]["page_number"],
                    result["metadata"]["chunk_number"],
                )

                normalized = result["score"] / max_score

                if key in fused:

                    fused[key]["score"] += normalized * 0.3

                else:

                    fused[key] = {
                        "text": result["text"],
                        "metadata": result["metadata"],
                        "score": normalized * 0.3,
                    }

    # ---------------- Feedback Adjustment ----------------

    feedback_scores = load_feedback_scores()

    for key, result in fused.items():

        feedback = feedback_scores.get(key, 0)

        # Small adjustment so feedback helps without
        # overpowering semantic/BM25 retrieval.
        result["score"] += feedback * 0.05

    # ---------------- Sort Fused Results ----------------

    fused_results = sorted(
        fused.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    print("\n===== FUSED RESULTS =====")

    for i, result in enumerate(
        fused_results,
        start=1,
    ):

        print(
            f"{i}. "
            f"{result['metadata']['filename']} | "
            f"Page {result['metadata']['page_number']} "
            f"Chunk {result['metadata']['chunk_number']} "
            f"Fusion={result['score']:.3f}"
        )

    print("=========================\n")

    # ---------------- Cross-Encoder Reranking ----------------

    final_results = rerank(
        query,
        fused_results,
        top_k=top_k,
    )

    return final_results

