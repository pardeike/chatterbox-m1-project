#!/usr/bin/env python3
"""
Chatterbox API Client Example
Demonstrates how to use the Chatterbox TTS server programmatically
Created by Claude for Michael Koker
"""

import requests
import json
from pathlib import Path
import time

class ChatterboxClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if the server is running and healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def synthesize(self, text, **kwargs):
        """
        Synthesize text to speech
        
        Args:
            text (str): Text to synthesize
            language (str): Language code (default: "en")
            exaggeration (float): Emotion level 0-1 (default: 0.5)
            cfg_weight (float): Speech control 0-1 (default: 0.5)
            temperature (float): Creativity 0.1-1.0 (default: 0.7)
            speed_factor (float): Speed multiplier 0.5-2.0 (default: 1.0)
            reference_audio_path (str): Path to reference audio for voice cloning
        
        Returns:
            bytes: Audio data in WAV format
        """
        url = f"{self.base_url}/synthesize"
        
        # Prepare form data
        data = {
            "text": text,
            "language": kwargs.get("language", "en"),
            "exaggeration": kwargs.get("exaggeration", 0.5),
            "cfg_weight": kwargs.get("cfg_weight", 0.5),
            "temperature": kwargs.get("temperature", 0.7),
            "speed_factor": kwargs.get("speed_factor", 1.0)
        }
        
        files = {}
        reference_audio_path = kwargs.get("reference_audio_path")
        if reference_audio_path and Path(reference_audio_path).exists():
            files["reference_audio"] = open(reference_audio_path, "rb")
        
        try:
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        finally:
            # Close any opened files
            for file in files.values():
                file.close()
    
    def clear_cache(self):
        """Clear the model cache on the server"""
        try:
            response = requests.post(f"{self.base_url}/clear_cache", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def main():
    print("🔌 Chatterbox API Client Example")
    print("=" * 35)
    
    # Initialize client
    client = ChatterboxClient()
    
    # Check server health
    print("🏥 Checking server health...")
    health = client.health_check()
    
    if "error" in health:
        print(f"❌ Server not reachable: {health['error']}")
        print("💡 Make sure to start the server first: ./start_server.sh")
        return
    
    print("✅ Server is healthy!")
    print(f"   Device: {health.get('device', 'unknown')}")
    print(f"   MPS Available: {health.get('mps_available', False)}")
    print(f"   Memory Usage: {health.get('memory_usage', 'unknown')}")
    
    # Example 1: Basic TTS
    print("\n🎙️  Example 1: Basic Text-to-Speech")
    text1 = "Hello! This is a test of the Chatterbox API client."
    print(f"Text: {text1}")
    
    try:
        start_time = time.time()
        audio_data = client.synthesize(text1)
        generation_time = time.time() - start_time
        
        # Save the audio
        output_file = "outputs/api_basic_example.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        
        print(f"✅ Generated in {generation_time:.2f} seconds")
        print(f"✅ Saved as: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Emotional TTS
    print("\n🎭 Example 2: Emotional Speech")
    text2 = "This is an exciting and dramatic example of emotional speech!"
    print(f"Text: {text2}")
    
    try:
        start_time = time.time()
        audio_data = client.synthesize(
            text2,
            exaggeration=0.8,
            cfg_weight=0.3,
            temperature=0.8
        )
        generation_time = time.time() - start_time
        
        output_file = "outputs/api_emotional_example.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        
        print(f"✅ Generated in {generation_time:.2f} seconds")
        print(f"✅ Saved as: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Voice Cloning (if reference audio exists)
    reference_files = list(Path("reference_audio").glob("*.wav"))
    if reference_files:
        print("\n🎭 Example 3: Voice Cloning")
        reference_file = reference_files[0]
        text3 = "Now I'm speaking with a cloned voice using the API!"
        print(f"Text: {text3}")
        print(f"Reference: {reference_file}")
        
        try:
            start_time = time.time()
            audio_data = client.synthesize(
                text3,
                reference_audio_path=str(reference_file),
                exaggeration=0.6,
                cfg_weight=0.4
            )
            generation_time = time.time() - start_time
            
            output_file = "outputs/api_cloned_example.wav"
            with open(output_file, "wb") as f:
                f.write(audio_data)
            
            print(f"✅ Generated in {generation_time:.2f} seconds")
            print(f"✅ Saved as: {output_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("\n⚠️  No reference audio found for voice cloning example")
    
    # Example 4: Multilingual
    print("\n🌍 Example 4: Multilingual Speech")
    multilingual_examples = [
        ("es", "¡Hola! Este es un ejemplo en español."),
        ("fr", "Bonjour! Ceci est un exemple en français."),
        ("de", "Hallo! Das ist ein Beispiel auf Deutsch."),
    ]
    
    for lang, text in multilingual_examples:
        print(f"   {lang.upper()}: {text}")
        try:
            audio_data = client.synthesize(text, language=lang)
            output_file = f"outputs/api_{lang}_example.wav"
            with open(output_file, "wb") as f:
                f.write(audio_data)
            print(f"   ✅ Saved as: {output_file}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 API client examples complete!")
    print("🎧 Check the 'outputs' folder for all generated audio files")
    
    # Clear cache example
    print("\n🧹 Clearing server cache...")
    result = client.clear_cache()
    if "error" not in result:
        print("✅ Cache cleared successfully")
    else:
        print(f"⚠️  Cache clear failed: {result['error']}")

if __name__ == "__main__":
    # Ensure outputs directory exists
    Path("outputs").mkdir(exist_ok=True)
    main()