from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
import os

from app.utils.text_splitter import chunk_text
from app.utils.text_filter import should_skip_chunk
from app.rag.embeddings import get_embeddings
from app.rag.vector_store import store_chunks
from app.rag.bm25 import build_bm25_index

router = APIRouter()

UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename,
    )

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    all_chunks = []
    all_metadatas = []

    # Extract text page by page
    for page_num, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text or not text.strip():
            continue

        page_chunks = chunk_text(text)

        for chunk_num, chunk in enumerate(page_chunks, start=1):

            chunk = chunk.strip()

            if should_skip_chunk(chunk):
                continue

            all_chunks.append(chunk)

            all_metadatas.append(
                {
                    "filename": file.filename,
                    "page_number": page_num,
                    "chunk_number": chunk_num,
                }
            )

    print("\n========== CHUNKS ==========")
    print(f"Total valid chunks: {len(all_chunks)}")

    for i, chunk in enumerate(all_chunks[:5]):
        print(f"\nChunk {i + 1}")
        print("-" * 40)
        print(chunk[:300])

    print("============================")

    # Generate embeddings
    embeddings = get_embeddings(all_chunks)

    print(
        f"\nGenerated {len(embeddings)} embeddings"
    )

    # Store chunks with metadata
    store_chunks(
        all_chunks,
        embeddings,
        all_metadatas,
    )

    # Build BM25 index
    build_bm25_index(
        all_chunks,
        all_metadatas,
    )

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "chunks": len(all_chunks),
        "message": "Document indexed successfully!",
    }