# Using Cloned Voices in Other Applications

## Overview

You have three main ways to integrate Chatterbox voice cloning into other applications:

1. **HTTP API** - Best for any application (Python, JavaScript, etc.)
2. **Direct Python Library** - Best for Python applications
3. **Command Line** - Best for scripts and automation

---

## Method 1: HTTP API (Recommended for Most Use Cases)

Your server at `http://localhost:8000` exposes a REST API that any application can call.

### From Python:
```python
import requests

def generate_speech(text, reference_audio_path):
    response = requests.post(
        "http://localhost:8000/synthesize",
        data={
            "text": text,
            "exaggeration": 0.6,
            "cfg_weight": 0.4
        },
        files={"reference_audio": open(reference_audio_path, "rb")}
    )
    
    with open("output.wav", "wb") as f:
        f.write(response.content)
```

### From JavaScript/Node.js:
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function generateSpeech(text, referenceAudioPath) {
    const formData = new FormData();
    formData.append('text', text);
    formData.append('exaggeration', '0.6');
    formData.append('cfg_weight', '0.4');
    formData.append('reference_audio', fs.createReadStream(referenceAudioPath));
    
    const response = await axios.post('http://localhost:8000/synthesize', formData, {
        responseType: 'arraybuffer',
        headers: formData.getHeaders()
    });
    
    fs.writeFileSync('output.wav', response.data);
}
```

### From cURL (Command Line):
```bash
curl -X POST "http://localhost:8000/synthesize" \
     -F "text=Your text here" \
     -F "exaggeration=0.6" \
     -F "cfg_weight=0.4" \
     -F "reference_audio=@reference_audio/my_voice.wav" \
     --output output.wav
```

---

## Method 2: Direct Python Integration

If your application is in Python, you can import Chatterbox directly:

```python
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

# Initialize once
model = ChatterboxTTS.from_pretrained(device="mps")

# Generate speech with cloned voice
wav = model.generate(
    "Your text here",
    audio_prompt_path="reference_audio/my_voice.wav",
    exaggeration=0.6,
    cfg_weight=0.4
)

ta.save("output.wav", wav, model.sr)
```

**Benefits:**
- No HTTP overhead
- Faster for batch processing
- Direct control over model

**Drawbacks:**
- Python only
- Must manage model memory
- Requires conda environment

---

## Method 3: Command Line Script

Create a simple CLI tool:

```bash
#!/bin/bash
# voice_clone.sh

TEXT="$1"
REFERENCE_AUDIO="$2"
OUTPUT="${3:-output.wav}"

source $HOME/miniforge3/etc/profile.d/conda.sh
conda activate chatterbox

python -c "
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta
import sys

model = ChatterboxTTS.from_pretrained(device='mps')
wav = model.generate(
    '''$TEXT''',
    audio_prompt_path='$REFERENCE_AUDIO',
    exaggeration=0.6,
    cfg_weight=0.4
)
ta.save('$OUTPUT', wav, model.sr)
print('Generated: $OUTPUT')
"
```

Usage:
```bash
./voice_clone.sh "Hello world" "reference_audio/my_voice.wav" "output.wav"
```

---

## Best Practices for Reference Audio

### Recording Quality:
- **Duration**: 10-30 seconds (optimal)
- **Format**: WAV (44.1kHz or 48kHz)
- **Content**: Natural conversational speech
- **Environment**: Quiet room with minimal echo
- **Microphone**: Good quality USB or built-in Mac mic

### What to Record:
Read a paragraph that includes varied phonemes:
```
"Hello, this is a sample of my voice for cloning purposes. 
I'm speaking naturally and clearly, with normal pacing. 
The quick brown fox jumps over the lazy dog. 
This sentence contains various sounds and inflections 
that will help the AI model capture my unique voice characteristics."
```

### Recording Tips:
- Speak at normal conversational pace
- Avoid extreme emotions (unless you want that in the clone)
- Single speaker only (no background voices)
- Consistent distance from microphone
- No music or sound effects

---

## Integration Examples

### Example 1: Chatbot with Cloned Voice
```python
# chatbot.py
import requests

class VoiceBot:
    def __init__(self, voice_reference_path):
        self.voice_reference = voice_reference_path
        self.api_url = "http://localhost:8000/synthesize"
    
    def speak(self, text):
        response = requests.post(
            self.api_url,
            data={"text": text, "exaggeration": 0.5},
            files={"reference_audio": open(self.voice_reference, "rb")}
        )
        
        with open("response.wav", "wb") as f:
            f.write(response.content)
        
        # Play the audio (using macOS)
        import os
        os.system("afplay response.wav")

# Usage
bot = VoiceBot("reference_audio/assistant_voice.wav")
bot.speak("Hello, how can I help you today?")
```

### Example 2: Batch Processing
```python
# batch_generate.py
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

model = ChatterboxTTS.from_pretrained(device="mps")

scripts = [
    ("Chapter 1: The Beginning", "chapter1.wav"),
    ("Chapter 2: The Journey", "chapter2.wav"),
    ("Chapter 3: The End", "chapter3.wav")
]

for text, output_file in scripts:
    wav = model.generate(
        text,
        audio_prompt_path="narrator_voice.wav",
        exaggeration=0.6
    )
    ta.save(output_file, wav, model.sr)
    print(f"Generated: {output_file}")
```

### Example 3: Video Voiceover Integration
```python
# video_voiceover.py
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

def add_voiceover(video_path, script, voice_reference, output_path):
    # Generate voiceover
    response = requests.post(
        "http://localhost:8000/synthesize",
        data={"text": script},
        files={"reference_audio": open(voice_reference, "rb")}
    )
    
    with open("voiceover.wav", "wb") as f:
        f.write(response.content)
    
    # Add to video
    video = VideoFileClip(video_path)
    audio = AudioFileClip("voiceover.wav")
    video = video.set_audio(audio)
    video.write_videofile(output_path)

# Usage
add_voiceover(
    "video.mp4",
    "This is the narration for my video",
    "narrator_voice.wav",
    "video_with_voiceover.mp4"
)
```

---

## Important Considerations

### Legal and Ethical:
- **Consent Required**: Only clone voices with explicit permission
- **Disclosure**: Inform listeners when audio is AI-generated
- **No Impersonation**: Don't use for fraud or impersonation
- **Watermarking**: All generated audio includes watermarks (PerTh)

### Technical:
- **Server Must Be Running**: API requires the server at localhost:8000
- **Memory Usage**: ~3-4GB per model load
- **Performance**: First generation is slower (model loading)
- **MPS Fallback**: Enable with `export PYTORCH_ENABLE_MPS_FALLBACK=1`

### Quality Control:
- **Test First**: Always test with short samples
- **Adjust Parameters**:
  - `exaggeration` (0.0-1.0): Emotion intensity
  - `cfg_weight` (0.0-1.0): Speech control/speed
  - `temperature` (0.1-1.0): Creativity/variation
- **Reference Audio Quality**: Better input = better output

---

## API Documentation

Once your server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Web UI**: http://localhost:8000

---

## Troubleshooting

**Issue**: API not responding
**Fix**: Ensure server is running (`python server.py`)

**Issue**: Poor voice quality
**Fix**: Use higher quality reference audio (10-30 seconds)

**Issue**: Slow generation
**Fix**: Ensure MPS fallback is enabled, close other apps

**Issue**: Out of memory
**Fix**: Use shorter text, restart server to clear cache

---

For complete working examples, see the `scripts/` directory in your project.