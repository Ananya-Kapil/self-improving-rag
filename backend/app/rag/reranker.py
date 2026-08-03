from sentence_transformers import CrossEncoder

# Load once when the backend starts
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, results, top_k=5):
    """
    Rerank retrieved chunks using a CrossEncoder.
    """

    if not results:
        return []

    pairs = [
        (query, result["text"])
        for result in results
    ]

    scores = reranker.predict(pairs)

    for result, score in zip(results, scores):
        result["rerank_score"] = float(score)

    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    print("\n===== RERANKED RESULTS =====")

    for i, result in enumerate(results, start=1):
        page = result["metadata"]["page_number"]
        chunk = result["metadata"]["chunk_number"]

        print(
            f"{i}. "
            f"Page {page} "
            f"Chunk {chunk} "
            f"Score={result['rerank_score']:.4f}"
        )

    print("============================\n")

    return results[:top_k]