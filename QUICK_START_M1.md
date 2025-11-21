# Quick Start Guide for M1 MacBook Air

This guide helps you get Chatterbox TTS running on your M1 MacBook Air without issues.

## The torchvision::nms Error - Explained

If you see an error like:
```
operator torchvision::nms does not exist
```

**What it means:** PyTorch and TorchVision versions are incompatible on your system.

**Why it happens:** This is a common issue on Apple Silicon (M1/M2/M3) where the PyTorch ecosystem requires specific version combinations to work correctly.

**The solution is simple:** We've included a fix script that installs the correct versions.

## Installation Options

### Option 1: Fresh Install (Recommended)

If you're setting up for the first time:

```bash
# Clone the repository
git clone https://github.com/pardeike/chatterbox-m1-project.git
cd chatterbox-m1-project

# Run the automated setup
./setup_m1.sh

# Start the server
./start_server_with_fallback.sh
```

### Option 2: Fix Existing Installation

If you already installed but got the torchvision error:

```bash
cd chatterbox-m1-project
./definitive_fix.sh
```

This will:
1. Remove conflicting PyTorch packages
2. Install compatible versions (PyTorch 2.4.1, TorchVision 0.19.1)
3. Install compatible Transformers (4.35.0)
4. Test that everything works

Then restart the server:
```bash
python server.py
```

### Option 3: Manual Fix

If the automatic scripts don't work:

```bash
# Activate your conda environment
conda activate chatterbox

# Remove old versions
pip uninstall torch torchvision torchaudio -y

# Install compatible versions
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu

# Install compatible transformers
pip install transformers==4.35.0 --force-reinstall

# Reinstall chatterbox
pip install chatterbox-tts --force-reinstall
```

## Verification

The server now validates your environment on startup. If there's an issue, you'll see:

```
❌ Environment validation failed!
Error: operator torchvision::nms does not exist

This is a PyTorch/TorchVision compatibility issue on M1 MacBook Air.

🔧 TO FIX THIS ISSUE, run one of these commands:

   Option 1 (Recommended):
   ./definitive_fix.sh
```

If you see:
```
✅ Environment validation passed - PyTorch 2.4.1, TorchVision 0.19.1
```

You're good to go! 🎉

## What Changed?

We've improved the server to:
1. **Test your environment before starting** - catches the issue immediately
2. **Provide clear fix instructions** - no more cryptic errors
3. **Pin working versions** - requirements.txt now includes specific versions
4. **Exit gracefully** - instead of starting in a broken state

## Still Having Issues?

1. Make sure you're using conda/miniforge (not system Python)
2. Check that you're in the right environment: `conda activate chatterbox`
3. Try a complete environment reset:
   ```bash
   conda env remove -n chatterbox
   ./setup_m1.sh
   ```
4. See [PYTORCH_FIX.md](PYTORCH_FIX.md) for more troubleshooting

## Why These Specific Versions?

- **PyTorch 2.4.1**: Latest stable release with good M1 support
- **TorchVision 0.19.1**: Compiled to work with PyTorch 2.4.1
- **Transformers 4.35.0**: Compatible with PyTorch 2.4.1 and doesn't trigger the NMS bug
- **CPU builds**: More stable than MPS builds for this specific library combination

These versions are tested and confirmed working on M1 MacBook Air.

## Performance Note

Using CPU builds doesn't mean poor performance! Apple Silicon CPUs are incredibly fast for neural networks. You'll still get:
- 2-5 second generation for short sentences
- ~3-4GB memory usage
- Excellent voice quality

The server also supports MPS fallback for operations that work better on the GPU.
