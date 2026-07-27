from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Convert a text chunk into a vector embedding.
    """
    return model.encode(text).tolist()


def get_embeddings(texts: list[str]):
    """
    Convert multiple text chunks into vector embeddings.
    """
    return model.encode(texts).tolist()