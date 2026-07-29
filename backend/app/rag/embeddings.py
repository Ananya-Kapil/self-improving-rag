from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Convert a single text into an embedding.
    """
    return model.encode(text).tolist()


def get_embeddings(texts: list[str]):
    """
    Convert multiple texts into embeddings.
    """
    return model.encode(texts).tolist()