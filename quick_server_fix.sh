#!/bin/bash
# Quick fix to remove speed_factor parameter that's causing the error

echo "🔧 Fixing server.py to remove unsupported speed_factor parameter..."

# Stop the current server first
echo "💡 Press Ctrl+C in the server terminal to stop it, then run this fix"

# Initialize conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

conda activate chatterbox

# Create a fixed version of the server
python -c "
import re

# Read the current server.py
with open('server.py', 'r') as f:
    content = f.read()

# Remove speed_factor from the function signature
content = re.sub(
    r'speed_factor: float = Form\(1\.0\),\s*',
    '',
    content
)

# Remove speed_factor from the generate() calls
content = re.sub(
    r',\s*speed_factor=speed_factor',
    '',
    content
)

# Write the fixed version
with open('server.py', 'w') as f:
    f.write(content)

print('✅ Fixed server.py - removed speed_factor parameter')
"

echo "🧪 Testing that Chatterbox can generate audio..."
python -c "
try:
    from chatterbox.tts import ChatterboxTTS
    import torchaudio as ta
    
    print('Loading model...')
    model = ChatterboxTTS.from_pretrained(device='mps')
    
    print('Generating test audio...')
    wav = model.generate(
        'Hello world test!',
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.7
    )
    
    ta.save('test_output.wav', wav, model.sr)
    print('✅ Audio generation successful!')
    print('✅ Server should now work!')
    
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "✅ Fix complete!"
echo "🚀 Now restart your server:"
echo "   python server.py"