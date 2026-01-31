# Backend (FastAPI) Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed (for faiss, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements*.txt ./

# Use clean requirements (no torch), then fallback options
RUN if [ -f requirements-clean.txt ]; then \
        pip install --no-cache-dir -r requirements-clean.txt; \
    elif [ -f requirements-314.txt ]; then \
        pip install --no-cache-dir -r requirements-314.txt; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
