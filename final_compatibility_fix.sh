#!/bin/bash
# Final compatibility fix for Chatterbox TTS on M1 MacBook Air
# Addresses the MinPLogitsWarper import error

echo "🔧 Final Compatibility Fix for Chatterbox TTS"
echo "=============================================="

# Initialize conda
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate chatterbox

echo "📍 Environment: $CONDA_DEFAULT_ENV"

# Keep the working PyTorch versions (these are good now!)
echo "✅ Keeping working PyTorch versions:"
python -c "
import torch
import torchvision
print(f'PyTorch: {torch.__version__} ✅')
print(f'TorchVision: {torchvision.__version__} ✅')

# Test that torchvision::nms still works
import torchvision.ops
boxes = torch.tensor([[0, 0, 1, 1], [0.5, 0.5, 1.5, 1.5]], dtype=torch.float32)
scores = torch.tensor([0.9, 0.8], dtype=torch.float32)
result = torchvision.ops.nms(boxes, scores, 0.5)
print('torchvision::nms operation: ✅ STILL WORKING')
"

echo ""
echo "🔧 Step 1: Finding compatible transformers version..."
# The issue is MinPLogitsWarper doesn't exist in transformers 4.35.0
# We need a version that has MinPLogitsWarper but still works with PyTorch 2.4.1

# Try transformers 4.40.0 (should have MinPLogitsWarper but be more stable than 4.46.3)
pip install transformers==4.40.0 --force-reinstall

echo ""
echo "🧪 Step 2: Testing MinPLogitsWarper import..."
python -c "
try:
    from transformers.generation.logits_process import MinPLogitsWarper
    print('✅ MinPLogitsWarper import successful')
except ImportError as e:
    print(f'❌ MinPLogitsWarper still missing: {e}')
    print('Trying transformers 4.42.0...')
    import subprocess
    subprocess.run(['pip', 'install', 'transformers==4.42.0', '--force-reinstall'])
"

echo ""
echo "🧪 Step 3: Re-testing after version update..."
python -c "
try:
    from transformers.generation.logits_process import MinPLogitsWarper, TopPLogitsWarper, RepetitionPenaltyLogitsProcessor
    print('✅ All required logits processors available')
    
    # Test LLaMA models still work
    from transformers import LlamaModel, LlamaConfig
    print('✅ LLaMA models still work')
    
except ImportError as e:
    print(f'❌ Still having import issues: {e}')
    print('Trying latest compatible version...')
    import subprocess
    subprocess.run(['pip', 'install', 'transformers==4.44.2', '--force-reinstall'])
"

echo ""
echo "🧪 Step 4: Final comprehensive test..."
python -c "
import torch
import torchvision
print(f'PyTorch: {torch.__version__}')
print(f'TorchVision: {torchvision.__version__}')

# Verify torchvision::nms still works
import torchvision.ops
boxes = torch.tensor([[0, 0, 1, 1]], dtype=torch.float32)
scores = torch.tensor([0.9], dtype=torch.float32)
result = torchvision.ops.nms(boxes, scores, 0.5)
print('✅ torchvision::nms: STILL WORKING')

# Test transformers components
try:
    from transformers import LlamaModel, LlamaConfig
    print('✅ LLaMA models: Working')
    
    from transformers.generation.logits_process import MinPLogitsWarper, TopPLogitsWarper, RepetitionPenaltyLogitsProcessor
    print('✅ All logits processors: Available')
    
    # The moment of truth - test Chatterbox TTS
    from chatterbox.tts import ChatterboxTTS
    print('✅ Chatterbox TTS: SUCCESSFULLY IMPORTED!')
    print('')
    print('🎉 ALL COMPATIBILITY ISSUES RESOLVED!')
    print('🚀 Ready to start the server!')
    
except ImportError as e:
    print(f'❌ Import error: {e}')
    import traceback
    traceback.print_exc()
    
    print('')
    print('💡 If still failing, we may need to use a dev/nightly version:')
    print('   pip install git+https://github.com/huggingface/transformers.git')
"

echo ""
echo "✅ Final compatibility fix complete!"
echo ""
echo "📋 If all tests passed, you can now run:"
echo "   ./start_server.sh"