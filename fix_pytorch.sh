#!/bin/bash
# Fixed PyTorch Installation for M1 MacBook Air
# Addresses the torchvision::nms compatibility issue

echo "🔧 Fixing PyTorch installation for M1 MacBook Air..."

# Initialize conda properly for M1 Mac
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    echo "📍 Found conda at $HOME/miniforge3"
    export PATH="$HOME/miniforge3/bin:$PATH"
    eval "$($HOME/miniforge3/bin/conda shell.bash hook)"
elif [ -f "/opt/homebrew/bin/conda" ]; then
    echo "📍 Found conda via Homebrew"
    export PATH="/opt/homebrew/bin:$PATH"
    eval "$(conda shell.bash hook)"
elif command -v conda &> /dev/null; then
    echo "📍 Found conda in PATH"
    eval "$(conda shell.bash hook)"
else
    echo "❌ Conda not found! Please run ./setup_m1.sh first"
    exit 1
fi

# Check if chatterbox environment exists
if ! conda env list | grep -q "chatterbox"; then
    echo "❌ Chatterbox environment not found!"
    echo "💡 Please run ./setup_m1.sh first to create the environment"
    exit 1
fi

# Activate the chatterbox environment
echo "🔄 Activating chatterbox environment..."
conda activate chatterbox

# Verify we're in the right environment
if [[ "$CONDA_DEFAULT_ENV" != "chatterbox" ]]; then
    echo "❌ Failed to activate chatterbox environment"
    echo "💡 Try manually: conda activate chatterbox"
    exit 1
fi

echo "✅ Successfully activated chatterbox environment"

# Remove existing PyTorch installations that might be causing conflicts
echo "🗑️  Removing conflicting PyTorch packages..."
pip uninstall torch torchaudio torchvision -y
conda remove pytorch torchvision torchaudio -y

# Clear conda cache
conda clean --all -y

# Install specific compatible versions for Apple Silicon
echo "📦 Installing compatible PyTorch for Apple Silicon..."

# Method 1: Use pip with specific Apple Silicon wheels (most reliable)
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# If the above doesn't work, try the nightly builds which often have better M1 support
# pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Reinstall transformers to ensure compatibility
pip install --upgrade transformers

# Test the installation
echo "🧪 Testing PyTorch installation..."
python -c "
import torch
import torchvision
print(f'✅ PyTorch version: {torch.__version__}')
print(f'✅ TorchVision version: {torchvision.__version__}')
print(f'✅ MPS available: {torch.backends.mps.is_available() if hasattr(torch.backends, \"mps\") else \"Not available in this version\"}')

# Test the specific operation that was failing
try:
    import torchvision.ops
    print('✅ TorchVision ops (including NMS) imported successfully')
except Exception as e:
    print(f'⚠️  TorchVision ops issue: {e}')

# Test Chatterbox import
try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imported successfully')
except Exception as e:
    print(f'❌ Chatterbox import failed: {e}')
"

echo "🔧 PyTorch fix complete!"