#!/usr/bin/env python3
"""
REST API Service for Synthetic Voices
Provides a clean API interface for applications to use synthetic voices
"""

from flask import Flask, request, jsonify, send_file
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta
import io
import os

app = Flask(__name__)

# Initialize model (loaded once on startup)
print("Loading Chatterbox model...")
model = ChatterboxTTS.from_pretrained(device="mps")
print("Model loaded and ready")

# Voice profiles for your application
VOICE_PROFILES = {
    "default": {
        "exaggeration": 0.5,
        "cfg_weight": 0.5,
        "temperature": 0.7,
        "description": "Standard neutral voice"
    },
    "professional": {
        "exaggeration": 0.3,
        "cfg_weight": 0.7,
        "temperature": 0.5,
        "description": "Professional business voice"
    },
    "friendly": {
        "exaggeration": 0.6,
        "cfg_weight": 0.4,
        "temperature": 0.7,
        "description": "Warm and friendly voice"
    },
    "enthusiastic": {
        "exaggeration": 0.8,
        "cfg_weight": 0.3,
        "temperature": 0.8,
        "description": "Energetic and excited voice"
    },
    "narrator": {
        "exaggeration": 0.4,
        "cfg_weight": 0.6,
        "temperature": 0.6,
        "description": "Documentary-style narrator"
    }
}

@app.route('/api/voices', methods=['GET'])
def list_voices():
    """List all available voice profiles"""
    return jsonify({
        "voices": VOICE_PROFILES,
        "count": len(VOICE_PROFILES)
    })

@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    """
    Generate speech from text using a voice profile
    
    Request body (JSON):
    {
        "text": "Text to synthesize",
        "voice": "professional",  // optional, defaults to "default"
        "speed": 1.0  // optional speed adjustment (not all versions support this)
    }
    
    Returns: WAV audio file
    """
    try:
        # Parse request
        data = request.get_json()
        text = data.get('text')
        voice_name = data.get('voice', 'default')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        if voice_name not in VOICE_PROFILES:
            return jsonify({
                "error": f"Voice '{voice_name}' not found",
                "available_voices": list(VOICE_PROFILES.keys())
            }), 400
        
        # Get voice profile
        profile = VOICE_PROFILES[voice_name]
        
        # Generate audio
        wav = model.generate(
            text,
            exaggeration=profile["exaggeration"],
            cfg_weight=profile["cfg_weight"],
            temperature=profile["temperature"]
        )
        
        # Convert to bytes
        buffer = io.BytesIO()
        ta.save(buffer, wav, model.sr, format="wav")
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='generated.wav'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/synthesize/custom', methods=['POST'])
def synthesize_custom():
    """
    Generate speech with custom parameters
    
    Request body (JSON):
    {
        "text": "Text to synthesize",
        "exaggeration": 0.5,  // 0.0-1.0
        "cfg_weight": 0.5,    // 0.0-1.0
        "temperature": 0.7    // 0.1-1.0
    }
    
    Returns: WAV audio file
    """
    try:
        data = request.get_json()
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Get parameters (with defaults)
        exaggeration = float(data.get('exaggeration', 0.5))
        cfg_weight = float(data.get('cfg_weight', 0.5))
        temperature = float(data.get('temperature', 0.7))
        
        # Validate ranges
        if not (0 <= exaggeration <= 1):
            return jsonify({"error": "exaggeration must be between 0 and 1"}), 400
        if not (0 <= cfg_weight <= 1):
            return jsonify({"error": "cfg_weight must be between 0 and 1"}), 400
        if not (0.1 <= temperature <= 1):
            return jsonify({"error": "temperature must be between 0.1 and 1"}), 400
        
        # Generate audio
        wav = model.generate(
            text,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature
        )
        
        # Convert to bytes
        buffer = io.BytesIO()
        ta.save(buffer, wav, model.sr, format="wav")
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='generated.wav'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "available_voices": len(VOICE_PROFILES)
    })

if __name__ == '__main__':
    print("\nSynthetic Voice API Server")
    print("=" * 50)
    print("Available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /api/voices          - List available voices")
    print("  POST /api/synthesize      - Generate speech with preset voice")
    print("  POST /api/synthesize/custom - Generate with custom parameters")
    print("  GET  /api/health          - Health check")
    print("\n" + "=" * 50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
