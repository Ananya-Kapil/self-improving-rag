import chromadb


client = chromadb.PersistentClient(path="data/embeddings")


collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings):
    """
    Store text chunks and their embeddings in ChromaDB.
    """

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )


def search_chunks(query_embedding, n_results=5):
    """
    Search for the most relevant chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results