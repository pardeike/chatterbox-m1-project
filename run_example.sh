#!/bin/bash
# Run the basic Chatterbox example
# Created by Claude for Michael Koker

echo "🍎 Running Chatterbox Example for M1 MacBook Air"
echo "================================================"

# Change to script directory
cd "$(dirname "$0")"

# Check if conda environment exists
if ! conda env list | grep -q "chatterbox"; then
    echo "❌ Chatterbox environment not found!"
    echo "💡 Please run ./setup_m1.sh first"
    exit 1
fi

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate chatterbox

# Optimize for MacBook Air performance
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Create outputs directory if it doesn't exist
mkdir -p outputs

echo "🚀 Running basic example..."
echo ""

# Run the example
python examples/basic_example.py

echo ""
echo "🎉 Example complete!"
echo "🎧 Check the 'outputs' folder for generated audio files"
echo ""
echo "💡 Next steps:"
echo "   • Start the web server: ./start_server.sh"
echo "   • Add reference audio to 'reference_audio' folder for voice cloning"
echo "   • Open generated audio files with QuickTime Player or any audio app"