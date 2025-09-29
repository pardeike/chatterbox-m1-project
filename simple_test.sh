#!/bin/bash
# Simple Environment Test and Fix

echo "🔍 Environment Diagnosis"
echo "======================="

# Find conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
    echo "✅ Found conda initialization"
else
    echo "❌ Conda not found"
    exit 1
fi

# Check environments
echo ""
echo "📋 Available environments:"
conda env list

# Activate chatterbox
echo ""
echo "🔄 Activating chatterbox..."
conda activate chatterbox

# Check activation
echo "📍 Current environment: $CONDA_DEFAULT_ENV"
echo "📍 Python location: $(which python)"
echo "📍 Pip location: $(which pip)"

# Check what's actually installed
echo ""
echo "📦 Installed packages:"
pip list | grep -E "(torch|sympy|chatterbox|transformers)"

# Test sympy installation location
echo ""
echo "🔍 Checking sympy installation:"
python -c "
import sys
import os

# Print Python info
print(f'Python executable: {sys.executable}')
print(f'Python version: {sys.version}')

# Check if sympy exists in site-packages
site_packages_dirs = [p for p in sys.path if 'site-packages' in p]
print(f'Site-packages directories:')
for sp in site_packages_dirs:
    print(f'  {sp}')
    if os.path.exists(sp):
        sympy_exists = os.path.exists(os.path.join(sp, 'sympy'))
        print(f'    sympy exists here: {sympy_exists}')

# Try to import sympy
try:
    import sympy
    print(f'✅ SymPy import successful: {sympy.__version__}')
    print(f'SymPy location: {sympy.__file__}')
except ImportError as e:
    print(f'❌ SymPy import failed: {e}')
"

echo ""
echo "🔧 If sympy is missing, installing it now..."
pip install sympy --force-reinstall

echo ""
echo "🧪 Final test:"
python -c "
try:
    import sympy
    print(f'✅ SymPy: {sympy.__version__}')
    
    import torch
    print(f'✅ PyTorch: {torch.__version__}')
    
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS: Working!')
    
    print('')
    print('🎉 EVERYTHING IS WORKING!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
"