#!/usr/bin/env python3
"""
Chatterbox TTS Server optimized for M1 MacBook Air
Features:
- Memory-efficient lazy loading
- MPS acceleration support
- Simple web UI
- RESTful API
- Voice cloning support
- Multilingual support
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import torchaudio as ta
import torch
import uvicorn
import io
import os
import tempfile
import asyncio
from pathlib import Path
import logging
import psutil
import time
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Chatterbox TTS Server (M1 Optimized)",
    description="Voice cloning and text-to-speech server optimized for Apple Silicon",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model cache (lazy loading for memory efficiency)
_model_cache = {}
_multilingual_model_cache = {}

def get_device():
    """Get optimal device for M1 MacBook Air"""
    if torch.backends.mps.is_available():
        logger.info("Using MPS (Apple Silicon GPU) acceleration")
        return "mps"
    else:
        logger.warning("MPS not available, falling back to CPU")
        return "cpu"

def get_system_info():
    """Get system information for monitoring"""
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        "device": get_device(),
        "mps_available": torch.backends.mps.is_available(),
        "memory_total_gb": round(memory.total / (1024**3), 1),
        "memory_available_gb": round(memory.available / (1024**3), 1),
        "memory_usage_percent": memory.percent,
        "cpu_usage_percent": cpu_percent,
        "models_loaded": {
            "english": "english" in _model_cache,
            "multilingual": "multilingual" in _multilingual_model_cache
        }
    }

async def get_model(multilingual=False):
    """Lazy load model with caching"""
    cache_key = "multilingual" if multilingual else "english"
    cache = _multilingual_model_cache if multilingual else _model_cache
    
    if cache_key not in cache:
        logger.info(f"Loading {cache_key} model...")
        start_time = time.time()
        
        try:
            if multilingual:
                from chatterbox.mtl_tts import ChatterboxMultilingualTTS
                model = ChatterboxMultilingualTTS.from_pretrained(device=get_device())
            else:
                from chatterbox.tts import ChatterboxTTS
                model = ChatterboxTTS.from_pretrained(device=get_device())
            
            cache[cache_key] = model
            load_time = time.time() - start_time
            logger.info(f"✅ {cache_key.title()} model loaded in {load_time:.1f} seconds")
        except Exception as e:
            logger.error(f"Failed to load {cache_key} model: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")
    
    return cache[cache_key]

@app.get("/", response_class=HTMLResponse)
async def root():
    """Simple web interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🍎 Chatterbox TTS - M1 MacBook Air</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 20px;
                background: #f5f5f7;
                color: #1d1d1f;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .container { 
                background: white; 
                padding: 24px; 
                border-radius: 12px; 
                margin: 20px 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .form-group {
                margin: 16px 0;
            }
            label {
                display: block;
                font-weight: 600;
                margin-bottom: 8px;
                color: #1d1d1f;
            }
            textarea, input, select { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e5e5e7;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s;
            }
            textarea:focus, input:focus, select:focus {
                outline: none;
                border-color: #007AFF;
            }
            textarea { 
                height: 120px; 
                resize: vertical;
                font-family: inherit;
            }
            .slider-container {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .slider {
                flex: 1;
            }
            .slider-value {
                min-width: 40px;
                font-weight: 600;
                color: #007AFF;
            }
            button { 
                background: #007AFF; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: background-color 0.2s;
                margin: 8px 8px 8px 0;
            }
            button:hover { 
                background: #0056CC; 
            }
            button:disabled {
                background: #c7c7cc;
                cursor: not-allowed;
            }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin: 16px 0;
            }
            .status-item {
                background: #f6f6f6;
                padding: 12px;
                border-radius: 8px;
                text-align: center;
            }
            .status-value {
                font-size: 24px;
                font-weight: 700;
                color: #007AFF;
            }
            .status-label {
                font-size: 14px;
                color: #86868b;
                margin-top: 4px;
            }
            #result {
                margin-top: 20px;
                padding: 16px;
                background: #f6f6f6;
                border-radius: 8px;
                min-height: 60px;
            }
            .audio-player {
                width: 100%;
                margin: 16px 0;
            }
            .download-link {
                display: inline-block;
                color: #007AFF;
                text-decoration: none;
                font-weight: 600;
                padding: 8px 16px;
                border: 2px solid #007AFF;
                border-radius: 8px;
                transition: all 0.2s;
            }
            .download-link:hover {
                background: #007AFF;
                color: white;
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #007AFF;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .tip {
                background: #e8f4fd;
                border-left: 4px solid #007AFF;
                padding: 16px;
                margin: 16px 0;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🍎 Chatterbox TTS</h1>
            <p>Voice Cloning & Text-to-Speech • Optimized for M1 MacBook Air</p>
        </div>
        
        <div class="container">
            <h3>🎙️ Text-to-Speech Generator</h3>
            <form id="ttsForm">
                <div class="form-group">
                    <label for="text">Text to synthesize:</label>
                    <textarea id="text" placeholder="Enter your text here (max 1000 characters)..." required></textarea>
                    <small>Character count: <span id="charCount">0</span>/1000</small>
                </div>
                
                <div class="form-group">
                    <label for="language">Language:</label>
                    <select id="language">
                        <option value="en">🇺🇸 English</option>
                        <option value="ar">🇸🇦 Arabic</option>
                        <option value="zh">🇨🇳 Chinese</option>
                        <option value="da">🇩🇰 Danish</option>
                        <option value="nl">🇳🇱 Dutch</option>
                        <option value="fi">🇫🇮 Finnish</option>
                        <option value="fr">🇫🇷 French</option>
                        <option value="de">🇩🇪 German</option>
                        <option value="el">🇬🇷 Greek</option>
                        <option value="he">🇮🇱 Hebrew</option>
                        <option value="hi">🇮🇳 Hindi</option>
                        <option value="it">🇮🇹 Italian</option>
                        <option value="ja">🇯🇵 Japanese</option>
                        <option value="ko">🇰🇷 Korean</option>
                        <option value="ms">🇲🇾 Malay</option>
                        <option value="no">🇳🇴 Norwegian</option>
                        <option value="pl">🇵🇱 Polish</option>
                        <option value="pt">🇵🇹 Portuguese</option>
                        <option value="ru">🇷🇺 Russian</option>
                        <option value="es">🇪🇸 Spanish</option>
                        <option value="sv">🇸🇪 Swedish</option>
                        <option value="sw">🇹🇿 Swahili</option>
                        <option value="tr">🇹🇷 Turkish</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Emotion/Exaggeration:</label>
                    <div class="slider-container">
                        <input type="range" id="exaggeration" class="slider" min="0" max="1" step="0.1" value="0.5">
                        <span id="exaggerationValue" class="slider-value">0.5</span>
                    </div>
                    <small>Higher values = more emotional and expressive</small>
                </div>
                
                <div class="form-group">
                    <label>Speaking Speed Control:</label>
                    <div class="slider-container">
                        <input type="range" id="cfg_weight" class="slider" min="0" max="1" step="0.1" value="0.5">
                        <span id="cfgWeightValue" class="slider-value">0.5</span>
                    </div>
                    <small>Lower values = faster speech, higher values = slower speech</small>
                </div>
                
                <div class="form-group">
                    <label for="reference_audio">Reference Audio (for voice cloning):</label>
                    <input type="file" id="reference_audio" accept="audio/*">
                    <small>Upload 3-30 seconds of clear audio to clone the voice</small>
                </div>
                
                <button type="submit" id="generateBtn">🎙️ Generate Speech</button>
                <button type="button" onclick="clearCache()">🧹 Clear Memory Cache</button>
            </form>
            
            <div id="result"></div>
        </div>
        
        <div class="container">
            <h3>📊 System Status</h3>
            <div id="statusGrid" class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="deviceStatus">-</div>
                    <div class="status-label">Device</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="memoryStatus">-</div>
                    <div class="status-label">Memory Usage</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="cpuStatus">-</div>
                    <div class="status-label">CPU Usage</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="modelsStatus">-</div>
                    <div class="status-label">Models Loaded</div>
                </div>
            </div>
            <button onclick="updateStatus()">🔄 Refresh Status</button>
        </div>
        
        <div class="tip">
            <strong>💡 Tips for best results:</strong><br>
            • Use clear, noise-free reference audio for voice cloning<br>
            • Keep text under 200 characters for fastest generation<br>
            • Plug in your MacBook for sustained performance<br>
            • Close other apps if you experience memory issues
        </div>
        
        <script>
            // Character counter
            document.getElementById('text').addEventListener('input', function() {
                const count = this.value.length;
                document.getElementById('charCount').textContent = count;
                if (count > 1000) {
                    this.style.borderColor = '#ff3b30';
                } else {
                    this.style.borderColor = '#e5e5e7';
                }
            });
            
            // Update slider values
            document.getElementById('exaggeration').oninput = function() {
                document.getElementById('exaggerationValue').textContent = this.value;
            }
            document.getElementById('cfg_weight').oninput = function() {
                document.getElementById('cfgWeightValue').textContent = this.value;
            }
            
            // Handle form submission
            document.getElementById('ttsForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const text = document.getElementById('text').value;
                if (text.length > 1000) {
                    alert('Text is too long! Please keep it under 1000 characters.');
                    return;
                }
                
                const generateBtn = document.getElementById('generateBtn');
                const originalText = generateBtn.innerHTML;
                generateBtn.innerHTML = '<div class="loading"></div> Generating...';
                generateBtn.disabled = true;
                
                const formData = new FormData();
                formData.append('text', text);
                formData.append('language', document.getElementById('language').value);
                formData.append('exaggeration', document.getElementById('exaggeration').value);
                formData.append('cfg_weight', document.getElementById('cfg_weight').value);
                
                const audioFile = document.getElementById('reference_audio').files[0];
                if (audioFile) {
                    formData.append('reference_audio', audioFile);
                }
                
                document.getElementById('result').innerHTML = '<div class="loading"></div> Generating audio...';
                
                try {
                    const response = await fetch('/synthesize', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const audio = document.createElement('audio');
                        audio.controls = true;
                        audio.className = 'audio-player';
                        audio.src = URL.createObjectURL(blob);
                        
                        const download = document.createElement('a');
                        download.href = audio.src;
                        download.download = 'chatterbox_generated.wav';
                        download.className = 'download-link';
                        download.innerHTML = '📥 Download Audio';
                        
                        document.getElementById('result').innerHTML = '<strong>✅ Audio generated successfully!</strong>';
                        document.getElementById('result').appendChild(document.createElement('br'));
                        document.getElementById('result').appendChild(document.createElement('br'));
                        document.getElementById('result').appendChild(audio);
                        document.getElementById('result').appendChild(document.createElement('br'));
                        document.getElementById('result').appendChild(document.createElement('br'));
                        document.getElementById('result').appendChild(download);
                    } else {
                        const error = await response.text();
                        document.getElementById('result').innerHTML = '❌ Error: ' + error;
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = '❌ Network error: ' + error.message;
                } finally {
                    generateBtn.innerHTML = originalText;
                    generateBtn.disabled = false;
                }
            }
            
            // Status updates
            async function updateStatus() {
                try {
                    const response = await fetch('/health');
                    const status = await response.json();
                    
                    document.getElementById('deviceStatus').textContent = status.device.toUpperCase();
                    document.getElementById('memoryStatus').textContent = status.memory_usage_percent + '%';
                    document.getElementById('cpuStatus').textContent = status.cpu_usage_percent + '%';
                    
                    const modelsLoaded = Object.values(status.models_loaded).filter(Boolean).length;
                    document.getElementById('modelsStatus').textContent = modelsLoaded;
                    
                } catch (error) {
                    console.error('Error loading status:', error);
                }
            }
            
            async function clearCache() {
                try {
                    const response = await fetch('/clear_cache', {method: 'POST'});
                    if (response.ok) {
                        alert('✅ Memory cache cleared successfully!');
                        updateStatus();
                    } else {
                        alert('❌ Error clearing cache');
                    }
                } catch (error) {
                    alert('❌ Network error: ' + error.message);
                }
            }
            
            // Initial status load and periodic updates
            updateStatus();
            setInterval(updateStatus, 30000); // Update every 30 seconds
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint with system information"""
    return get_system_info()

@app.post("/synthesize")
async def synthesize_text(
    text: str = Form(...),
    language: str = Form("en"),
    exaggeration: float = Form(0.5),
    cfg_weight: float = Form(0.5),
    temperature: float = Form(0.7),
    speed_factor: float = Form(1.0),
    reference_audio: Optional[UploadFile] = File(None)
):
    """
    Synthesize text to speech
    Optimized for M1 MacBook Air memory constraints
    """
    try:
        # Validate inputs
        if len(text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Determine if multilingual model is needed
        multilingual = language != "en"
        model = await get_model(multilingual=multilingual)
        
        # Handle reference audio for voice cloning
        audio_prompt_path = None
        temp_dir = None
        
        if reference_audio and reference_audio.filename:
            temp_dir = tempfile.mkdtemp()
            audio_prompt_path = os.path.join(temp_dir, reference_audio.filename)
            
            content = await reference_audio.read()
            with open(audio_prompt_path, "wb") as f:
                f.write(content)
            
            logger.info(f"Using reference audio: {reference_audio.filename}")
        
        # Generate audio
        logger.info(f"Generating audio for text: {text[:50]}...")
        
        generation_args = {
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
            "speed_factor": speed_factor
        }
        
        if audio_prompt_path:
            generation_args["audio_prompt_path"] = audio_prompt_path
        
        if multilingual and language != "en":
            wav = model.generate(text, language_id=language, **generation_args)
        else:
            wav = model.generate(text, **generation_args)
        
        # Convert to audio stream
        buffer = io.BytesIO()
        ta.save(buffer, wav, model.sr, format="wav")
        buffer.seek(0)
        
        # Cleanup temporary files
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        
        logger.info("Audio generation completed successfully")
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=chatterbox_generated.wav"}
        )
        
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_cache")
async def clear_model_cache():
    """Clear model cache to free memory"""
    global _model_cache, _multilingual_model_cache
    
    models_cleared = len(_model_cache) + len(_multilingual_model_cache)
    
    _model_cache.clear()
    _multilingual_model_cache.clear()
    
    # Force garbage collection
    import gc
    gc.collect()
    
    # Clear MPS cache if available
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    
    logger.info(f"Cleared {models_cleared} models from cache")
    
    return {
        "message": "Model cache cleared successfully",
        "models_cleared": models_cleared,
        "memory_freed": True
    }

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Chatterbox TTS Server",
        "version": "1.0.0",
        "platform": "M1 MacBook Air Optimized",
        "features": [
            "Text-to-Speech",
            "Voice Cloning",
            "Multilingual Support",
            "MPS Acceleration",
            "Memory Optimization"
        ],
        "supported_languages": [
            "ar", "da", "de", "el", "en", "es", "fi", "fr", "he", "hi",
            "it", "ja", "ko", "ms", "nl", "no", "pl", "pt", "ru", "sv", "sw", "tr", "zh"
        ]
    }

if __name__ == "__main__":
    print("🍎 Starting Chatterbox TTS Server for M1 MacBook Air")
    print(f"🔧 Device: {get_device()}")
    print("🌐 Server will be available at: http://localhost:8000")
    
    # Optimize for MacBook Air
    os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")
    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=1,  # Single worker for memory efficiency
        reload=False,
        log_level="info"
    )
