#!/bin/bash
# Quick fix for missing sympy dependency

echo "🔧 Installing missing sympy dependency..."

# Initialize conda
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate chatterbox

# Install sympy
echo "📦 Installing sympy..."
pip install sympy

# Test everything works now
echo "🧪 Testing complete installation..."
python -c "
try:
    import sympy
    print(f'✅ SymPy: {sympy.__version__}')
    
    import torch
    print(f'✅ PyTorch: {torch.__version__}')
    
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA models working')
    
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imported successfully')
    
    print('')
    print('🎉 EVERYTHING IS WORKING!')
    print('🚀 Ready to run the server!')
    
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "✅ Sympy fix complete!"