# Installation Troubleshooting Guide

## Common Installation Issues

### ModuleNotFoundError: Could not import module 'PreTrainedModel'

This error occurs when `sentence-transformers` dependencies are missing or incompatible.

#### Solution 1: Reinstall Dependencies (Recommended)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Uninstall problematic packages
pip uninstall sentence-transformers transformers torch -y

# Reinstall with explicit versions
pip install torch>=2.0.0
pip install transformers>=4.30.0
pip install sentence-transformers==2.2.2
pip install faiss-cpu==1.7.4
```

#### Solution 2: Clean Install

```bash
cd backend

# Remove virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Create new virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements.txt
```

#### Solution 3: Install PyTorch Separately (CPU Version)

If you're on a CPU-only system or want a lighter installation:

```bash
# For CPU-only (recommended for most systems)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then install other dependencies
pip install transformers>=4.30.0 sentence-transformers==2.2.2 faiss-cpu==1.7.4
```

#### Solution 4: GPU Support (Optional)

If you have an NVIDIA GPU with CUDA:

```bash
# Check CUDA version first
nvidia-smi

# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Then install other dependencies
pip install transformers>=4.30.0 sentence-transformers==2.2.2
# Note: Use faiss-gpu if you have GPU
pip install faiss-gpu==1.7.4
```

### FAISS Installation Issues (Windows)

On Windows, FAISS can sometimes fail to install.

#### Solution:

```bash
# Option 1: Install pre-built wheel
pip install faiss-cpu --no-cache-dir

# Option 2: Use conda (if available)
conda install -c conda-forge faiss-cpu

# Option 3: Build from source (advanced)
# Follow instructions at: https://github.com/facebookresearch/faiss
```

### Out of Memory Errors

If you get memory errors when loading the embedding model:

1. **Use a smaller model:**
   - Edit `backend/.env`:
   ```env
   EMBED_MODEL_NAME=all-MiniLM-L6-v2
   ```
   This is already the default and is the smallest model.

2. **Reduce batch size:**
   - The code already uses `show_progress_bar=False` to reduce memory usage.
   - You can modify `vector_store.py` to process texts in smaller batches.

3. **Check available memory:**
   ```bash
   # Linux/Mac
   free -h
   
   # Windows
   wmic OS get TotalVisibleMemorySize,FreePhysicalMemory
   ```

### Version Conflicts

If you see version conflict errors:

```bash
# Check current versions
pip list | grep -E "torch|transformers|sentence-transformers"

# Create a fresh environment
python -m venv venv_fresh
source venv_fresh/bin/activate  # or venv_fresh\Scripts\activate on Windows

# Install exact versions that work together
pip install torch==2.1.0
pip install transformers==4.35.0
pip install sentence-transformers==2.2.2
pip install faiss-cpu==1.7.4
```

### Slow Model Download

The embedding model (`all-MiniLM-L6-v2`) downloads automatically on first use (~80MB). If download is slow:

1. **Pre-download the model:**
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

2. **Use a local cache:**
   ```bash
   # Set cache directory (optional)
   export TRANSFORMERS_CACHE=/path/to/cache
   ```

### Verify Installation

Test that everything works:

```python
# Test script
python -c "
from sentence_transformers import SentenceTransformer
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['Hello world'])
print(f'Model loaded successfully. Embedding shape: {embeddings.shape}')
"
```

## System-Specific Notes

### Windows
- Use `pip install torch --index-url https://download.pytorch.org/whl/cpu` for CPU version
- May need Visual C++ Redistributables for some packages
- Use PowerShell or Command Prompt with Administrator privileges if needed

### Linux
- May need: `sudo apt-get install build-essential python3-dev`
- Some distributions may require `pip3` instead of `pip`

### macOS
- May need Xcode Command Line Tools: `xcode-select --install`
- Apple Silicon (M1/M2): PyTorch should work natively, but check compatibility

## Getting Help

If issues persist:

1. Check the logs in `backend/logs/app.log`
2. Verify Python version: `python --version` (should be 3.11+)
3. Check pip version: `pip --version` (upgrade if < 23.0)
4. Create an issue with:
   - Python version
   - OS and architecture
   - Full error traceback
   - Output of `pip list`
