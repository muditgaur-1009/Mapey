@echo off
REM Quick fix script for dependency issues on Windows

echo Fixing Mapey Backend Dependencies...
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Uninstall problematic packages
echo Cleaning up existing packages...
pip uninstall -y sentence-transformers transformers torch torchvision 2>nul

REM Install PyTorch (CPU version) - CRITICAL: must install together for compatibility
echo Installing PyTorch (CPU version) with compatible torchvision...
echo IMPORTANT: PyTorch and TorchVision MUST be installed together from same source!
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

REM Verify PyTorch installation
echo Verifying PyTorch installation...
python -c "import torch; import torchvision; print(f'PyTorch: {torch.__version__}, TorchVision: {torchvision.__version__}')" || (
    echo ERROR: PyTorch installation failed! Please check the error above.
    pause
    exit /b 1
)

REM Install transformers and sentence-transformers
echo Installing transformers and sentence-transformers...
pip install transformers>=4.30.0 --no-cache-dir
pip install --force-reinstall sentence-transformers==2.2.2 --no-cache-dir

REM Final verification
echo Testing sentence-transformers import...
python -c "from sentence_transformers import SentenceTransformer; print('✅ All dependencies installed successfully!')" || (
    echo ERROR: sentence-transformers test failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

REM Install FAISS
echo Installing FAISS...
pip install faiss-cpu==1.7.4

REM Install remaining dependencies
echo Installing remaining dependencies...
pip install -r requirements.txt

echo.
echo ======================================
echo Dependencies fixed!
echo Test the installation with:
echo   python -c "from sentence_transformers import SentenceTransformer; print('OK')"
echo.

pause
