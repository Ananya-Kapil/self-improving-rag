import uuid
import chromadb

# Tune this based on retrieval quality during testing.
MAX_DISTANCE = 2.0

client = chromadb.PersistentClient(path="data/embeddings")

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings, metadatas):
    """
    Store document chunks, embeddings, and metadata in ChromaDB.
    """

    # Safety check
    if not (
        len(chunks) == len(embeddings) == len(metadatas)
    ):
        raise ValueError(
            "Chunks, embeddings, and metadatas must have the same length."
        )

    # Clear old data before indexing a new document.
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\nStored {collection.count()} chunks.\n")


def search_chunks(query_embedding, n_results=5):
    """
    Retrieve the most relevant chunks and filter weak matches.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    print("\n========== RAW CHROMA RESULTS ==========")
    print(results)
    print("========================================\n")


    filtered_results = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]


    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance <= MAX_DISTANCE:
            filtered_results.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )


    # Sort results by relevance.
    # Lower distance means a better semantic match.
    filtered_results.sort(
        key=lambda x: x["distance"]
    )


    print("\n========== FILTERED RESULTS ==========")

    for result in filtered_results:
        print(result)

    print("======================================\n")


    return filtered_results