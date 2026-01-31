#!/bin/bash
# Quick fix script for dependency issues

echo "Fixing Mapey Backend Dependencies..."
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Uninstall problematic packages
echo "Cleaning up existing packages..."
pip uninstall -y sentence-transformers transformers torch torchvision 2>/dev/null || true

# Install PyTorch (CPU version)
echo "Installing PyTorch (CPU version)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install transformers and sentence-transformers
echo "Installing transformers and sentence-transformers..."
pip install transformers>=4.30.0
pip install sentence-transformers==2.2.2

# Install FAISS
echo "Installing FAISS..."
pip install faiss-cpu==1.7.4

# Install remaining dependencies
echo "Installing remaining dependencies..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "Dependencies fixed!"
echo "Test the installation with:"
echo "  python -c \"from sentence_transformers import SentenceTransformer; print('OK')\""
echo ""
