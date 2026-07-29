from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
from app.utils.text_splitter import chunk_text
from app.rag.embeddings import get_embeddings
from app.rag.vector_store import store_chunks
import os

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    extracted_text = ""

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        print(f"\n----- PAGE {i+1} -----")
        print(repr(text))

        if text:
            extracted_text += text + "\n"

    # Split into chunks
    chunks = chunk_text(extracted_text)

    # Generate embeddings
    embeddings = get_embeddings(chunks)

    # Store in ChromaDB
    store_chunks(chunks, embeddings)

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "characters": len(extracted_text),
        "chunks": len(chunks),
        "message": "Document indexed successfully!"
    }