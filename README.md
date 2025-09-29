# Chatterbox TTS - M1 MacBook Air Deployment

A complete, production-ready deployment of [Resemble AI's Chatterbox](https://github.com/resemble-ai/chatterbox) text-to-speech system, optimized for Apple Silicon M1 MacBook Air.

## Features

- **State-of-the-art TTS**: Outperforms ElevenLabs in blind evaluations
- **Voice Cloning**: Clone any voice with 10-30 seconds of audio
- **Multilingual**: Supports 20+ languages
- **Apple Silicon Optimized**: Uses MPS acceleration for fast inference
- **Web Interface**: Beautiful, responsive UI for easy use
- **REST API**: Easy integration with other applications
- **Voice Library System**: Manage multiple synthetic voices
- **Memory Efficient**: Optimized for MacBook Air constraints
- **Built-in Watermarking**: All audio includes imperceptible watermarks

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Integration Examples](#integration-examples)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Prerequisites

- **Hardware**: Apple Silicon M1, M2, or M3 Mac
- **OS**: macOS 11.0 or later
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: ~5GB for models and dependencies
- **Python**: 3.11 (will be installed via conda)

## Quick Start

```bash
# Clone this repository
git clone https://github.com/mkoker/chatterbox-m1-project.git
cd chatterbox-m1-project

# Run the automated setup
chmod +x setup_m1.sh
./setup_m1.sh

# Start the server
export PYTORCH_ENABLE_MPS_FALLBACK=1
source $HOME/miniforge3/etc/profile.d/conda.sh
conda activate chatterbox
python server.py
```

Open http://localhost:8000 in your browser.

## Installation

### Automated Installation

The easiest way to get started:

```bash
./setup_m1.sh
```

This installs:
- Miniforge (conda for ARM64)
- PyTorch with MPS support
- Chatterbox TTS and all dependencies
- FastAPI server components

### Manual Installation

If you prefer manual control:

```bash
# Install Miniforge
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
bash Miniforge3-MacOSX-arm64.sh

# Create environment
conda create -n chatterbox python=3.11 -y
conda activate chatterbox

# Install PyTorch
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu

# Install Chatterbox and dependencies
pip install chatterbox-tts transformers==4.46.3
pip install fastapi uvicorn python-multipart psutil
```

### Troubleshooting Installation

If you encounter issues, see [PYTORCH_FIX.md](PYTORCH_FIX.md) for common solutions.

## Usage

### Web Interface

Start the server and access the web UI:

```bash
./start_server_with_fallback.sh
```

Then open http://localhost:8000

### Python API

```python
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

# Initialize model
model = ChatterboxTTS.from_pretrained(device="mps")

# Basic text-to-speech
wav = model.generate("Hello from Chatterbox!")
ta.save("output.wav", wav, model.sr)

# Voice cloning
wav = model.generate(
    "This is a cloned voice.",
    audio_prompt_path="reference_audio/my_voice.wav",
    exaggeration=0.6,
    cfg_weight=0.4
)
ta.save("cloned_output.wav", wav, model.sr)
```

### REST API

```bash
# Generate speech
curl -X POST "http://localhost:8000/synthesize" \
     -F "text=Hello world" \
     -F "exaggeration=0.6" \
     --output speech.wav

# With voice cloning
curl -X POST "http://localhost:8000/synthesize" \
     -F "text=Hello in cloned voice" \
     -F "reference_audio=@reference_audio/voice.wav" \
     --output cloned_speech.wav
```

### Command Line

```bash
# Using the voice library
python scripts/voice_library.py

# Direct voice cloning
python scripts/direct_voice_cloning.py

# API client example
python scripts/use_cloned_voice_api.py
```

## API Documentation

### Endpoints

**Web Interface**
- `GET /` - Web UI

**API**
- `POST /synthesize` - Generate speech
- `GET /health` - Health check
- `POST /clear_cache` - Clear model cache

**Interactive Docs**
- Visit http://localhost:8000/docs when server is running

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `text` | string | - | Text to synthesize (max 1000 chars) |
| `language` | string | - | Language code (en, es, fr, etc.) |
| `exaggeration` | float | 0.0-1.0 | Emotion/expression intensity |
| `cfg_weight` | float | 0.0-1.0 | Speech control (lower = faster) |
| `temperature` | float | 0.1-1.0 | Creativity/variation |
| `reference_audio` | file | - | Reference audio for voice cloning |

### Example Response

```json
{
  "status": "success",
  "audio": "binary_wav_data",
  "duration": 3.5,
  "sample_rate": 24000
}
```

## Integration Examples

### E-Learning Platform

```python
from chatterbox.tts import ChatterboxTTS

class CourseNarrator:
    def __init__(self):
        self.model = ChatterboxTTS.from_pretrained(device="mps")
    
    def narrate_lesson(self, text, output_path):
        wav = self.model.generate(text, exaggeration=0.4, cfg_weight=0.6)
        ta.save(output_path, wav, self.model.sr)
```

### Voice Assistant

```python
import requests

def speak(text):
    response = requests.post(
        "http://localhost:8000/synthesize",
        data={"text": text}
    )
    # Play audio
    with open("response.wav", "wb") as f:
        f.write(response.content)
```

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for more examples.

## Troubleshooting

### Common Issues

**Issue**: `operator torchvision::nms does not exist`  
**Fix**: Run `./definitive_fix.sh`

**Issue**: `rope_scaling` configuration error  
**Fix**: Run `pip install transformers==4.46.3 --force-reinstall`

**Issue**: MPS operation not supported  
**Fix**: Enable fallback with `export PYTORCH_ENABLE_MPS_FALLBACK=1`

**Issue**: Server won't start  
**Fix**: Initialize conda: `source $HOME/miniforge3/etc/profile.d/conda.sh`

See [PYTORCH_FIX.md](PYTORCH_FIX.md) for detailed troubleshooting.

## Project Structure

```
chatterbox-m1-project/
├── README.md                       # This file
├── setup_m1.sh                     # Automated setup script
├── server.py                       # Main web server
├── start_server_with_fallback.sh  # Server launcher with MPS fallback
├── requirements.txt                # Python dependencies
│
├── examples/                       # Usage examples
│   ├── basic_example.py
│   └── voice_cloning_example.py
│
├── scripts/                        # Integration scripts
│   ├── voice_library.py           # Voice management system
│   ├── api_service.py             # Standalone API service
│   ├── direct_voice_cloning.py    # Direct Python integration
│   └── use_cloned_voice_api.py    # API client example
│
├── static/                         # Web interface
│   └── index.html
│
├── reference_audio/                # Voice samples for cloning
│   └── README.md
│
├── outputs/                        # Generated audio files
│
└── docs/                          # Additional documentation
    ├── GETTING_STARTED.md
    ├── INTEGRATION_GUIDE.md
    ├── SYNTHETIC_VOICES_GUIDE.md
    └── PYTORCH_FIX.md
```

## Performance

### Expected Performance on M1 MacBook Air

- **Model Loading**: 30-60 seconds (first time only)
- **Generation Speed**: 2-5 seconds for short sentences
- **Memory Usage**: ~3-4GB
- **Voice Cloning**: Works with 10-30 second reference clips

### Optimization Tips

- Keep MacBook plugged in for sustained performance
- Close memory-intensive applications
- Use shorter text chunks for faster generation
- Models cache in memory after first load
- Enable MPS fallback for unsupported operations

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The underlying Chatterbox TTS model is also MIT licensed by Resemble AI.

## Acknowledgments

- **Resemble AI** for creating Chatterbox TTS
- **Chatterbox Model**: https://github.com/resemble-ai/chatterbox
- The open-source community for PyTorch, Transformers, and FastAPI

## Citation

If you use this project in your research or application, please cite:

```bibtex
@misc{chatterboxtts2025,
  author = {{Resemble AI}},
  title = {{Chatterbox-TTS}},
  year = {2025},
  howpublished = {\url{https://github.com/resemble-ai/chatterbox}},
  note = {GitHub repository}
}
```

## Support

- **Issues**: Open an issue on GitHub
- **Chatterbox Documentation**: https://github.com/resemble-ai/chatterbox
- **Discord**: https://discord.gg/rJq9cRJBJ6

## Legal and Ethical Use

- Only clone voices with explicit permission
- Disclose when audio is AI-generated
- All generated audio includes watermarks (PerTh)
- Do not use for impersonation or fraud
- Follow ethical AI guidelines

---

**Built with ❤️ for Apple Silicon**