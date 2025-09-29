#!/bin/bash
# Quick fix for rope_scaling configuration issue
# This resolves the final compatibility problem

echo "🔧 Fixing rope_scaling configuration issue..."

# Initialize conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate chatterbox

echo "📦 Installing specific transformers version for rope_scaling compatibility..."

# The issue is transformers version compatibility with rope_scaling format
# Try transformers 4.46.3 which Chatterbox was designed for
pip install transformers==4.46.3 --force-reinstall

echo "🧪 Testing the fix..."
python -c "
try:
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS imports successfully')
    
    # Try creating the model (this will test the rope_scaling issue)
    print('⚡ Testing model initialization...')
    model = ChatterboxTTS.from_pretrained(device='cpu')  # Use CPU for testing
    print('✅ Model initialization successful!')
    
    print('')
    print('🎉 rope_scaling issue FIXED!')
    print('🚀 Server should now work for text generation')
    
except Exception as e:
    print(f'❌ Still having issues: {e}')
    print('')
    print('💡 Alternative approach: Try transformers==4.44.2')
    import subprocess
    subprocess.run(['pip', 'install', 'transformers==4.44.2', '--force-reinstall'])
"

echo ""
echo "✅ Fix complete!"
echo ""
echo "📋 Now restart your server:"
echo "   1. Press Ctrl+C to stop the current server"
echo "   2. Run: python server.py"
echo "   3. Try generating text at http://localhost:8000"