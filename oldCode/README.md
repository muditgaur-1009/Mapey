# 🧠 Mapey - AI Career Roadmap Generator

A production-grade application that generates personalized career roadmaps using AI agents, LangGraph, RAG, and vector search.

## 🏗️ Architecture

- **Backend**: FastAPI with async support, structured logging, and comprehensive error handling
- **Frontend**: Next.js 14 with TypeScript, TailwindCSS, and modern UI/UX
- **AI/ML**: LangGraph for agent workflows, LangChain, Ollama LLM, FAISS vector store
- **Features**: RAG (Retrieval Augmented Generation), web search integration (Tavily), file processing

## 📁 Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Route handlers
│   │   ├── core/           # Core configuration & logging
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── logs/               # Application logs (generated)
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
└── frontend/               # Next.js frontend
    ├── app/                # Next.js app directory
    ├── components/         # React components
    ├── lib/                # Utilities & API client
    ├── types/              # TypeScript types
    └── package.json        # Node dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama installed and running (for LLM)
- Tavily API key (optional, for web search)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the API server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   API will be available at: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local if API URL is different
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:3000`

## ⚙️ Configuration

### Backend Environment Variables

```env
# API Settings
API_V1_PREFIX=/api/v1
PROJECT_NAME=Mapey Roadmap API
VERSION=1.0.0
DEBUG=true

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# LLM Settings
OLLAMA_MODEL=llama3.2:1b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.4
OLLAMA_NUM_CTX=1048

# Tavily API Key (required for web search)
TAVILY_API_KEY=your_tavily_api_key_here

# Embedding Model
EMBED_MODEL_NAME=all-MiniLM-L6-v2

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Vector Store (optional)
VECTOR_STORE_INDEX_PATH=

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.pdf,.txt,.docx
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### Health Check
- `GET /api/v1/health/` - Check API health status

### Roadmap Generation
- `POST /api/v1/roadmap/generate` - Generate roadmap from file upload
  - Form data: `topic`, `resume_file`, `jd` (optional)
- `POST /api/v1/roadmap/generate-from-text` - Generate roadmap from text input
  - JSON body: `{ "topic": "...", "resume": "...", "jd": "..." }`

### Vector Store Management
- `GET /api/v1/roadmap/vector-store/stats` - Get vector store statistics
- `POST /api/v1/roadmap/vector-store/clear` - Clear vector store

## 🔧 Development

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black app/
flake8 app/
mypy app/

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

## 📊 Logging

The application uses structured JSON logging for production monitoring:

- **Location**: `backend/logs/`
- **Files**:
  - `app.log` - All application logs
  - `errors.log` - Error-level logs only
- **Format**: JSON (production) or text (development)
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🐳 Docker Support (Optional)

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🔐 Production Considerations

1. **Environment Variables**: Never commit `.env` files. Use secrets management.
2. **CORS**: Configure `CORS_ORIGINS` for your production domain.
3. **Rate Limiting**: Consider adding rate limiting middleware.
4. **Authentication**: Add authentication/authorization as needed.
5. **Database**: Consider persisting vector store and user data.
6. **Monitoring**: Set up APM tools (e.g., Sentry, DataDog).
7. **Scaling**: Use process managers (Gunicorn, Uvicorn workers) for production.

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
