from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app = FastAPI(
    title="Self-Improving RAG API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Self-Improving RAG API 🚀"}

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(query_router)