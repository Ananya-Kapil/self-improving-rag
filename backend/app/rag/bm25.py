from rank_bm25 import BM25Okapi

bm25 = None

documents = []
metadatas = []


def build_bm25_index(chunks, metadata_list):
    """
    Build BM25 index from document chunks.
    """

    global bm25
    global documents
    global metadatas

    documents = chunks
    metadatas = metadata_list

    tokenized_docs = [
        chunk.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_docs)

    print(f"\nBuilt BM25 index with {len(chunks)} chunks.\n")


def bm25_search(query, top_k=5):
    """
    Keyword search using BM25.
    """

    global bm25
    global documents
    global metadatas

    if bm25 is None:
        return []

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []

    for idx, score in ranked[:top_k]:

        results.append(
            {
                "text": documents[idx],
                "metadata": metadatas[idx],
                "score": float(score),
            }
        )

    return results