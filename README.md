# 🚀 Mapey - AI-Powered Career Roadmap Generator

<div align="center">

![Mapey Logo](https://img.shields.io/badge/Mapey-Career_Roadmap_AI-red?style=for-the-badge)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)

**Generate personalized career roadmaps powered by AI**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

**Mapey** is an AI-powered career roadmap generator that analyzes your resume, compares it with your target role, and creates a personalized learning path. Using advanced LLM technology (Llama 3.2) and multi-agent workflows with **real-time progress tracking**, Mapey provides:

- 📊 **Skill Gap Analysis** - Understand what you need to learn
- 🎓 **Personalized Curriculum** - Step-by-step learning path
- 🔗 **Curated Resources** - Best courses, projects, and materials
- 📈 **Career Strategy** - Timeline and milestones for success
- ⚡ **Real-Time Progress** - Live updates with visual progress bar

## ✨ Features

### Core Capabilities

- **🤖 AI-Powered Analysis**
  - LangGraph 6-stage multi-agent workflow
  - Llama 3.2 (1B) local LLM via Ollama
  - FAISS vector store with RAG (Retrieval Augmented Generation)
  - Semantic search and web scraping (Tavily)

- **💼 Comprehensive Career Analysis**
  - Role breakdown and industry expectations
  - Skill gap identification
  - Multi-phase learning curriculum
  - Resource curation via web search
  - Interview preparation strategy

- **🎨 Modern UI/UX**
  - Responsive dark theme design
  - Smooth animations and transitions
  - Real-time toast notifications
  - Copy-to-clipboard functionality
  - Mobile, tablet, and desktop support

- **🔐 Security**
  - JWT authentication (HS256)
  - Secure API endpoints
  - Environment-based configuration
  - CORS protection

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (Python 3.14 recommended)
- **Docker & Docker Compose** (required)
- **Windows 10/11** or **Linux/macOS**
- **4GB RAM minimum** (8GB recommended)
- **10GB free disk space**
- **NVIDIA GPU** (optional but recommended for faster generation)
  - Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) for GPU support

### Installation (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/muditgaur-1009/mapey.git
   cd mapey
   ```

2. **Setup the project** (creates venv, installs dependencies, configures env files)
   ```powershell
   # Windows PowerShell
   python -m mapey setup
   ```

3. **Update your ENVs** (Clerk and Tavily)

4. **Start all services** (runs Docker containers for backend, frontend, and Ollama)
   ```powershell
   python -m mapey start
   ```

   This command will:
   - Start Docker Compose services
   - Pull Ollama models (nomic-embed-text, llama3.2:1b)
   - Initialize the backend
   - 🎮 **Use GPU automatically** if NVIDIA GPU is detected!

5. **Open the app!** 🎉
   ```
   Frontend: http://localhost:3000
   Backend API: http://localhost:8000
   API Docs: http://localhost:8000/docs
   ```

### First Roadmap Generation

1. Go to http://localhost:3000
2. Click **"Enter Text"** button
3. Fill in:
   - **Target Role**: "Python Backend Developer"
   - **Resume**: Paste your skills and experience
   - **Job Description** (optional): Paste a job posting
4. Click **"Generate Roadmap"**
5. Watch the **real-time progress bar!** (takes 3-5 minutes)
6. View your personalized roadmap! 🎊

### File Upload Alternative

You can also **upload a PDF/TXT resume** instead of pasting text:
1. Click **"Upload Resume"** button
2. Select your resume file
3. Fill in target role and job description
4. Click **"Generate Roadmap"**
5. Progress updates shown in results area

### How It Works

```
Frontend → SSE Connection → Backend
   ↓
Opens EventSource to /generate-from-text-stream
   ↓
Backend sends real-time updates:
  data: {"progress": 10, "step": "Analyzing..."}
  data: {"progress": 45, "step": "Skill gaps..."}
   ↓
Final Result delivered at 100%
```

### 6-Stage Workflow

1. **Topic Analyzer** (10-25%) - Analyzes target role and industry expectations
2. **Skill Gap Agent** (30-45%) - Compares resume with job requirements  
3. **Curriculum Planner** (50-60%) - Designs personalized learning path
4. **RAG Retriever** (60-65%) - Retrieves relevant context from experience
5. **Resource Curator** (70-80%) - Finds best learning resources via web search
6. **Validator** (85-100%) - Generates final comprehensive roadmap


## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Mapey Roadmap API"
}
```

#### 2. Generate Roadmap (Streaming with Progress) ⭐ NEW
```http
POST /roadmap/generate-from-text-stream
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "topic": "Python Backend Developer",
  "resume": "Your resume text here...",
  "jd": "Optional job description"
}
```

**Response:** Server-Sent Events (SSE)
```
data: {"progress": 10, "step": "Analyzing target role", "status": "processing"}
data: {"progress": 25, "step": "Topic analysis complete", "status": "processing"}
data: {"progress": 45, "step": "Skill gap analysis complete", "status": "processing"}
...
data: {"progress": 100, "step": "Complete", "status": "complete", "result": {...}}
```

#### 3. Generate Roadmap (Non-streaming)
```http
POST /roadmap/generate-from-text
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "topic": "Full Stack Developer",
  "resume": "Your resume...",
  "jd": "Job description..."
}
```

**Response:**
```json
{
  "roadmap": "Complete roadmap markdown...",
  "skill_gaps": "Skill gap analysis...",
  "curriculum": "Learning curriculum...",
  "resources": "Curated resources...",
  "analysis": "Role analysis...",
  "rag_context": "Retrieved context..."
}
```

#### 4. Vector Store Stats
```http
GET /roadmap/vector-store/stats
Authorization: Bearer <JWT_TOKEN>
```

### Authentication

Generate a JWT token:
```powershell
docker exec mapey-backend-1 python -c "import jwt; import time; print(jwt.encode({'sub': 'test-user', 'exp': int(time.time()) + 3600}, 'change-me', algorithm='HS256'))"
```

Use in requests:
```bash
Authorization: Bearer <your_jwt_token>
```

## 🧪 Testing

### Run Test Script
```powershell
.\test_api.ps1
```

Tests include:
- ✅ Health check
- ✅ JWT token generation
- ✅ Vector store stats
- ✅ Roadmap generation (full workflow)

### Manual API Testing
```powershell
# Generate token
$token = docker exec mapey-backend-1 python -c "import jwt; import time; print(jwt.encode({'sub': 'test-user', 'exp': int(time.time()) + 3600}, 'change-me', algorithm='HS256'))"

# Test streaming endpoint
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $token"
}

$body = @{
    topic = "Data Scientist"
    resume = "Sample resume text"
    jd = ""
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/roadmap/generate-from-text-stream" -Method Post -Body $body -Headers $headers
```


## 🐛 Troubleshooting

### Services won't start
```powershell
# Check Docker is running
docker ps

# Restart with Python command
python -m mapey start

# Or manually rebuild containers
docker-compose down -v
docker-compose up --build -d
```

### Models not found
```powershell
# Pull models again
docker exec mapey-ollama-1 ollama pull nomic-embed-text
docker exec mapey-ollama-1 ollama pull llama3.2:1b
docker-compose restart backend
```

### Slow generation
- Normal processing time: **3-5 minutes**
- Depends on hardware (CPU-based LLM)
- Check resource usage: `docker stats`
- First generation may be slower (model loading)


## 🌟 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM application framework
- **LangGraph** - Multi-agent workflow orchestration
- **Ollama** - Local LLM inference (Llama 3.2)
- **FAISS** - Vector similarity search
- **Tavily** - Web search API
- **Pydantic** - Data validation
- **PyJWT** - JWT authentication
- **Uvicorn** - ASGI server

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management
- **React Hot Toast** - Toast notifications
- **React Markdown** - Markdown rendering
- **Lucide React** - Icon library

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Node.js 20** - JavaScript runtime

## 📊 Performance

- **Generation Time**: 3-5 minutes (varies by hardware)
- **Memory Usage**: ~2GB RAM (with all services)
- **Disk Usage**: ~3GB (includes models)
- **CPU**: CPU-based LLM (no GPU required)
- **Concurrent Users**: Limited by CPU (single-threaded LLM)

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- **Ollama** - For local LLM infrastructure
- **LangChain** - For LLM application framework
- **Tavily** - For web search capabilities
- **FastAPI** - For the excellent Python web framework
- **Next.js** - For the powerful React framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/muditgaur-1009/mapey/issues)
- **Documentation**: See `/docs` folder

---

<div align="center">

**Made with ❤️ by Mudit Gaur**

⭐ Star this project on GitHub if you fonnd this helpful!

</div>

