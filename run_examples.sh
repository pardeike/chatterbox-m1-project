#!/bin/bash
# Run Chatterbox TTS Examples for M1 MacBook Air

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍎 Chatterbox TTS Examples - M1 MacBook Air${NC}"
echo "============================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Conda not found. Please run setup.sh first!${NC}"
    exit 1
fi

# Activate conda environment
echo -e "${BLUE}🐍 Activating conda environment...${NC}"
eval "$(conda shell.bash hook)"
conda activate chatterbox

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate 'chatterbox' environment${NC}"
    echo "Please run setup.sh to create the environment"
    exit 1
fi

# Optimize environment for M1 MacBook Air
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Check if in correct directory
if [ ! -f "examples/basic_examples.py" ]; then
    echo -e "${YELLOW}⚠️  Changing to project directory...${NC}"
    cd "$(dirname "$0")"
fi

echo ""
echo -e "${YELLOW}📋 Available Examples:${NC}"
echo "   1) Basic text-to-speech"
echo "   2) Voice cloning (needs reference audio)"
echo "   3) Multilingual TTS"
echo "   4) Performance benchmarking"
echo "   5) Batch text processing"
echo "   6) All examples (recommended)"
echo ""

# Create audio_samples directory if it doesn't exist
mkdir -p audio_samples

# Check for reference audio
if [ ! -f "reference_voice.wav" ] && [ ! -f "audio_samples/reference_voice.wav" ]; then
    echo -e "${YELLOW}⚠️  No reference audio found for voice cloning${NC}"
    echo "   To test voice cloning:"
    echo "   1. Record 10-30 seconds of clear speech"
    echo "   2. Save as 'reference_voice.wav' in this directory"
    echo "   3. Re-run this script"
    echo ""
fi

read -p "Choose an example (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}🧪 Running basic TTS example...${NC}"
        cd examples
        python3 -c "
from basic_examples import example_1_basic_tts, check_setup
if check_setup():
    example_1_basic_tts()
"
        ;;
    2)
        echo -e "${GREEN}🎭 Running voice cloning example...${NC}"
        cd examples
        python3 -c "
from basic_examples import example_2_voice_cloning, check_setup
if check_setup():
    example_2_voice_cloning()
"
        ;;
    3)
        echo -e "${GREEN}🌍 Running multilingual example...${NC}"
        cd examples
        python3 -c "
from basic_examples import example_3_multilingual, check_setup
if check_setup():
    example_3_multilingual()
"
        ;;
    4)
        echo -e "${GREEN}⚡ Running performance benchmark...${NC}"
        cd examples
        python3 -c "
from basic_examples import example_4_performance_test, check_setup
if check_setup():
    example_4_performance_test()
"
        ;;
    5)
        echo -e "${GREEN}📚 Running batch processing example...${NC}"
        cd examples
        python3 -c "
from basic_examples import example_5_batch_generation, check_setup
if check_setup():
    example_5_batch_generation()
"
        ;;
    6)
        echo -e "${GREEN}🚀 Running all examples...${NC}"
        echo ""
        echo -e "${YELLOW}Note: This will take several minutes and download ~2.5GB of models${NC}"
        echo "Press Enter to continue or Ctrl+C to cancel"
        read
        cd examples
        python3 basic_examples.py
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Example completed!${NC}"

# Show generated files
if ls examples/*.wav 1> /dev/null 2>&1; then
    echo ""
    echo -e "${BLUE}📁 Generated audio files:${NC}"
    for file in examples/*.wav; do
        if [ -f "$file" ]; then
            size=$(du -h "$file" | cut -f1)
            echo "   🎵 $(basename "$file") ($size)"
        fi
    done
    echo ""
    echo -e "${YELLOW}💡 You can play these files with:${NC}"
    echo "   • QuickTime Player"
    echo "   • VLC Media Player"
    echo "   • Or any audio player"
fi

echo ""
echo -e "${BLUE}🌐 Want to try the web interface?${NC}"
echo "   Run: ./start_server.sh"
