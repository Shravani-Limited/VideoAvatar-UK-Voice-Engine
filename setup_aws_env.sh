#!/bin/bash

# setup_aws_env.sh
# Automated setup for F5-TTS training on AWS EC2 (Ubuntu/Deep Learning AMI)
# Ideal for g5.2xlarge or similar instances.

set -e  # Exit immediately if a command exits with a non-zero status.

echo "🚀 Starting AWS Environment Setup for F5-TTS..."

# 1. System Updates & Essential Libraries
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get install -y \
    libsndfile1 \
    ffmpeg \
    git \
    build-essential \
    python3-dev

# 2. Check for NVIDIA Driver
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  WARNING: nvidia-smi not found! Ensure you are running on a GPU instance with drivers installed."
    echo "    On AWS, use the 'Deep Learning AMI' to avoid manual driver installation."
else
    echo "✅ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
fi

# 3. Setup Python Environment (using venv for simplicity on standard AMI)
# Note: On Deep Learning AMIs, you might prefer Conda. This script uses venv for a clean slate.
echo "🐍 Setting up Python Virtual Environment..."
if [ -d "venv" ]; then
    echo "   Removing existing venv..."
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# 4. Install PyTorch (CUDA 12.1 is stable for most F5-TTS builds)
echo "🔥 Installing PyTorch (with CUDA 12.1)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5. Install F5-TTS Dependencies
echo "📚 Installing F5-TTS requirements..."
pip install -r requirements.txt

# 6. Install F5-TTS (from source, or local link)
# Using git+https to ensure we get the latest code structure if needed, 
# but for now we rely on requirements.txt for the heavy lifting.
# If you cloned F5-TTS separately, you would run `pip install -e .` here.

echo "✅ Environment Setup Complete!"
echo "👉 To activate: source venv/bin/activate"
