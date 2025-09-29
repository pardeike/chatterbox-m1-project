#!/usr/bin/env python3
"""
Example: Using Chatterbox TTS API from another application
"""

import requests
import os

def generate_speech_with_cloned_voice(text, reference_audio_path, output_path="output.wav"):
    """
    Generate speech using a cloned voice via the API
    
    Args:
        text: Text to synthesize
        reference_audio_path: Path to the reference audio file for voice cloning
        output_path: Where to save the generated audio
    """
    url = "http://localhost:8000/synthesize"
    
    # Prepare the request
    data = {
        "text": text,
        "language": "en",
        "exaggeration": 0.6,
        "cfg_weight": 0.4,
        "temperature": 0.7
    }
    
    files = {}
    if reference_audio_path and os.path.exists(reference_audio_path):
        files["reference_audio"] = open(reference_audio_path, "rb")
    
    try:
        # Send request to API
        response = requests.post(url, data=data, files=files, timeout=60)
        response.raise_for_status()
        
        # Save the audio
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"Audio saved to: {output_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
    finally:
        # Close file if opened
        if files:
            files["reference_audio"].close()

# Example usage
if __name__ == "__main__":
    # Generate speech with a cloned voice
    generate_speech_with_cloned_voice(
        text="This is a test of voice cloning from another application.",
        reference_audio_path="reference_audio/my_voice.wav",
        output_path="cloned_output.wav"
    )