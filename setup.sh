#!/bin/bash

# Setup script for WebAPI_App
# This script automates the environment setup process

set -e  # Exit on error

echo "🚀 WebAPI_App Setup Script"
echo "=========================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.12"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required (found: $PYTHON_VERSION)"
    exit 1
fi
echo "  Found Python $PYTHON_VERSION ✓"
echo ""

# Check if uv is installed
echo "✓ Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "  uv not found. Installing uv..."
    pip3 install uv
    echo "  uv installed successfully ✓"
else
    UV_VERSION=$(uv --version 2>&1 | awk '{print $2}')
    echo "  Found uv $UV_VERSION ✓"
fi
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "  Virtual environment already exists. Skipping..."
else
    uv venv
    echo "  Virtual environment created ✓"
fi
echo ""

# Activate virtual environment and install dependencies
echo "✓ Installing dependencies..."
source .venv/bin/activate
uv pip install -r requirements.txt
echo "  Dependencies installed ✓"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "  .env file created ✓"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your actual API credentials!"
else
    echo "✓ .env file already exists"
fi
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Base.vn API credentials"
echo "2. Activate virtual environment: source .venv/bin/activate"
echo "3. Run the app: streamlit run app.py"
echo ""
