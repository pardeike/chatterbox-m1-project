# Creating Synthetic Voices for Applications

## Overview

Chatterbox offers several approaches to create synthetic voices for your applications:

1. **Voice Cloning** - Clone existing voices (requires reference audio)
2. **Default Voice** - Use the built-in default voice (no reference needed)
3. **Voice Variations** - Create variations by adjusting parameters
4. **Custom Voice Library** - Build a library of synthetic voices for your app

---

## Method 1: Using the Default Synthetic Voice

The simplest approach - no reference audio needed:

```python
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

# Load model
model = ChatterboxTTS.from_pretrained(device="mps")

# Generate with default voice (no reference audio)
wav = model.generate(
    "This uses the default synthetic voice.",
    exaggeration=0.5,
    cfg_weight=0.5,
    temperature=0.7
)

ta.save("default_voice.wav", wav, model.sr)
```

**Use cases:**
- Narrator voices for applications
- System notifications
- Tutorial videos
- Background narration

---

## Method 2: Creating Voice Variations

Create different synthetic voice "characters" by adjusting parameters:

```python
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

model = ChatterboxTTS.from_pretrained(device="mps")

# Define different voice profiles
voice_profiles = {
    "professional": {
        "exaggeration": 0.3,
        "cfg_weight": 0.7,
        "temperature": 0.5
    },
    "enthusiastic": {
        "exaggeration": 0.8,
        "cfg_weight": 0.3,
        "temperature": 0.9
    },
    "calm_narrator": {
        "exaggeration": 0.4,
        "cfg_weight": 0.6,
        "temperature": 0.6
    },
    "dramatic": {
        "exaggeration": 0.9,
        "cfg_weight": 0.2,
        "temperature": 0.8
    }
}

# Generate with different profiles
text = "Welcome to our application."

for profile_name, params in voice_profiles.items():
    wav = model.generate(text, **params)
    ta.save(f"{profile_name}_voice.wav", wav, model.sr)
    print(f"Generated: {profile_name}")
```

---

## Method 3: Voice Library for Applications

Create a reusable library of synthetic voices:

```python
#!/usr/bin/env python3
"""
Voice Library Manager
Create and manage multiple synthetic voices for your application
"""

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import json
import os

class SyntheticVoiceLibrary:
    def __init__(self, device="mps"):
        self.model = ChatterboxTTS.from_pretrained(device=device)
        self.voices = {}
        self.load_voice_library()
    
    def load_voice_library(self, library_path="voice_library.json"):
        """Load voice profiles from JSON"""
        if os.path.exists(library_path):
            with open(library_path, 'r') as f:
                self.voices = json.load(f)
    
    def save_voice_library(self, library_path="voice_library.json"):
        """Save voice profiles to JSON"""
        with open(library_path, 'w') as f:
            json.dump(self.voices, f, indent=2)
    
    def create_voice(self, name, reference_audio=None, 
                    exaggeration=0.5, cfg_weight=0.5, temperature=0.7,
                    description=""):
        """
        Create a new synthetic voice profile
        
        Args:
            name: Unique identifier for this voice
            reference_audio: Optional path to reference audio for cloning
            exaggeration: Emotion level (0.0-1.0)
            cfg_weight: Speech control (0.0-1.0)
            temperature: Creativity (0.1-1.0)
            description: Human-readable description
        """
        self.voices[name] = {
            "reference_audio": reference_audio,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
            "description": description
        }
        self.save_voice_library()
        print(f"Voice '{name}' created successfully")
    
    def generate(self, text, voice_name, output_path=None):
        """
        Generate speech using a voice from the library
        
        Args:
            text: Text to synthesize
            voice_name: Name of voice profile to use
            output_path: Optional path to save audio
        
        Returns:
            audio tensor
        """
        if voice_name not in self.voices:
            raise ValueError(f"Voice '{voice_name}' not found in library")
        
        profile = self.voices[voice_name]
        
        # Generate audio
        wav = self.model.generate(
            text,
            audio_prompt_path=profile.get("reference_audio"),
            exaggeration=profile["exaggeration"],
            cfg_weight=profile["cfg_weight"],
            temperature=profile["temperature"]
        )
        
        # Save if output path provided
        if output_path:
            ta.save(output_path, wav, self.model.sr)
            print(f"Audio saved to: {output_path}")
        
        return wav
    
    def list_voices(self):
        """List all available voices"""
        print("\nAvailable Synthetic Voices:")
        print("-" * 50)
        for name, profile in self.voices.items():
            print(f"\n{name}:")
            print(f"  Description: {profile.get('description', 'N/A')}")
            print(f"  Has Reference: {'Yes' if profile.get('reference_audio') else 'No'}")
            print(f"  Parameters: ex={profile['exaggeration']}, "
                  f"cfg={profile['cfg_weight']}, temp={profile['temperature']}")

# Example usage
if __name__ == "__main__":
    # Create voice library
    library = SyntheticVoiceLibrary(device="mps")
    
    # Add different voice profiles
    library.create_voice(
        name="assistant",
        description="Professional assistant voice",
        exaggeration=0.4,
        cfg_weight=0.6,
        temperature=0.6
    )
    
    library.create_voice(
        name="narrator",
        description="Calm documentary narrator",
        exaggeration=0.3,
        cfg_weight=0.7,
        temperature=0.5
    )
    
    library.create_voice(
        name="character_excited",
        description="Enthusiastic character voice",
        exaggeration=0.8,
        cfg_weight=0.3,
        temperature=0.8
    )
    
    # If you have reference audio for specific characters
    library.create_voice(
        name="brand_voice",
        reference_audio="reference_audio/brand_voice.wav",
        description="Official brand voice",
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.7
    )
    
    # List all voices
    library.list_voices()
    
    # Use voices in your application
    library.generate(
        "Welcome to our application.",
        voice_name="assistant",
        output_path="welcome_message.wav"
    )
    
    library.generate(
        "This is an exciting new feature!",
        voice_name="character_excited",
        output_path="feature_announcement.wav"
    )
