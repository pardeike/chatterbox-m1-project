#!/bin/bash
# Diagnostic script to debug the sympy/environment issue

echo "🔍 Debugging Environment Issues"
echo "==============================="

# Initialize conda
if [ -f "$HOME/miniforge3/bin/conda" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate chatterbox

echo "📍 Environment Information:"
echo "   CONDA_DEFAULT_ENV: $CONDA_DEFAULT_ENV"
echo "   CONDA_PREFIX: $CONDA_PREFIX"

echo ""
echo "🐍 Python Information:"
which python
python --version
echo "   Python path: $(which python)"

echo ""
echo "📦 Package Locations:"
python -c "
import sys
print('Python executable:', sys.executable)
print('Python path:')
for p in sys.path:
    print(f'  {p}')
"

echo ""
echo "🔍 Sympy Investigation:"
python -c "
import sys
import os

# Check if sympy directory exists
conda_prefix = os.environ.get('CONDA_PREFIX', '')
sympy_path = os.path.join(conda_prefix, 'lib', 'python3.11', 'site-packages', 'sympy')
print(f'SymPy expected at: {sympy_path}')
print(f'SymPy directory exists: {os.path.exists(sympy_path)}')

if os.path.exists(sympy_path):
    print(f'SymPy contents: {os.listdir(sympy_path)[:5]}...')

# Try different import methods
try:
    import sympy
    print(f'✅ Direct import successful: {sympy.__version__}')
    print(f'SymPy location: {sympy.__file__}')
except ImportError as e:
    print(f'❌ Direct import failed: {e}')

# Try sys.path manipulation
try:
    site_packages = os.path.join(conda_prefix, 'lib', 'python3.11', 'site-packages')
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)
        print(f'Added to path: {site_packages}')
    
    import sympy
    print(f'✅ Import after path fix successful: {sympy.__version__}')
except ImportError as e:
    print(f'❌ Import after path fix failed: {e}')
"

echo ""
echo "💡 Attempting Different Activation Method:"

# Try a more explicit activation
export PATH="$HOME/miniforge3/envs/chatterbox/bin:$PATH"
export PYTHONPATH="$HOME/miniforge3/envs/chatterbox/lib/python3.11/site-packages:$PYTHONPATH"

python -c "
try:
    import sympy
    print(f'✅ SymPy works with explicit PATH: {sympy.__version__}')
    
    # Now test the full chain
    from transformers import LlamaModel, LlamaConfig
    print('✅ Transformers LLaMA import successful')
    
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS import successful')
    
    print('')
    print('🎉 SUCCESS! Environment is working!')
    
except Exception as e:
    print(f'❌ Still failing: {e}')
    import traceback
    traceback.print_exc()
"