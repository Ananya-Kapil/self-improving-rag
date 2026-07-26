from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="Self-Improving RAG",
    description="A production-ready RAG system",
    version="1.0.0",
)

# Register API routers
app.include_router(health_router)
app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Self-Improving RAG API 🚀"
    }