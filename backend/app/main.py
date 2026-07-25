from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to the Self-Improving RAG API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
