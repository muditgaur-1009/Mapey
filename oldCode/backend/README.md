# Mapey Backend API

Production-grade FastAPI backend for career roadmap generation.

## Features

- ✅ FastAPI with async/await support
- ✅ Structured JSON logging
- ✅ Comprehensive error handling
- ✅ Request/response validation with Pydantic
- ✅ CORS middleware
- ✅ File upload handling
- ✅ Vector store with FAISS
- ✅ LangGraph agent workflows
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Web search integration (Tavily)

## API Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with custom config
uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
```

## Production Deployment

```bash
# Using Uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn (recommended for production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/        # API route handlers
│   ├── core/
│   │   ├── config.py      # Configuration management
│   │   └── logging.py     # Logging setup
│   ├── models/
│   │   └── schemas.py     # Pydantic models
│   ├── services/
│   │   ├── agents.py      # LangGraph agents
│   │   ├── vector_store.py # FAISS vector store
│   │   └── file_processor.py # File processing
│   └── main.py            # FastAPI app
├── logs/                  # Application logs
└── requirements.txt       # Dependencies
```
