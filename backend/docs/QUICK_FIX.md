# Quick Fix for ModuleNotFoundError

## The Problem
You're seeing: `ModuleNotFoundError: Could not import module 'PreTrainedModel'`

This happens because `transformers` and `torch` dependencies are not properly installed.

## Immediate Fix

Run these commands in your terminal:

```bash
cd backend

# Activate your virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install PyTorch (CPU version - recommended for most users)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install transformers
pip install transformers>=4.30.0

# Reinstall sentence-transformers
pip install --force-reinstall sentence-transformers==2.2.2

# Verify installation
python -c "from sentence_transformers import SentenceTransformer; print('✅ Success!')"
```

## Or Use the Fix Script

**Windows:**
```bash
cd backend
fix_dependencies.bat
```

**Linux/Mac:**
```bash
cd backend
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

## After Installation

Try starting the server again:
```bash
uvicorn app.main:app --reload
```

The app should now start successfully! The embedding model will download automatically on first use (~80MB).

## Still Having Issues?

1. Check Python version: `python --version` (should be 3.11+)
2. Verify pip is up to date: `pip install --upgrade pip`
3. See detailed troubleshooting: `INSTALLATION_TROUBLESHOOTING.md`
