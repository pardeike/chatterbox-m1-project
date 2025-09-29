#!/bin/bash
# Chatterbox TTS Installation for M1 MacBook Air

echo "Setting up Chatterbox for M1 MacBook Air"
echo "============================================"

# Check if we're on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "This script is designed for Apple Silicon Macs"
    exit 1
fi

# Set script directory as working directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for M1 Macs
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Install system dependencies
echo "Installing system dependencies..."
brew install ffmpeg portaudio

# Install miniforge (conda for ARM64) if not present
if ! command -v conda &> /dev/null; then
    echo "Installing Miniforge (ARM64 conda)..."
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
    bash Miniforge3-MacOSX-arm64.sh -b -p "$HOME/miniforge3"
    
    # Initialize conda
    "$HOME/miniforge3/bin/conda" init zsh
    source ~/.zshrc
    rm Miniforge3-MacOSX-arm64.sh
fi

# Initialize conda for this session
eval "$($HOME/miniforge3/bin/conda shell.bash hook)"

# Create conda environment with ARM64-optimized packages
echo "Creating conda environment..."
conda create -n chatterbox python=3.11 -y
conda activate chatterbox

# Install PyTorch with MPS support for M1
echo "Installing PyTorch with Apple Silicon support..."
conda install pytorch torchvision torchaudio -c pytorch -y

# Install Chatterbox TTS and dependencies
echo "Installing Chatterbox TTS..."
pip install chatterbox-tts
pip install fastapi uvicorn python-multipart
pip install librosa soundfile psutil

# Test installation
echo "Testing installation..."
python -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'MPS available: {torch.backends.mps.is_available()}')
try:
    from chatterbox.tts import ChatterboxTTS
    print('Chatterbox TTS: Available')
    print('Installation complete!')
except ImportError as e:
    print(f'Chatterbox import failed: {e}')
    exit(1)
"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "   1. Run: conda activate chatterbox"
echo "   2. Try: ./run_example.sh"
echo "   3. Or start server: ./start_server.sh"
echo ""
echo "Performance tips for MacBook Air:"
echo "   • Keep your MacBook plugged in for sustained performance"
echo "   • Close other memory-intensive applications"
echo "   • Use shorter texts for better memory efficiency"