#!/bin/bash
# Start the Chatterbox TTS Server

echo "Starting Chatterbox TTS Server for M1 MacBook Air"
echo "====================================================="

# Change to script directory
cd "$(dirname "$0")"

# Initialize conda properly for M1 Mac
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    echo "Initializing conda from miniforge3..."
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
elif [ -f "/opt/homebrew/bin/conda" ]; then
    echo "Using conda from Homebrew..."
    export PATH="/opt/homebrew/bin:$PATH"
    eval "$(conda shell.bash hook)"
else
    echo "Conda not found! Please run ./setup_m1.sh first"
    exit 1
fi

# Check if conda is now available
if ! command -v conda &> /dev/null; then
    echo "Conda still not available after initialization"
    echo "Try: source $HOME/miniforge3/etc/profile.d/conda.sh"
    exit 1
fi

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate chatterbox

# Check if packages are installed
python -c "
try:
    from chatterbox.tts import ChatterboxTTS
    import fastapi
    import uvicorn
    print('All dependencies found')
except ImportError as e:
    print(f'Missing dependency: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "Please run ./setup_m1.sh first"
    exit 1
fi

# Optimize for MacBook Air performance
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Show system info
echo "System Information:"
python -c "
import torch
import psutil
print(f'   Device: {'MPS' if torch.backends.mps.is_available() else 'CPU'}')
print(f'   Available memory: {psutil.virtual_memory().available / 1024**3:.1f} GB')
print(f'   CPU usage: {psutil.cpu_percent()}%')
"

echo ""
echo "Starting server..."
echo "Open http://localhost:8000 in your browser"
echo "API documentation: http://localhost:8000/docs"
echo ""
echo "Tips:"
echo "   • Keep your MacBook plugged in for best performance"
echo "   • Close other memory-intensive apps"
echo "   • Press Ctrl+C to stop the server"
echo ""

# Start the server
python server.py