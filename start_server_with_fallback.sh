#!/bin/bash
# Enable MPS fallback for operations not yet supported on Apple Silicon

echo "Enabling MPS Fallback for M1 MacBook Air"
echo "==========================================="

# Initialize conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

conda activate chatterbox

# Set the environment variable to enable MPS fallback
export PYTORCH_ENABLE_MPS_FALLBACK=1

echo "MPS fallback enabled"
echo "Starting server with CPU fallback for unsupported operations..."
echo ""
echo "The server will use MPS (Apple Silicon GPU) where possible"
echo "and automatically fall back to CPU for unsupported operations"
echo ""

# Start the server with the environment variable set
python server.py