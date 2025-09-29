#!/usr/bin/env python3
"""
Chatterbox TTS API Client
Simple client for interacting with the Chatterbox server
"""

import requests
import json
from pathlib import Path
import time

class ChatterboxClient:
    """Simple API client for Chatterbox TTS Server"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Check server health and status"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def synthesize(self, text, language="en", exaggeration=0.5, cfg_weight=0.5, 
                  reference_audio_path=None, output_path="generated.wav"):
        """
        Synthesize text to speech
        
        Args:
            text: Text to synthesize
            language: Language code (en, es, fr, de, etc.)
            exaggeration: Emotion level (0.0-1.0)
            cfg_weight: Speed control (0.0-1.0, lower = faster)
            reference_audio_path: Path to reference audio for voice cloning
            output_path: Where to save the generated audio
        
        Returns:
            dict: Result information
        """
        data = {
            "text": text,
            "language": language,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight
        }
        
        files = {}
        if reference_audio_path and Path(reference_audio_path).exists():
            files["reference_audio"] = open(reference_audio_path, "rb")
        
        try:
            print(f"🎙️ Generating audio for: {text[:50]}...")
            start_time = time.time()
            
            response = self.session.post(
                f"{self.base_url}/synthesize",
                data=data,
                files=files,
                stream=True
            )
            response.raise_for_status()
            
            # Save audio file
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            generation_time = time.time() - start_time
            
            return {
                "success": True,
                "output_path": output_path,
                "generation_time": generation_time,
                "file_size": Path(output_path).stat().st_size
            }
            
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
        
        finally:
            # Close file if it was opened
            for file in files.values():
                file.close()
    
    def clear_cache(self):
        """Clear server model cache"""
        try:
            response = self.session.post(f"{self.base_url}/clear_cache")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_api_info(self):
        """Get API information"""
        try:
            response = self.session.get(f"{self.base_url}/api/info")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

def main():
    """Example usage of the API client"""
    print("🍎 Chatterbox TTS API Client Example")
    print("=" * 40)
    
    # Initialize client
    client = ChatterboxClient()
    
    # Check server health
    print("🔍 Checking server health...")
    health = client.health_check()
    
    if "error" in health:
        print(f"❌ Server not available: {health['error']}")
        print("Please start the server with: ./start_server.sh")
        return
    
    print(f"✅ Server healthy!")
    print(f"   Device: {health.get('device', 'unknown')}")
    print(f"   Memory: {health.get('memory_usage_percent', 0)}%")
    print(f"   MPS Available: {health.get('mps_available', False)}")
    
    # Get API info
    print("\n📋 Getting API information...")
    api_info = client.get_api_info()
    if "error" not in api_info:
        print(f"   Version: {api_info.get('version', 'unknown')}")
        print(f"   Features: {len(api_info.get('features', []))} available")
        print(f"   Languages: {len(api_info.get('supported_languages', []))} supported")
    
    # Example 1: Basic TTS
    print("\n🎙️ Example 1: Basic text-to-speech")
    result = client.synthesize(
        text="Hello! This is a test of the Chatterbox API client on M1 MacBook Air.",
        output_path="api_client_basic.wav"
    )
    
    if result["success"]:
        print(f"✅ Generated: {result['output_path']}")
        print(f"   Time: {result['generation_time']:.2f}s")
        print(f"   Size: {result['file_size'] / 1024:.1f} KB")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 2: Different language
    print("\n🌍 Example 2: Spanish TTS")
    result = client.synthesize(
        text="¡Hola! Este es un ejemplo en español.",
        language="es",
        exaggeration=0.7,
        output_path="api_client_spanish.wav"
    )
    
    if result["success"]:
        print(f"✅ Generated Spanish audio: {result['output_path']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 3: Voice cloning (if reference audio exists)
    reference_files = ["reference_voice.wav", "audio_samples/reference_voice.wav"]
    reference_audio = None
    
    for ref_file in reference_files:
        if Path(ref_file).exists():
            reference_audio = ref_file
            break
    
    if reference_audio:
        print(f"\n🎭 Example 3: Voice cloning with {reference_audio}")
        result = client.synthesize(
            text="This is an example of voice cloning using the API client!",
            reference_audio_path=reference_audio,
            exaggeration=0.6,
            cfg_weight=0.4,
            output_path="api_client_cloned.wav"
        )
        
        if result["success"]:
            print(f"✅ Generated cloned voice: {result['output_path']}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print("\n⚠️ No reference audio found for voice cloning example")
        print("   Add 'reference_voice.wav' to test voice cloning")
    
    # Show generated files
    print("\n📁 Generated files:")
    for file_pattern in ["api_client_*.wav"]:
        import glob
        for file_path in glob.glob(file_pattern):
            size = Path(file_path).stat().st_size / 1024
            print(f"   🎵 {file_path} ({size:.1f} KB)")
    
    print("\n🎉 API client examples completed!")
    print("💡 You can integrate this client into your own applications")

if __name__ == "__main__":
    main()
