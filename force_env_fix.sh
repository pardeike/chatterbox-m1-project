#!/bin/bash
# Force fix for environment activation issues

echo "🔧 Force Environment Fix"
echo "========================"

# Initialize conda
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

# Deactivate and reactivate environment
conda deactivate
conda activate chatterbox

# Set explicit paths
export PATH="$HOME/miniforge3/envs/chatterbox/bin:$PATH"
export PYTHONPATH="$HOME/miniforge3/envs/chatterbox/lib/python3.11/site-packages"

echo "📍 Using Python: $(which python)"
echo "📍 Environment: $CONDA_DEFAULT_ENV"

# Test if it works now
echo ""
echo "🧪 Testing with forced paths..."
python -c "
import sys
print(f'Python executable: {sys.executable}')

try:
    import sympy
    print(f'✅ SymPy: {sympy.__version__}')
    
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA: Working')
    
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS: Working')
    
    print('')
    print('🎉 EVERYTHING WORKS!')
    print('✅ Ready to start server!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('')
    print('🔄 Trying alternative approach...')
    
    # Alternative: use the full Python path
    import subprocess
    import os
    
    conda_python = os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')
    print(f'Trying conda Python: {conda_python}')
"

echo ""
echo "💡 If that worked, you can now run:"
echo "   ./start_server.sh"
echo ""
echo "🔧 If it didn't work, let's try the debug script:"
echo "   ./debug_environment.sh"