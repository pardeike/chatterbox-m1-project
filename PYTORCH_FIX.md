# 🔧 PyTorch/TorchVision Fix for M1 MacBook Air

The error you encountered is a common compatibility issue between PyTorch and TorchVision on Apple Silicon. Here's how to fix it:

## 🚀 Quick Fix

**Run this command in your terminal:**

```bash
cd ~/chatterbox-m1-project
chmod +x fix_pytorch.sh
./fix_pytorch.sh
```

This will:
1. Remove conflicting PyTorch packages
2. Install compatible versions
3. Test the installation

## 🔄 Alternative Fix (if quick fix doesn't work)

```bash
chmod +x fix_pytorch_alternative.sh
./fix_pytorch_alternative.sh
```

## 🛠️ Manual Fix (step by step)

If the automated fixes don't work, follow these manual steps:

### 1. Activate Environment
```bash
conda activate chatterbox
```

### 2. Clean Installation
```bash
# Remove existing packages
pip uninstall torch torchaudio torchvision transformers -y
conda remove pytorch torchvision torchaudio -y

# Clear cache
conda clean --all -y
pip cache purge
```

### 3. Install Compatible Versions

**Option A: Using pip (recommended for M1)**
```bash
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

**Option B: Using conda**
```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch -c conda-forge
```

**Option C: Nightly builds (latest features)**
```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

### 4. Reinstall Dependencies
```bash
pip install transformers
pip install chatterbox-tts --force-reinstall
pip install librosa soundfile numpy scipy
```

### 5. Test Installation
```bash
python -c "
import torch
import torchvision
from chatterbox.tts import ChatterboxTTS
print('✅ All packages imported successfully!')
print(f'PyTorch: {torch.__version__}')
print(f'TorchVision: {torchvision.__version__}')
print(f'MPS available: {torch.backends.mps.is_available() if hasattr(torch.backends, \"mps\") else False}')
"
```

## 🔍 Understanding the Error

The error `operator torchvision::nms does not exist` occurs because:

1. **Version Mismatch**: PyTorch and TorchVision versions are incompatible
2. **Architecture Issue**: Packages weren't compiled properly for Apple Silicon
3. **Installation Method**: Mixing conda and pip installations can cause conflicts

## 🎯 Prevention for Future

To avoid this issue in the future:

1. **Use consistent installation methods** (either conda or pip, not both)
2. **Install from Apple Silicon optimized sources**
3. **Use version pinning** for critical packages
4. **Test immediately after installation**

## ✅ Verification Steps

After fixing, verify everything works:

```bash
# Test basic PyTorch
python -c "import torch; print('PyTorch OK')"

# Test TorchVision ops
python -c "import torchvision.ops; print('TorchVision ops OK')"

# Test Transformers
python -c "from transformers import LlamaModel; print('Transformers OK')"

# Test Chatterbox
python -c "from chatterbox.tts import ChatterboxTTS; print('Chatterbox OK')"
```

## 🆘 If Nothing Works

If you're still having issues:

1. **Complete environment reset**:
   ```bash
   conda env remove -n chatterbox
   ./setup_m1.sh
   ```

2. **Update macOS**: Ensure you have the latest macOS version for better Apple Silicon support

3. **Check available memory**: Make sure you have enough free RAM

4. **Try CPU-only mode**: Some M1 compatibility issues can be bypassed by using CPU instead of MPS

## 📞 Getting Help

If you continue to have issues:
- Check the main README.md for more troubleshooting
- Visit the Chatterbox GitHub issues page
- Ensure your macOS and Xcode Command Line Tools are updated

The most important thing is getting the PyTorch/TorchVision versions aligned properly for Apple Silicon! 🍎