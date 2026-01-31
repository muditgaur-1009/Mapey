# URGENT FIX - PyTorch/TorchVision Version Mismatch

## The Problem
You're getting: `RuntimeError: operator torchvision::nms does not exist`

This happens when PyTorch and TorchVision versions are incompatible. They MUST be installed together from the same source.

## Quick Fix (Run This Now)

```bash
cd backend
venv\Scripts\activate  # Windows

# Uninstall incompatible versions
pip uninstall -y torch torchvision transformers sentence-transformers

# Install compatible versions TOGETHER
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Verify installation
python -c "import torch; import torchvision; print(f'PyTorch: {torch.__version__}, TorchVision: {torchvision.__version__}')"

# Reinstall transformers and sentence-transformers
pip install transformers>=4.30.0
pip install sentence-transformers==2.2.2

# Test
python -c "from sentence_transformers import SentenceTransformer; print('✅ Success!')"
```

## Or Use the Fix Script

```bash
cd backend
fix_dependencies.bat
```

## Why This Happens

When you install PyTorch and TorchVision separately or from different sources, they can have incompatible compiled operators. They must be installed together from the same PyTorch repository.

## After Fix

Restart your server:
```bash
uvicorn app.main:app --reload
```

The error should be resolved!
