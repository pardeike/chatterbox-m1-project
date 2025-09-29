# 🚀 Getting Started with Chatterbox TTS on M1 MacBook Air

## Quick Start (2 minutes)

1. **Open Terminal** and navigate to this project:
   ```bash
   cd ~/chatterbox-m1-project
   ```

2. **Run the launcher**:
   ```bash
   chmod +x launch.sh
   ./launch.sh
   ```

3. **Choose option 1** to install everything automatically

4. **Choose option 4** to start the web server, then open http://localhost:8000

## Step-by-Step Installation

### 1. Setup Environment
```bash
# Make setup script executable and run
chmod +x setup_m1.sh
./setup_m1.sh
```

This installs:
- Homebrew (if needed)
- Conda for ARM64
- PyTorch with MPS support
- Chatterbox TTS
- All dependencies

### 2. Test Basic Functionality
```bash
# Activate environment
conda activate chatterbox

# Test basic TTS
python examples/basic_example.py
```

### 3. Try Voice Cloning
```bash
# Add a voice sample to reference_audio/ folder
# Then run:
python examples/voice_cloning_example.py
```

### 4. Start Web Server
```bash
python server.py
# Open http://localhost:8000 in browser
```

## Usage Examples

### Python API
```python
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Load model
model = ChatterboxTTS.from_pretrained(device="mps")

# Generate speech
wav = model.generate("Hello from M1 MacBook Air!")
ta.save("output.wav", wav, model.sr)
```

### Voice Cloning
```python
# Clone voice with reference audio
wav = model.generate(
    "This is cloned speech!",
    audio_prompt_path="reference_audio/my_voice.wav",
    exaggeration=0.6
)
```

### HTTP API
```bash
# Start server first, then:
curl -X POST "http://localhost:8000/synthesize" \
     -F "text=Hello World!" \
     -F "exaggeration=0.7" \
     --output generated.wav
```

## File Structure
```
chatterbox-m1-project/
├── launch.sh              # Main launcher (start here!)
├── setup_m1.sh            # Installation script
├── server.py              # Web server
├── examples/               # Python examples
├── reference_audio/        # Voice samples for cloning
├── outputs/               # Generated audio files
├── static/                # Web interface
└── scripts/               # API client examples
```

## Performance Tips

### Optimal Settings
- **General use**: exaggeration=0.5, cfg_weight=0.5
- **Emotional**: exaggeration=0.8, cfg_weight=0.3
- **Fast speech**: cfg_weight=0.3, speed_factor=1.2

### M1 MacBook Air Specific
- Keep laptop plugged in for sustained performance
- Close memory-intensive apps (8GB models)
- Use shorter texts for faster generation
- Models cache in memory after first load

## Common Issues

### MPS Not Available
- Update macOS to latest version
- Falls back to CPU automatically
- Check with: `python -c "import torch; print(torch.backends.mps.is_available())"`

### Memory Issues
- Clear cache: `curl -X POST http://localhost:8000/clear_cache`
- Use shorter text chunks
- Restart server if memory grows

### Installation Problems
```bash
# Reset environment
conda env remove -n chatterbox
./setup_m1.sh
```

## Next Steps

1. **Voice Cloning**: Record your voice and add to `reference_audio/`
2. **API Integration**: Use `scripts/api_client_example.py` as reference
3. **Custom Applications**: Build on top of the server API
4. **Production**: Deploy with proper authentication and scaling

## Support

- Check the main README.md for comprehensive documentation
- Use the launcher's help option (option 7)
- Visit https://github.com/resemble-ai/chatterbox for Chatterbox issues

**Happy voice synthesis! 🎙️**