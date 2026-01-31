# 🚀 Mapey Setup Guide

Complete step-by-step guide to set up and run the Mapey application.

## Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Node.js 18+**
   ```bash
   node --version  # Should be 18 or higher
   npm --version
   ```

3. **Ollama** (for LLM)
   - Download from: https://ollama.ai
   - Install and ensure it's running:
   ```bash
   ollama serve
   ```
   - Pull the required model:
   ```bash
   ollama pull llama3.2:1b
   ```

4. **Tavily API Key** (optional, for web search)
   - Sign up at: https://tavily.com
   - Get your API key from the dashboard

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This may take a few minutes as it installs ML libraries (PyTorch, transformers, etc.).

**If you encounter `ModuleNotFoundError: Could not import module 'PreTrainedModel'`:**

Use the quick fix script:
```bash
# Windows
fix_dependencies.bat

# Linux/Mac
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

Or manually fix:
```bash
pip install --upgrade pip setuptools wheel
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers>=4.30.0 sentence-transformers==2.2.2
pip install -r requirements.txt
```

See `backend/INSTALLATION_TROUBLESHOOTING.md` for detailed troubleshooting.

### Step 4: Configure Environment Variables

Create a `.env` file in the `backend/` directory:

**Windows:**
```bash
copy env.example .env
```

**Linux/Mac:**
```bash
cp env.example .env
```

Edit `.env` and update these values:
- `TAVILY_API_KEY`: Your Tavily API key (if you have one)
- `OLLAMA_BASE_URL`: Default is `http://localhost:11434`
- `CORS_ORIGINS`: Add your frontend URLs

### Step 5: Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Verify it's working:
- Open browser: http://localhost:8000/docs
- You should see the Swagger API documentation

## Frontend Setup

### Step 1: Navigate to Frontend Directory

Open a new terminal window:

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure Environment Variables

Create `.env.local` file:

```bash
# Windows
copy .env.example .env.local

# Linux/Mac
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Start the Development Server

```bash
npm run dev
```

You should see:
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
```

Open http://localhost:3000 in your browser.

## Quick Start Scripts

### Windows

Double-click `start.bat` or run:
```bash
start.bat
```

This will start both backend and frontend in separate windows.

### Linux/Mac

Make the script executable and run:
```bash
chmod +x start.sh
./start.sh
```

## Verification

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/api/v1/health/
   ```
   Should return: `{"status":"healthy","version":"1.0.0","service":"Mapey Roadmap API"}`

2. **Frontend:**
   - Open http://localhost:3000
   - Check if "API Online" status is green in the header

3. **Test Roadmap Generation:**
   - Enter a target role (e.g., "ML Engineer")
   - Upload a resume (PDF or TXT)
   - Optionally add a job description
   - Click "Generate Roadmap"
   - Wait for the AI agents to process (may take 1-2 minutes)

## Troubleshooting

### Backend Issues

**Issue: Module not found errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Ollama connection error**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

**Issue: Port 8000 already in use**
```bash
# Change port in .env or use different port
uvicorn app.main:app --port 8001
```

### Frontend Issues

**Issue: API connection failed**
- Check if backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

**Issue: Build errors**
```bash
# Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run dev
```

**Issue: TypeScript errors**
```bash
npm run type-check
```

### Common Issues

**Vector Store Errors:**
- If FAISS installation fails on Windows, try:
  ```bash
  pip install faiss-cpu --no-cache-dir
  ```

**Memory Issues:**
- The embedding model loads into memory. Ensure you have at least 2GB RAM available.
- For lower-end machines, reduce `OLLAMA_NUM_CTX` in `.env`

**Slow Generation:**
- Roadmap generation can take 1-3 minutes depending on:
  - LLM response time
  - Network speed (for web search)
  - System resources
- Be patient, especially on first run

## Production Deployment

### Backend

1. Set `DEBUG=false` in `.env`
2. Use a production ASGI server:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```
3. Use a reverse proxy (nginx) for SSL and routing
4. Set up process management (systemd, PM2, etc.)

### Frontend

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Start production server:
   ```bash
   npm start
   ```
3. Or deploy to Vercel/Netlify:
   ```bash
   vercel deploy
   ```

## Next Steps

- Read the main [README.md](README.md) for architecture details
- Check [backend/README.md](backend/README.md) for API documentation
- Review [frontend/README.md](frontend/README.md) for frontend details

## Support

If you encounter issues:
1. Check the logs in `backend/logs/`
2. Review browser console errors
3. Verify all environment variables are set correctly
4. Ensure all prerequisites are installed and running
