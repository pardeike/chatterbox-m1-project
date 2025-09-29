#!/bin/bash
# Voice Cloning Example Runner
# Created by Claude for Michael Koker

echo "🎭 Running Voice Cloning Example for M1 MacBook Air"
echo "==================================================="

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

# Check if reference audio directory has files
if [ ! "$(ls -A reference_audio 2>/dev/null)" ]; then
    echo "📁 Reference audio folder is empty"
    echo "💡 To test voice cloning:"
    echo "   1. Record a 10-30 second voice sample"
    echo "   2. Save it as a .wav file in the 'reference_audio' folder"
    echo "   3. Run this script again"
    echo ""
    echo "🎙️ For now, running without voice cloning..."
fi

echo "🚀 Running voice cloning example..."
echo ""

# Run the voice cloning example
python examples/voice_cloning_example.py

echo ""
echo "🎉 Voice cloning example complete!"
echo "🎧 Check the 'outputs' folder for generated audio files"