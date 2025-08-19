#!/bin/bash

# Qdrant Workshop Setup Script
# This script helps set up the workshop environment

echo "🚀 Qdrant Vector Database Workshop Setup"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version detected. Python $required_version+ is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 detected"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error above."
    exit 1
fi

# Check if JupyterLab is available
if ! python3 -c "import jupyterlab" &> /dev/null; then
    echo ""
    echo "📚 Installing JupyterLab..."
    if pip3 install jupyterlab; then
        echo "✅ JupyterLab installed successfully!"
    else
        echo "❌ Failed to install JupyterLab. Please install manually: pip install jupyterlab"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "🔐 Setting up environment configuration..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Created .env file from env.example"
        echo "⚠️  IMPORTANT: Edit .env file with your Qdrant Cloud credentials!"
        echo "   - QDRANT_URL: Your cluster URL from cloud.qdrant.io"
        echo "   - QDRANT_API_KEY: Your API key from cloud.qdrant.io"
    else
        echo "⚠️  env.example not found. Please create .env file manually."
    fi
else
    echo "✅ .env file already exists"
fi

# Check if .env has been configured
if [ -f .env ]; then
    if grep -q "your-cluster.qdrant.io" .env || grep -q "your-api-key" .env; then
        echo ""
        echo "⚠️  WARNING: .env file contains placeholder values!"
        echo "   Please edit .env file with your actual Qdrant Cloud credentials:"
        echo "   - QDRANT_URL=https://your-cluster.qdrant.io:6333"
        echo "   - QDRANT_API_KEY=your-actual-api-key"
    else
        echo "✅ .env file appears to be configured"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Qdrant Cloud credentials"
echo "2. Launch JupyterLab: jupyter lab"
echo "3. Open 01_fundamentals.ipynb and follow the workshop"
echo ""
echo "🔗 Get Qdrant Cloud credentials at: https://cloud.qdrant.io"
echo "📚 Workshop documentation: README.md"
echo ""
echo "Happy learning! 🚀"
