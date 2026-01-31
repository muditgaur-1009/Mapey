# 📁 Mapey Project Structure

Complete overview of the project structure and file organization.

## Root Directory

```
Roadmap/
├── backend/              # FastAPI backend application
├── frontend/             # Next.js frontend application
├── venv/                 # Python virtual environment (existing)
├── Mapeyv1.py           # Original Streamlit implementation (preserved)
├── README.md             # Main project documentation
├── SETUP_GUIDE.md        # Step-by-step setup instructions
├── PROJECT_STRUCTURE.md  # This file
├── start.sh              # Startup script (Linux/Mac)
├── start.bat             # Startup script (Windows)
└── .gitignore           # Git ignore rules
```

## Backend Structure (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   │
│   ├── api/                       # API layer
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py          # Health check endpoint
│   │       └── roadmap.py         # Roadmap generation endpoints
│   │
│   ├── core/                      # Core application configuration
│   │   ├── __init__.py
│   │   ├── config.py              # Environment configuration
│   │   └── logging.py             # Logging setup
│   │
│   ├── models/                    # Data models & schemas
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models for API
│   │
│   └── services/                  # Business logic layer
│       ├── __init__.py
│       ├── agents.py              # LangGraph agent workflows
│       ├── vector_store.py        # FAISS vector store service
│       └── file_processor.py      # File parsing utilities
│
├── logs/                          # Application logs (generated at runtime)
│   ├── app.log                    # All logs
│   └── errors.log                 # Error logs only
│
├── env.example                    # Environment variables template
├── requirements.txt               # Python dependencies
└── README.md                      # Backend-specific documentation
```

### Key Backend Files

- **`app/main.py`**: FastAPI application with middleware, error handlers, and route registration
- **`app/core/config.py`**: Centralized configuration using Pydantic Settings
- **`app/core/logging.py`**: Structured JSON logging with file handlers
- **`app/api/routes/roadmap.py`**: Main API endpoints for roadmap generation
- **`app/services/agents.py`**: LangGraph workflow with topic analyzer, skill gap agent, curriculum planner, etc.
- **`app/services/vector_store.py`**: FAISS-based vector store with persistence support

## Frontend Structure (`frontend/`)

```
frontend/
├── app/                           # Next.js App Router
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                   # Home page
│   └── globals.css                # Global styles & Tailwind
│
├── components/                    # React components
│   ├── Header.tsx                 # App header with API status
│   ├── RoadmapForm.tsx            # Input form component
│   ├── RoadmapResults.tsx         # Results display component
│   └── LoadingSpinner.tsx         # Loading state component
│
├── lib/                           # Utilities & business logic
│   ├── api.ts                     # API client with axios
│   └── store.ts                   # Zustand state management
│
├── types/                         # TypeScript type definitions
│   └── api.ts                     # API request/response types
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── next.config.js                 # Next.js configuration
├── package.json                   # Node.js dependencies
├── postcss.config.js              # PostCSS configuration
├── tailwind.config.js             # TailwindCSS configuration
├── tsconfig.json                  # TypeScript configuration
└── README.md                      # Frontend-specific documentation
```

### Key Frontend Files

- **`app/page.tsx`**: Main application page with form and results layout
- **`components/RoadmapForm.tsx`**: Form with file upload and text input options
- **`components/RoadmapResults.tsx`**: Markdown renderer for roadmap results
- **`lib/api.ts`**: Centralized API client with error handling and interceptors
- **`lib/store.ts`**: Global state management for roadmap data

## Architecture Overview

### Backend Architecture

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│ Routes │ │Middleware│
└───┬───┘ └─────────┘
    │
┌───▼────────┐
│  Services  │
│  - Agents  │
│  - Vector  │
│  - Files   │
└────────────┘
```

### Frontend Architecture

```
┌──────────────────┐
│  Next.js App     │
│  (App Router)    │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│ Pages │ │Components│
└───┬───┘ └─────────┘
    │
┌───▼────────┐
│   Store    │
│ (Zustand)  │
└─────┬──────┘
      │
┌─────▼─────┐
│  API      │
│  Client   │
└───────────┘
```

## Data Flow

1. **User Input** → Frontend Form (`RoadmapForm.tsx`)
2. **API Request** → API Client (`lib/api.ts`)
3. **HTTP Request** → FastAPI Backend (`app/main.py`)
4. **Route Handler** → Roadmap Route (`app/api/routes/roadmap.py`)
5. **Business Logic** → Services (`app/services/`)
   - File Processing → Vector Store
   - LangGraph Agents → Roadmap Generation
6. **Response** → JSON Response → Frontend
7. **State Update** → Zustand Store → UI Update

## Environment Variables

### Backend (`backend/.env`)

See `backend/env.example` for all available variables.

Key variables:
- `TAVILY_API_KEY`: Web search API key
- `OLLAMA_BASE_URL`: Ollama server URL
- `LOG_LEVEL`: Logging verbosity
- `CORS_ORIGINS`: Allowed frontend origins

### Frontend (`frontend/.env.local`)

- `NEXT_PUBLIC_API_URL`: Backend API URL

## Logging

Logs are stored in `backend/logs/`:
- `app.log`: All application logs
- `errors.log`: Error-level logs only

Log format: JSON (production) or text (development)

## Generated Files

These files/directories are created at runtime:
- `backend/logs/`: Log files
- `frontend/.next/`: Next.js build cache
- `frontend/node_modules/`: Node.js dependencies
- `backend/venv/`: Python virtual environment (if created)

## Dependencies

### Backend (`requirements.txt`)
- FastAPI, Uvicorn
- LangChain, LangGraph
- FAISS, Sentence Transformers
- Pydantic, Pydantic Settings
- Tavily, PyPDF

### Frontend (`package.json`)
- Next.js 14
- React 18
- TypeScript
- TailwindCSS
- Zustand, Axios
- React Dropzone, React Markdown

## Development Workflow

1. **Backend Development:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload
   ```

2. **Frontend Development:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Full Stack:**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   ./start.sh
   ```

## Production Considerations

- **Backend**: Use Gunicorn with Uvicorn workers
- **Frontend**: Build static assets with `npm run build`
- **Logging**: Ensure log rotation is configured
- **Monitoring**: Set up APM tools for production
- **Security**: Use environment variables for secrets, enable HTTPS
- **Scaling**: Consider horizontal scaling for backend API
