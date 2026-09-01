# Self-Improving RAG 🚀

A Retrieval-Augmented Generation (RAG) system that uses **hybrid retrieval, reranking, query rewriting, and user feedback** to improve future retrieval results.

## Features

* 📄 PDF/document upload
* ✂️ Text chunking and filtering
* 🔎 Semantic/vector retrieval
* 🔤 BM25 keyword retrieval
* 🔀 Hybrid retrieval
* 🎯 Cross-encoder reranking
* ✏️ Query rewriting
* 👍 Positive / 👎 negative feedback
* 🧠 Feedback-based retrieval improvement
* 📊 Retrieval and feedback analytics
* 🧪 Automated backend tests
* 🐳 Docker support for frontend and backend

## How Self-Improvement Works

The system records user feedback for retrieved chunks.

```text
User Query
    ↓
Query Rewriting
    ↓
Semantic Retrieval + BM25
    ↓
Hybrid Score Fusion
    ↓
Feedback Score Adjustment
    ↓
Cross-Encoder Reranking
    ↓
Final Context
    ↓
LLM Answer
    ↓
User Feedback
    └──────────────→ Future Retrieval
```

Positive feedback gives a chunk a positive score, while negative feedback gives it a negative score.

Feedback is associated with:

```text
(filename, page, chunk)
```

This allows the system to learn which retrieved chunks have historically been useful.

## Architecture

```text
Frontend (React + Vite)
        │
        ▼
FastAPI Backend
        │
        ├── Upload API
        │      └── Document processing
        │
        ├── Query API
        │      ├── Query rewriting
        │      ├── Vector retrieval
        │      ├── BM25 retrieval
        │      ├── Feedback adjustment
        │      └── Reranking
        │
        ├── Feedback API
        │
        └── Analytics API
```

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* LangChain text splitters
* ChromaDB
* Sentence Transformers
* BM25
* Cross-encoder reranking

### Frontend

* React
* Vite
* JavaScript

### Infrastructure

* Docker
* Docker Compose

## Project Structure

```text
Self-improving RAG/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── analytics.py
│   │   │   ├── feedback.py
│   │   │   ├── health.py
│   │   │   ├── query.py
│   │   │   └── upload.py
│   │   │
│   │   ├── rag/
│   │   │   ├── bm25.py
│   │   │   ├── embeddings.py
│   │   │   ├── hybrid_retriever.py
│   │   │   ├── reranker.py
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   │
│   │   ├── services/
│   │   │   ├── feedback_analyzer.py
│   │   │   ├── feedback_scorer.py
│   │   │   ├── llm.py
│   │   │   ├── logger.py
│   │   │   └── query_rewriter.py
│   │   │
│   │   └── utils/
│   │       ├── text_filter.py
│   │       └── text_splitter.py
│   │
│   ├── tests/
│   ├── data/
│   ├── requirements.txt
│   └── dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Self-improving RAG"
```

### 2. Backend environment

Create:

```text
backend/.env
```

Add the required API key:

```env
OPENROUTER_API_KEY=your_api_key
```

Do not commit `.env` to Git.

### 3. Start the backend

```powershell
cd backend
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### 4. Start the frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## Docker Setup

From the project root:

```powershell
docker compose build
docker compose up
```

The services will be available at:

```text
Frontend: http://localhost:5173
Backend:  http://localhost:8000
```

To stop the containers:

```powershell
docker compose down
```

## Testing

From the project root:

```powershell
$env:PYTHONPATH="backend"
pytest backend/tests -v
```

The test suite covers core backend functionality including feedback scoring, feedback analytics, and query rewriting.

## API Endpoints

| Endpoint         | Purpose                           |
| ---------------- | --------------------------------- |
| `GET /`          | API welcome message               |
| `POST /upload`   | Upload/process documents          |
| `POST /query`    | Ask questions using RAG           |
| `POST /feedback` | Submit user feedback              |
| `GET /analytics` | View feedback/retrieval analytics |

FastAPI also provides interactive API documentation at:

```text
http://localhost:8000/docs
```

## Analytics

The analytics dashboard tracks metrics such as:

* Total queries
* Positive feedback
* Negative feedback
* Feedback rate
* Helpfulness rate
* Feedback chunks
* Positive/negative chunks
* Most retrieved pages

## Current Limitations

* Feedback learning is currently score-based rather than model fine-tuning.
* Feedback is derived from user interactions with retrieved context.
* The system currently focuses on retrieval improvement rather than retraining the underlying embedding or language models.

## Future Improvements

Possible future improvements include:

* More sophisticated feedback weighting
* Evaluation datasets and retrieval benchmarks
* Automated retrieval quality monitoring
* Better handling of conflicting feedback
* Persistent feedback databases
* Authentication and user-specific feedback
* Improved frontend UX

## Status

The core RAG pipeline, feedback-based self-improvement, analytics, automated tests, and Docker deployment are implemented.

## Author

**Ananya**


If you found this project useful, consider giving the repository a star ⭐
