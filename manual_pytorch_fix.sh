#!/bin/bash
# Simple Manual PyTorch Fix for M1 MacBook Air
# Step-by-step approach when automation fails

echo "🔧 Manual PyTorch Fix for M1 MacBook Air"
echo "========================================"
echo ""

# Step 1: Initialize conda
echo "Step 1: Initializing conda..."
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    echo "✅ Found miniforge3"
    export PATH="$HOME/miniforge3/bin:$PATH"
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
else
    echo "❌ Miniforge3 not found. Please run ./setup_m1.sh first"
    exit 1
fi

# Step 2: Activate environment
echo ""
echo "Step 2: Activating chatterbox environment..."
conda activate chatterbox

if [[ "$CONDA_DEFAULT_ENV" != "chatterbox" ]]; then
    echo "❌ Failed to activate environment"
    echo "💡 Please run these commands manually:"
    echo "   source $HOME/miniforge3/etc/profile.d/conda.sh"
    echo "   conda activate chatterbox"
    exit 1
fi

echo "✅ Environment activated: $CONDA_DEFAULT_ENV"

# Step 3: Show current versions
echo ""
echo "Step 3: Current package versions..."
python -c "
try:
    import torch
    print(f'Current PyTorch: {torch.__version__}')
except ImportError:
    print('PyTorch: Not installed')

try:
    import torchvision
    print(f'Current TorchVision: {torchvision.__version__}')
except ImportError:
    print('TorchVision: Not installed')
"

# Step 4: Remove packages
echo ""
echo "Step 4: Removing problematic packages..."
echo "💡 This may show errors if packages aren't installed - that's OK"
pip uninstall torch torchaudio torchvision transformers -y 2>/dev/null || echo "Some packages weren't installed"

# Step 5: Install fresh packages
echo ""
echo "Step 5: Installing fresh PyTorch..."
echo "📦 This may take a few minutes..."

# Use CPU-only PyTorch for better compatibility
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

if [ $? -ne 0 ]; then
    echo "⚠️  Pip install failed, trying conda..."
    conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
fi

# Step 6: Install other dependencies
echo ""
echo "Step 6: Installing other dependencies..."
pip install transformers
pip install chatterbox-tts --force-reinstall

# Step 7: Test installation
echo ""
echo "Step 7: Testing installation..."
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import torch
    print(f'✅ PyTorch: {torch.__version__}')
    
    import torchvision
    print(f'✅ TorchVision: {torchvision.__version__}')
    
    # Test the problematic operation
    import torchvision.ops
    print('✅ TorchVision ops imported successfully')
    
    # Test transformers
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA imported successfully')
    
    # Test Chatterbox
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imported successfully')
    
    # Test MPS
    if hasattr(torch.backends, 'mps'):
        print(f'✅ MPS available: {torch.backends.mps.is_available()}')
    else:
        print('ℹ️  MPS not available (using CPU)')
    
    print('')
    print('🎉 ALL TESTS PASSED!')
    print('🚀 You can now run: ./start_server.sh')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('')
    print('💡 If you still have issues, try:')
    print('   1. Restart terminal')
    print('   2. conda activate chatterbox')
    print('   3. Run this script again')
"

echo ""
echo "🔧 Manual fix complete!"