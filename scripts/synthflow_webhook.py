#!/usr/bin/env python3
"""
Webhook endpoint compatible with voice AI platforms
Designed to integrate Chatterbox with platforms like Synthflow.ai
"""

from flask import Flask, request, jsonify, send_file
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta
import io
import base64
import os

app = Flask(__name__)

# Initialize model once
print("Loading Chatterbox model...")
model = ChatterboxTTS.from_pretrained(device="mps")
print("Model ready")

@app.route('/webhook/tts', methods=['POST'])
def webhook_tts():
    """
    Webhook endpoint for voice AI platforms
    
    Expected request format:
    {
        "text": "Text to synthesize",
        "voice_id": "optional_voice_identifier",
        "return_format": "base64" or "url"
    }
    
    Returns:
    {
        "audio": "base64_encoded_audio" or "url_to_audio",
        "format": "wav",
        "duration": 3.5
    }
    """
    try:
        data = request.get_json()
        text = data.get('text')
        return_format = data.get('return_format', 'base64')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Voice parameters (can be customized per voice_id)
        voice_id = data.get('voice_id', 'default')
        params = get_voice_params(voice_id)
        
        # Generate audio
        wav = model.generate(text, **params)
        
        # Calculate duration
        duration = wav.shape[-1] / model.sr
        
        # Return based on requested format
        if return_format == 'base64':
            # Encode as base64 for direct transmission
            buffer = io.BytesIO()
            ta.save(buffer, wav, model.sr, format="wav")
            buffer.seek(0)
            
            audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            return jsonify({
                "audio": audio_base64,
                "format": "wav",
                "duration": duration,
                "sample_rate": model.sr
            })
        
        elif return_format == 'file':
            # Save and return file
            buffer = io.BytesIO()
            ta.save(buffer, wav, model.sr, format="wav")
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype='audio/wav',
                as_attachment=True,
                download_name='speech.wav'
            )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_voice_params(voice_id):
    """Map voice IDs to parameters"""
    voice_profiles = {
        "default": {
            "exaggeration": 0.5,
            "cfg_weight": 0.5,
            "temperature": 0.7
        },
        "professional": {
            "exaggeration": 0.3,
            "cfg_weight": 0.7,
            "temperature": 0.5
        },
        "friendly": {
            "exaggeration": 0.6,
            "cfg_weight": 0.4,
            "temperature": 0.7
        },
        "calm": {
            "exaggeration": 0.4,
            "cfg_weight": 0.6,
            "temperature": 0.6
        }
    }
    
    return voice_profiles.get(voice_id, voice_profiles["default"])

@app.route('/webhook/voices', methods=['GET'])
def list_voices():
    """List available voices for the platform"""
    return jsonify({
        "voices": [
            {"id": "default", "name": "Default Voice", "language": "en"},
            {"id": "professional", "name": "Professional Voice", "language": "en"},
            {"id": "friendly", "name": "Friendly Voice", "language": "en"},
            {"id": "calm", "name": "Calm Voice", "language": "en"}
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "chatterbox-tts-webhook",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Chatterbox TTS Webhook Server for Voice AI Platforms")
    print("="*60)
    print("\nWebhook URL: http://localhost:5001/webhook/tts")
    print("Voices URL:  http://localhost:5001/webhook/voices")
    print("Health URL:  http://localhost:5001/health")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
