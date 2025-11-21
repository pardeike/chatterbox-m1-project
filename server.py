#!/usr/bin/env python3
"""
Lightweight Chatterbox TTS Server optimized for M1 MacBook Air
Memory-efficient with lazy loading and model caching
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import torchaudio as ta
import torch
import uvicorn
import io
import os
import sys
import tempfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_environment():
    """
    Validate PyTorch/TorchVision compatibility before starting server.
    
    Note: torchvision is imported inside this function (not at module level) intentionally.
    This allows us to catch and report import errors gracefully with helpful messages,
    rather than having the server fail to start with no explanation.
    """
    try:
        import torchvision
        import torchvision.ops
        
        # Test the problematic NMS operation with sample data
        # These values are minimal test cases: two bounding boxes with scores
        boxes = torch.tensor([[0, 0, 1, 1], [0.5, 0.5, 1.5, 1.5]], dtype=torch.float32)
        scores = torch.tensor([0.9, 0.8], dtype=torch.float32)
        torchvision.ops.nms(boxes, scores, 0.5)
        
        logger.info(f"✅ Environment validation passed - PyTorch {torch.__version__}, TorchVision {torchvision.__version__}")
        return True
    except Exception as e:
        logger.error("❌ Environment validation failed!")
        logger.error(f"Error: {str(e)}")
        logger.error("")
        logger.error("This is a PyTorch/TorchVision compatibility issue on M1 MacBook Air.")
        logger.error("")
        logger.error("🔧 TO FIX THIS ISSUE, run one of these commands:")
        logger.error("")
        logger.error("   Option 1 (Recommended):")
        logger.error("   ./definitive_fix.sh")
        logger.error("")
        logger.error("   Option 2 (Alternative):")
        logger.error("   ./fix_pytorch.sh")
        logger.error("")
        logger.error("   Option 3 (Manual):")
        logger.error("   conda activate chatterbox")
        logger.error("   pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu")
        logger.error("   pip install transformers==4.35.0 --force-reinstall")
        logger.error("")
        logger.error("After running the fix, restart the server.")
        logger.error("")
        return False

app = FastAPI(title="Chatterbox TTS Server (M1 Optimized)", version="1.0.0")

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
        return "mps"
    else:
        logger.warning("MPS not available, falling back to CPU")
        return "cpu"

async def get_model(multilingual=False):
    """Lazy load model with caching"""
    cache_key = "multilingual" if multilingual else "english"
    cache = _multilingual_model_cache if multilingual else _model_cache
    
    if cache_key not in cache:
        logger.info(f"Loading {cache_key} model...")
        
        try:
            if multilingual:
                from chatterbox.mtl_tts import ChatterboxMultilingualTTS
                model = ChatterboxMultilingualTTS.from_pretrained(device=get_device())
            else:
                from chatterbox.tts import ChatterboxTTS
                model = ChatterboxTTS.from_pretrained(device=get_device())
            
            cache[cache_key] = model
            logger.info(f"{cache_key.title()} model loaded")
        except Exception as e:
            error_msg = str(e)
            # String matching is appropriate here - we're looking for the specific
            # "operator torchvision::nms does not exist" error from transformers/torch
            if "torchvision::nms" in error_msg or "does not exist" in error_msg:
                logger.error("❌ Model loading failed due to PyTorch/TorchVision compatibility issue")
                logger.error("🔧 Run './definitive_fix.sh' to fix this issue")
                raise RuntimeError(
                    "PyTorch/TorchVision compatibility error. "
                    "Please run './definitive_fix.sh' to fix the environment. "
                    "See PYTORCH_FIX.md for more details."
                ) from e
            else:
                raise
    
    return cache[cache_key]

@app.get("/")
async def root():
    """Simple web interface"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {
            "message": "Chatterbox TTS Server (M1 Optimized)",
            "endpoints": {
                "synthesize": "/synthesize",
                "health": "/health",
                "docs": "/docs"
            }
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    import psutil
    
    memory_info = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        "status": "healthy",
        "device": get_device(),
        "mps_available": torch.backends.mps.is_available(),
        "memory_usage": f"{memory_info.percent}%",
        "cpu_usage": f"{cpu_percent}%",
        "models_loaded": {
            "english": "english" in _model_cache,
            "multilingual": "multilingual" in _multilingual_model_cache
        }
    }

@app.post("/synthesize")
async def synthesize_text(
    text: str = Form(...),
    language: str = Form("en"),
    exaggeration: float = Form(0.5),
    cfg_weight: float = Form(0.5),
    temperature: float = Form(0.7),
    reference_audio: UploadFile = File(None)
):
    """
    Synthesize text to speech
    Optimized for M1 MacBook Air memory constraints
    """
    try:
        # Validate inputs
        if len(text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
        
        # Determine if multilingual model is needed
        multilingual = language != "en"
        model = await get_model(multilingual=multilingual)
        
        # Handle reference audio for voice cloning
        audio_prompt_path = None
        if reference_audio:
            # Save uploaded file temporarily
            temp_dir = tempfile.mkdtemp()
            audio_prompt_path = os.path.join(temp_dir, reference_audio.filename)
            
            with open(audio_prompt_path, "wb") as f:
                content = await reference_audio.read()
                f.write(content)
        
        # Generate audio
        logger.info(f"Generating audio for: {text[:50]}...")
        
        if multilingual and language != "en":
            wav = model.generate(
                text,
                language_id=language,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                temperature=temperature
            )
        else:
            wav = model.generate(
                text,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                temperature=temperature
            )
        
        # Convert to audio stream
        buffer = io.BytesIO()
        ta.save(buffer, wav, model.sr, format="wav")
        buffer.seek(0)
        
        # Cleanup temporary files
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            os.remove(audio_prompt_path)
            os.rmdir(temp_dir)
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=generated.wav"}
        )
        
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_cache")
async def clear_model_cache():
    """Clear model cache to free memory"""
    global _model_cache, _multilingual_model_cache
    
    _model_cache.clear()
    _multilingual_model_cache.clear()
    
    # Force garbage collection
    import gc
    gc.collect()
    
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    
    return {"message": "Model cache cleared", "memory_freed": True}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    # Validate environment before starting
    if not validate_environment():
        logger.error("Server startup aborted due to environment validation failure")
        sys.exit(1)
    
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    print("Starting Chatterbox TTS Server for M1 MacBook Air")
    print(f"Device: {get_device()}")
    print("Server will be available at: http://localhost:8000")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=1,  # Single worker for memory efficiency on MacBook Air
        reload=False
    )