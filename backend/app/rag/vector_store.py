import uuid
import chromadb

client = chromadb.PersistentClient(path="data/embeddings")

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings):
    """
    Store document chunks in ChromaDB.
    """

    # Clear old data before indexing a new document
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
    )

    print(f"\nStored {collection.count()} chunks.\n")


def search_chunks(query_embedding, n_results=5):
    """
    Search for the most relevant chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances"],
    )

    print("\n========== CHROMA RESULTS ==========")
    print(results)
    print("====================================\n")

    return results