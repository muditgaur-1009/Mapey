@echo off
REM Direct fix for PyTorch/TorchVision compatibility issue
REM Run this script from the backend directory

echo ========================================
echo FIXING PyTorch/TorchVision Compatibility
echo ========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo ERROR: Virtual environment not found! Please run this from the backend directory.
    pause
    exit /b 1
)

echo.
echo Step 1: Uninstalling incompatible packages...
pip uninstall -y torch torchvision transformers sentence-transformers 2>nul

echo.
echo Step 2: Installing compatible PyTorch and TorchVision TOGETHER...
echo (This may take a few minutes...)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

if errorlevel 1 (
    echo.
    echo ERROR: PyTorch installation failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Verifying PyTorch installation...
python -c "import torch; import torchvision; print(f'SUCCESS: PyTorch {torch.__version__}, TorchVision {torchvision.__version__}')"

if errorlevel 1 (
    echo.
    echo ERROR: PyTorch verification failed!
    pause
    exit /b 1
)

echo.
echo Step 4: Installing transformers...
pip install transformers>=4.30.0 --no-cache-dir

echo.
echo Step 5: Installing sentence-transformers...
pip install --force-reinstall sentence-transformers==2.2.2 --no-cache-dir

echo.
echo Step 6: Final verification...
python -c "from sentence_transformers import SentenceTransformer; print('SUCCESS: All dependencies installed correctly!')"

if errorlevel 1 (
    echo.
    echo ERROR: Final verification failed! Check error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo FIX COMPLETE!
echo ========================================
echo.
echo You can now restart your server with:
echo   uvicorn app.main:app --reload
echo.
pause
