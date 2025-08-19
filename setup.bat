@echo off
REM Qdrant Workshop Setup Script for Windows
REM This script helps set up the workshop environment

echo 🚀 Qdrant Vector Database Workshop Setup
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python detected: %python_version%

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip detected

REM Install dependencies
echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies. Please check the error above.
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully!

REM Check if JupyterLab is available
python -c "import jupyterlab" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📚 Installing JupyterLab...
    pip install jupyterlab
    if errorlevel 1 (
        echo ❌ Failed to install JupyterLab. Please install manually: pip install jupyterlab
    ) else (
        echo ✅ JupyterLab installed successfully!
    )
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo 🔐 Setting up environment configuration...
    if exist env.example (
        copy env.example .env >nul
        echo ✅ Created .env file from env.example
        echo ⚠️  IMPORTANT: Edit .env file with your Qdrant Cloud credentials!
        echo    - QDRANT_URL: Your cluster URL from cloud.qdrant.io
        echo    - QDRANT_API_KEY: Your API key from cloud.qdrant.io
    ) else (
        echo ⚠️  env.example not found. Please create .env file manually.
    )
) else (
    echo ✅ .env file already exists
)

REM Check if .env has been configured
if exist .env (
    findstr "your-cluster.qdrant.io" .env >nul
    if not errorlevel 1 (
        echo.
        echo ⚠️  WARNING: .env file contains placeholder values!
        echo    Please edit .env file with your actual Qdrant Cloud credentials:
        echo    - QDRANT_URL=https://your-cluster.qdrant.io:6333
        echo    - QDRANT_API_KEY=your-actual-api-key
    ) else (
        echo ✅ .env file appears to be configured
    )
)

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your Qdrant Cloud credentials
echo 2. Launch JupyterLab: jupyter lab
echo 3. Open 01_fundamentals.ipynb and follow the workshop
echo.
echo 🔗 Get Qdrant Cloud credentials at: https://cloud.qdrant.io
echo 📚 Workshop documentation: README.md
echo.
echo Happy learning! 🚀
pause
