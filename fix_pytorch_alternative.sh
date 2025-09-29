#!/bin/bash
# Alternative PyTorch installation method for M1 MacBook Air
# If the main fix doesn't work, try this approach

echo "🔄 Alternative PyTorch installation for M1 MacBook Air..."

# Activate environment
eval "$(conda shell.bash hook)"
conda activate chatterbox

# Complete clean slate approach
echo "🧹 Complete cleanup of PyTorch packages..."
pip uninstall torch torchaudio torchvision transformers -y
conda remove pytorch torchvision torchaudio cpuonly -y

# Clean everything
conda clean --all -y
pip cache purge

# Install PyTorch using conda-forge (often more reliable for M1)
echo "📦 Installing PyTorch via conda-forge..."
conda install pytorch torchvision torchaudio cpuonly -c pytorch -c conda-forge -y

# If that fails, try the official PyTorch conda channel with specific versions
# conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 cpuonly -c pytorch -y

# Reinstall other dependencies
echo "📦 Reinstalling other dependencies..."
pip install transformers
pip install chatterbox-tts --no-deps --force-reinstall

# Install any missing dependencies individually
pip install librosa soundfile numpy scipy

echo "🧪 Testing installation..."
python -c "
try:
    import torch
    import torchvision
    print(f'✅ PyTorch: {torch.__version__}')
    print(f'✅ TorchVision: {torchvision.__version__}')
    
    # Test MPS
    if hasattr(torch.backends, 'mps'):
        print(f'✅ MPS available: {torch.backends.mps.is_available()}')
    else:
        print('ℹ️  MPS not available in this PyTorch version')
    
    # Test problematic import
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA import successful')
    
    # Test Chatterbox
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS import successful')
    
    print('🎉 All imports successful!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('💡 Try the manual installation steps below')
"

echo "✅ Alternative installation complete!"