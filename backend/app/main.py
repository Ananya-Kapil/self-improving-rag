from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.api.feedback import router as feedback_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Self-Improving RAG API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(query_router)
app.include_router(feedback_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Self-Improving RAG API 🚀"
    }