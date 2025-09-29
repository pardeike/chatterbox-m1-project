#!/bin/bash
# Definitive Fix for torchvision::nms error on M1 MacBook Air
# This addresses the core Apple Silicon compatibility issue

echo "🔧 Definitive Fix for torchvision::nms on M1 MacBook Air"
echo "========================================================"

# Initialize conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
else
    echo "❌ Conda not found"
    exit 1
fi

# Activate environment
conda activate chatterbox

echo "📍 Environment: $CONDA_DEFAULT_ENV"

# The core issue: torchvision::nms operator doesn't exist
# This happens when PyTorch and TorchVision are compiled differently
# Solution: Use CPU-only versions that are more stable on M1

echo ""
echo "🗑️  Step 1: Complete PyTorch ecosystem cleanup..."
pip uninstall torch torchvision torchaudio -y
conda remove pytorch torchvision torchaudio cpuonly -y

echo ""
echo "📦 Step 2: Installing PyTorch CPU-only (most stable for M1)..."

# Option 1: Try stable CPU-only versions
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu

if [ $? -ne 0 ]; then
    echo "⚠️  Stable versions failed, trying conda..."
    conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 cpuonly -c pytorch -y
fi

if [ $? -ne 0 ]; then
    echo "⚠️  Specific versions failed, trying latest stable..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

echo ""
echo "🧪 Step 3: Testing torchvision operations..."
python -c "
import torch
import torchvision
print(f'PyTorch: {torch.__version__}')
print(f'TorchVision: {torchvision.__version__}')

# Test the specific operation that's failing
try:
    import torchvision.ops
    # Test NMS operation specifically
    boxes = torch.tensor([[0, 0, 1, 1], [0.5, 0.5, 1.5, 1.5]], dtype=torch.float32)
    scores = torch.tensor([0.9, 0.8], dtype=torch.float32)
    result = torchvision.ops.nms(boxes, scores, 0.5)
    print('✅ torchvision::nms operation works!')
except Exception as e:
    print(f'❌ torchvision::nms still failing: {e}')
    raise
"

echo ""
echo "📦 Step 4: Adjusting other dependencies..."
# Sometimes we need to downgrade transformers for compatibility
pip install transformers==4.35.0 --force-reinstall

echo ""
echo "📦 Step 5: Reinstalling Chatterbox with no-deps..."
pip uninstall chatterbox-tts -y
pip install chatterbox-tts --no-deps
pip install librosa soundfile numpy scipy fastapi uvicorn python-multipart

echo ""
echo "🧪 Step 6: Final comprehensive test..."
python -c "
import torch
import torchvision
import torchvision.ops
print(f'✅ PyTorch: {torch.__version__}')
print(f'✅ TorchVision: {torchvision.__version__}')

# Test the problematic import chain
try:
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA import successful')
except Exception as e:
    print(f'❌ Transformers error: {e}')
    raise

# Test Chatterbox TTS
try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS import successful')
    print('')
    print('🎉 ALL IMPORTS SUCCESSFUL!')
    print('🚀 torchvision::nms error is FIXED!')
except Exception as e:
    print(f'❌ Chatterbox TTS error: {e}')
    import traceback
    traceback.print_exc()
    raise
"

echo ""
echo "✅ Definitive fix complete!"
echo ""
echo "📋 If this worked, you can now run:"
echo "   ./start_server.sh"
echo ""
echo "💡 This fix uses CPU-only PyTorch which is more stable on M1"
echo "💡 Performance will still be excellent on Apple Silicon"