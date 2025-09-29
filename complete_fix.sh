#!/bin/bash
# Complete Environment Fix for Chatterbox TTS on M1 MacBook Air
# Addresses version conflicts and numpy issues

echo "🔧 Complete Chatterbox Environment Fix for M1 MacBook Air"
echo "=========================================================="

# Initialize conda
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    echo "📍 Found conda at $HOME/miniforge3"
    export PATH="$HOME/miniforge3/bin:$PATH"
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
else
    echo "❌ Miniforge3 not found. Please run ./setup_m1.sh first"
    exit 1
fi

# Activate environment
echo "🔄 Activating chatterbox environment..."
conda activate chatterbox

if [[ "$CONDA_DEFAULT_ENV" != "chatterbox" ]]; then
    echo "❌ Failed to activate environment"
    exit 1
fi

echo "✅ Environment activated: $CONDA_DEFAULT_ENV"

# Step 1: Complete cleanup
echo ""
echo "🧹 Step 1: Complete package cleanup..."
pip uninstall torch torchaudio torchvision transformers chatterbox-tts gradio numpy scipy -y 2>/dev/null || true
conda remove pytorch torchvision torchaudio numpy scipy -y 2>/dev/null || true

# Clear cache
pip cache purge
conda clean --all -y

# Step 2: Install numpy first (fixes the numpy.exceptions error)
echo ""
echo "📦 Step 2: Installing numpy..."
conda install numpy=1.24.3 -c conda-forge -y

# Step 3: Install the exact PyTorch versions that Chatterbox wants
echo ""
echo "📦 Step 3: Installing PyTorch 2.6.0 (as required by Chatterbox)..."

# Try to install PyTorch 2.6.0 - if not available, use nightly
pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

if [ $? -ne 0 ]; then
    echo "⚠️  PyTorch 2.6.0 not available, trying nightly build..."
    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
fi

# Step 4: Install exact transformers version
echo ""
echo "📦 Step 4: Installing transformers 4.46.3..."
pip install transformers==4.46.3

# Step 5: Install other dependencies
echo ""
echo "📦 Step 5: Installing other dependencies..."
pip install scipy librosa soundfile
pip install brotli>=1.1.0  # For gradio

# Step 6: Install Chatterbox TTS
echo ""
echo "📦 Step 6: Installing Chatterbox TTS..."
pip install chatterbox-tts --no-deps
pip install fastapi uvicorn python-multipart psutil

# Step 7: Verify installation
echo ""
echo "🧪 Step 7: Testing installation..."
python -c "
import sys
print(f'Python: {sys.version}')
print('')

# Test numpy first
try:
    import numpy as np
    print(f'✅ NumPy: {np.__version__}')
    # Test the specific attribute that was failing
    test_array = np.ndarray((2, 2))
    print('✅ NumPy ndarray works')
except Exception as e:
    print(f'❌ NumPy error: {e}')

# Test PyTorch
try:
    import torch
    print(f'✅ PyTorch: {torch.__version__}')
    
    import torchvision
    print(f'✅ TorchVision: {torchvision.__version__}')
    
    import torchaudio
    print(f'✅ TorchAudio: {torchaudio.__version__}')
    
    # Test MPS
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        print('✅ MPS acceleration available')
        device = 'mps'
    else:
        print('ℹ️  Using CPU (MPS not available)')
        device = 'cpu'
        
except Exception as e:
    print(f'❌ PyTorch error: {e}')

# Test transformers
try:
    import transformers
    print(f'✅ Transformers: {transformers.__version__}')
    
    # Test the specific import that was failing
    from transformers import LlamaModel, LlamaConfig
    print('✅ LLaMA models import successfully')
    
except Exception as e:
    print(f'❌ Transformers error: {e}')

# Test Chatterbox TTS
try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imported successfully')
    print('')
    print('🎉 ALL TESTS PASSED!')
    print('🚀 Ready to run: ./start_server.sh')
    
except Exception as e:
    print(f'❌ Chatterbox TTS error: {e}')
    print('')
    print('💡 If Chatterbox still fails, the model may need to download on first use')
"

echo ""
echo "🎉 Complete environment fix finished!"
echo ""
echo "📋 Next steps:"
echo "   1. Test basic functionality: ./run_example.sh"
echo "   2. Start web server: ./start_server.sh"
echo "   3. If still having issues, restart terminal and try again"