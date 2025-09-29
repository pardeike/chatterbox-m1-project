# Creating Synthetic Voices for Applications - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Voice Creation Methods](#voice-creation-methods)
3. [Application Examples](#application-examples)
4. [Integration Patterns](#integration-patterns)
5. [Best Practices](#best-practices)
6. [Ethical Guidelines](#ethical-guidelines)

---

## Overview

Chatterbox allows you to create synthetic voices for applications in three ways:

1. **Default Synthetic Voice** - Use the built-in voice (no reference needed)
2. **Parameter-Based Variations** - Create unique voices by adjusting parameters
3. **Voice Cloning** - Create voices from reference audio samples

---

## Voice Creation Methods

### Method 1: Default Synthetic Voice

The simplest approach - generates speech without any reference audio:

**Via API:**
```bash
curl -X POST "http://localhost:8000/synthesize" \
     -F "text=Hello from a synthetic voice" \
     -F "exaggeration=0.5" \
     -F "cfg_weight=0.5" \
     --output synthetic_voice.wav
```

**Via Python:**
```python
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

model = ChatterboxTTS.from_pretrained(device="mps")
wav = model.generate("Hello from a synthetic voice")
ta.save("output.wav", wav, model.sr)
```

### Method 2: Parameter-Based Voice Variations

Create distinct synthetic voice "characters" by adjusting three parameters:

| Parameter | Range | Effect |
|-----------|-------|--------|
| `exaggeration` | 0.0-1.0 | Emotion/expression intensity |
| `cfg_weight` | 0.0-1.0 | Speech control (lower = faster) |
| `temperature` | 0.1-1.0 | Creativity/variation |

**Voice Character Examples:**

```python
# Professional business voice
professional = {
    "exaggeration": 0.3,
    "cfg_weight": 0.7,
    "temperature": 0.5
}

# Enthusiastic presenter
enthusiastic = {
    "exaggeration": 0.8,
    "cfg_weight": 0.3,
    "temperature": 0.9
}

# Calm narrator
narrator = {
    "exaggeration": 0.4,
    "cfg_weight": 0.6,
    "temperature": 0.6
}

# Dramatic character
dramatic = {
    "exaggeration": 0.9,
    "cfg_weight": 0.2,
    "temperature": 0.8
}
```

### Method 3: Voice Cloning

Create synthetic voices from reference audio:

```python
# Clone a specific voice
wav = model.generate(
    "Text in cloned voice",
    audio_prompt_path="reference_audio/voice_sample.wav",
    exaggeration=0.6,
    cfg_weight=0.4
)
```

**Reference Audio Requirements:**
- Duration: 10-30 seconds optimal
- Format: WAV, 44.1kHz or 48kHz
- Quality: Clean, minimal background noise
- Content: Natural conversational speech
- Single speaker only

---

## Application Examples

### Example 1: E-Learning Platform

Create different synthetic voices for different course topics:

```python
class CourseNarrator:
    def __init__(self):
        self.model = ChatterboxTTS.from_pretrained(device="mps")
        
        self.subjects = {
            "science": {"exaggeration": 0.4, "cfg_weight": 0.6, "temperature": 0.6},
            "history": {"exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.7},
            "math": {"exaggeration": 0.3, "cfg_weight": 0.7, "temperature": 0.5},
            "art": {"exaggeration": 0.7, "cfg_weight": 0.4, "temperature": 0.8}
        }
    
    def narrate_lesson(self, subject, text, output_path):
        params = self.subjects.get(subject, self.subjects["science"])
        wav = self.model.generate(text, **params)
        ta.save(output_path, wav, self.model.sr)

# Usage
narrator = CourseNarrator()
narrator.narrate_lesson("science", "The water cycle consists of...", "lesson1.wav")
```

### Example 2: Mobile App with Voice Notifications

```python
class AppVoiceNotifications:
    def __init__(self):
        self.api_url = "http://localhost:8000/synthesize"
        
        # Different notification types
        self.notification_voices = {
            "success": {"exaggeration": 0.7, "cfg_weight": 0.4},
            "error": {"exaggeration": 0.5, "cfg_weight": 0.6},
            "info": {"exaggeration": 0.4, "cfg_weight": 0.5},
            "warning": {"exaggeration": 0.6, "cfg_weight": 0.5}
        }
    
    def notify(self, message, notification_type="info"):
        params = self.notification_voices[notification_type]
        
        response = requests.post(
            self.api_url,
            data={"text": message, **params}
        )
        
        # Play audio in app
        self.play_audio(response.content)
    
    def play_audio(self, audio_data):
        # Implementation depends on your platform
        # iOS: AVAudioPlayer
        # Android: MediaPlayer
        # Web: HTML5 Audio
        pass
```

### Example 3: Video Game Character Voices

```python
class GameCharacterVoices:
    def __init__(self):
        self.model = ChatterboxTTS.from_pretrained(device="mps")
        
        # Different character archetypes
        self.characters = {
            "hero": {
                "exaggeration": 0.6,
                "cfg_weight": 0.5,
                "reference": "characters/hero_voice.wav"
            },
            "villain": {
                "exaggeration": 0.8,
                "cfg_weight": 0.3,
                "reference": "characters/villain_voice.wav"
            },
            "narrator": {
                "exaggeration": 0.4,
                "cfg_weight": 0.6,
                "reference": None  # Use default voice
            },
            "npc_merchant": {
                "exaggeration": 0.7,
                "cfg_weight": 0.4,
                "reference": "characters/merchant_voice.wav"
            }
        }
    
    def speak(self, character_name, dialogue, output_path):
        if character_name not in self.characters:
            raise ValueError(f"Unknown character: {character_name}")
        
        char = self.characters[character_name]
        
        wav = self.model.generate(
            dialogue,
            audio_prompt_path=char["reference"],
            exaggeration=char["exaggeration"],
            cfg_weight=char["cfg_weight"]
        )
        
        ta.save(output_path, wav, self.model.sr)
        return output_path

# Usage
voices = GameCharacterVoices()
voices.speak("hero", "I must save the kingdom!", "hero_line1.wav")
voices.speak("villain", "You'll never stop me!", "villain_line1.wav")
```

### Example 4: Podcast/Audiobook Production

```python
class AudiobookProducer:
    def __init__(self):
        self.model = ChatterboxTTS.from_pretrained(device="mps")
    
    def produce_chapter(self, text, narrator_voice_path, output_path):
        """
        Process long-form content with proper pacing
        """
        # Split into manageable chunks
        chunks = self.split_text(text, max_chars=200)
        audio_segments = []
        
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}")
            
            wav = self.model.generate(
                chunk,
                audio_prompt_path=narrator_voice_path,
                exaggeration=0.4,  # Calm narration
                cfg_weight=0.6,    # Deliberate pacing
                temperature=0.6
            )
            
            audio_segments.append(wav)
            
            # Add brief pause between segments
            silence = torch.zeros((1, int(self.model.sr * 0.3)))  # 300ms
            audio_segments.append(silence)
        
        # Concatenate all segments
        final_audio = torch.cat(audio_segments, dim=-1)
        ta.save(output_path, final_audio, self.model.sr)
        
        return output_path
    
    def split_text(self, text, max_chars=200):
        """Split text at sentence boundaries"""
        import re
        sentences = re.split(r'([.!?]+)', text)
        
        chunks = []
        current_chunk = ""
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i] + sentences[i+1]
            
            if len(current_chunk) + len(sentence) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
```

### Example 5: Accessibility Tool (Screen Reader)

```python
class AccessibleScreenReader:
    def __init__(self):
        self.api_url = "http://localhost:8000/synthesize"
        
        # Optimized for clarity
        self.voice_params = {
            "exaggeration": 0.3,  # Clear, not dramatic
            "cfg_weight": 0.7,    # Deliberate pacing
            "temperature": 0.5    # Consistent
        }
    
    def read_text(self, text, play_audio=True):
        """Read text aloud with clear pronunciation"""
        response = requests.post(
            self.api_url,
            data={"text": text, **self.voice_params}
        )
        
        if response.ok:
            if play_audio:
                self.play_audio(response.content)
            return response.content
        
        return None
    
    def read_ui_element(self, element_type, element_text):
        """Read UI elements with appropriate context"""
        prefix = {
            "button": "Button:",
            "link": "Link:",
            "heading": "Heading:",
            "input": "Input field:"
        }.get(element_type, "")
        
        full_text = f"{prefix} {element_text}"
        return self.read_text(full_text)
```

---

## Integration Patterns

### Pattern 1: Microservice Architecture

```python
# voice_service.py - Dedicated voice synthesis microservice
from fastapi import FastAPI
from chatterbox.tts import ChatterboxTTS

app = FastAPI()
model = ChatterboxTTS.from_pretrained(device="mps")

@app.post("/generate")
async def generate_voice(text: str, voice_profile: str = "default"):
    # Generate and return audio
    wav = model.generate(text, **PROFILES[voice_profile])
    return StreamingResponse(audio_stream(wav))

# Other microservices can call this service
# Example: user_service -> voice_service -> returns audio
```

### Pattern 2: Background Job Processing

```python
# For generating large volumes of synthetic voices
from celery import Celery
from chatterbox.tts import ChatterboxTTS

app = Celery('voice_tasks')
model = ChatterboxTTS.from_pretrained(device="mps")

@app.task
def generate_voice_async(text, voice_params, output_path):
    """Generate voice in background"""
    wav = model.generate(text, **voice_params)
    ta.save(output_path, wav, model.sr)
    return output_path

# Usage
result = generate_voice_async.delay(
    "Long text...",
    {"exaggeration": 0.5},
    "output.wav"
)
```

### Pattern 3: Caching Layer

```python
import hashlib
import os

class VoiceCacheManager:
    def __init__(self, cache_dir="voice_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.model = ChatterboxTTS.from_pretrained(device="mps")
    
    def get_cache_key(self, text, params):
        """Generate cache key from text and parameters"""
        key_str = f"{text}_{params}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def generate_cached(self, text, **params):
        """Generate or retrieve from cache"""
        cache_key = self.get_cache_key(text, str(params))
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        
        if os.path.exists(cache_path):
            print(f"Cache hit: {cache_key}")
            return cache_path
        
        # Generate new audio
        print(f"Cache miss: {cache_key}, generating...")
        wav = self.model.generate(text, **params)
        ta.save(cache_path, wav, self.model.sr)
        
        return cache_path
```

---

## Best Practices

### 1. Performance Optimization

```python
# Load model once and reuse
class VoiceGenerator:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model = ChatterboxTTS.from_pretrained(device="mps")
        return cls._instance
    
    def generate(self, text, **params):
        return self._model.generate(text, **params)

# Use singleton pattern
generator = VoiceGenerator()
```

### 2. Error Handling

```python
def safe_voice_generation(text, max_retries=3):
    """Generate voice with retry logic"""
    for attempt in range(max_retries):
        try:
            wav = model.generate(text)
            return wav
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(f"Failed after {max_retries} attempts: {e}")
                raise
            logging.warning(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(1)
```

### 3. Text Preprocessing

```python
def preprocess_text_for_tts(text):
    """Clean and prepare text for TTS"""
    import re
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Expand common abbreviations
    replacements = {
        'Dr.': 'Doctor',
        'Mr.': 'Mister',
        'Mrs.': 'Missus',
        'etc.': 'etcetera',
        'vs.': 'versus'
    }
    
    for abbr, full in replacements.items():
        text = text.replace(abbr, full)
    
    # Handle numbers
    text = re.sub(r'\b(\d+)\b', lambda m: num2words(int(m.group(1))), text)
    
    return text
```

### 4. Quality Assurance

```python
def validate_audio_output(audio_path):
    """Check generated audio quality"""
    import librosa
    
    # Load audio
    y, sr = librosa.load(audio_path)
    
    # Check duration
    duration = librosa.get_duration(y=y, sr=sr)
    if duration < 0.5:
        return False, "Audio too short"
    
    # Check for silence
    rms = librosa.feature.rms(y=y)[0]
    if np.mean(rms) < 0.01:
        return False, "Audio is silent"
    
    return True, "Audio valid"
```

---

## Ethical Guidelines

### Legal Requirements

1. **Consent**: Obtain explicit permission before cloning someone's voice
2. **Disclosure**: Clearly indicate when audio is AI-generated
3. **Usage Rights**: Respect voice ownership and usage restrictions
4. **No Impersonation**: Don't use for fraud or deception

### Best Practices

- **Watermarking**: All Chatterbox audio includes imperceptible watermarks
- **Attribution**: Credit when using synthetic voices
- **Transparency**: Be open about AI usage
- **Responsible Use**: Consider societal impact

### Application-Specific Guidelines

**Accessibility Tools**: ✅ Acceptable
**Educational Content**: ✅ Acceptable (with disclosure)
**Entertainment**: ✅ Acceptable (with consent if cloning)
**News/Journalism**: ⚠️ Use carefully, always disclose
**Fraud/Impersonation**: ❌ Never acceptable
**Political Content**: ⚠️ Requires disclosure and consent

---

## Resources

- **Voice Library Script**: `scripts/voice_library.py`
- **API Service**: `scripts/api_service.py`
- **Examples**: `examples/` directory
- **API Documentation**: http://localhost:8000/docs (when server running)

For more information, see:
- `INTEGRATION_GUIDE.md` - API integration details
- `README.md` - General documentation
- `GETTING_STARTED.md` - Quick start guide