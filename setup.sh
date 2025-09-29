#!/bin/bash
# Chatterbox TTS Setup for M1 MacBook Air
# Created by Claude AI Assistant

set -e  # Exit on any error

echo "🍎 Chatterbox TTS Setup for M1 MacBook Air"
echo "=========================================="

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    print_error "This script is designed for Apple Silicon Macs only"
    exit 1
fi

print_success "✅ Running on Apple Silicon ($(uname -m))"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
    print_success "✅ Homebrew installed"
else
    print_success "✅ Homebrew already installed"
fi

# Install system dependencies
print_status "Installing system dependencies..."
brew install ffmpeg portaudio || print_warning "Some packages may already be installed"

# Check if conda is installed (prefer miniforge for M1)
if ! command -v conda &> /dev/null; then
    print_status "Installing Miniforge (ARM64 conda)..."
    cd /tmp
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
    bash Miniforge3-MacOSX-arm64.sh -b -p "$HOME/miniforge3"
    
    # Add to shell profile
    echo 'export PATH="$HOME/miniforge3/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$($HOME/miniforge3/bin/conda shell.zsh hook)"' >> ~/.zshrc
    
    # Source for current session
    export PATH="$HOME/miniforge3/bin:$PATH"
    eval "$($HOME/miniforge3/bin/conda shell.bash hook)"
    
    rm Miniforge3-MacOSX-arm64.sh
    print_success "✅ Miniforge installed"
else
    print_success "✅ Conda already available"
    eval "$(conda shell.bash hook)"
fi

# Create conda environment
print_status "Creating conda environment 'chatterbox'..."
if conda env list | grep -q "chatterbox"; then
    print_warning "Environment 'chatterbox' already exists. Removing and recreating..."
    conda env remove -n chatterbox -y
fi

conda create -n chatterbox python=3.11 -y
conda activate chatterbox

print_success "✅ Conda environment created and activated"

# Install PyTorch with MPS support
print_status "Installing PyTorch with Apple Silicon support..."
conda install pytorch torchvision torchaudio -c pytorch -y

# Install Chatterbox TTS
print_status "Installing Chatterbox TTS..."
pip install chatterbox-tts

# Install additional dependencies for the server
print_status "Installing additional dependencies..."
pip install fastapi uvicorn python-multipart librosa soundfile psutil numpy scipy requests

# Test the installation
print_status "Testing installation..."
python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'MPS available: {torch.backends.mps.is_available()}')
print(f'MPS built: {torch.backends.mps.is_built()}')

try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imported successfully')
except ImportError as e:
    print(f'❌ Chatterbox import failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_success "✅ Installation test passed!"
else
    print_error "❌ Installation test failed!"
    exit 1
fi

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

print_success "🎉 Setup complete!"
echo ""
echo "📍 Project location: $(pwd)"
echo "🚀 Next steps:"
echo "   1. Run: conda activate chatterbox"
echo "   2. Try: ./run_example.sh"
echo "   3. Or start server: ./start_server.sh"
echo ""
echo "💡 Performance tips:"
echo "   • Keep your MacBook plugged in for best performance"
echo "   • Close other memory-intensive applications"
echo "   • Monitor Activity Monitor during intensive tasks"
