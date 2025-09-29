#!/usr/bin/env python3
"""
Basic Chatterbox TTS Example for M1 MacBook Air
"""
import torchaudio as ta
import torch
from pathlib import Path
import time
import psutil
import os

def main():
    print("Chatterbox TTS Example for M1 MacBook Air")
    print("=" * 50)
    
    # Check system info
    print(f"Python version: {torch.__version__}")
    print(f"PyTorch version: {torch.__version__}")
    
    # Check MPS availability
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"MPS built: {torch.backends.mps.is_built()}")
    
    # Memory check
    memory_info = psutil.virtual_memory()
    print(f"Available memory: {memory_info.available / 1024**3:.1f} GB")
    
    try:
        # Load model
        print("\nLoading Chatterbox model...")
        start_time = time.time()
        
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device=device)
        
        load_time = time.time() - start_time
        print(f"Model loaded in {load_time:.1f} seconds")
        
        # Example 1: Basic text-to-speech
        print("\nExample 1: Basic TTS")
        text1 = "Hello! This is Chatterbox running on your M1 MacBook Air with Apple Silicon acceleration."
        print(f"Text: {text1}")
        
        start_time = time.time()
        wav1 = model.generate(text1)
        gen_time = time.time() - start_time
        
        output_file1 = "outputs/basic_example.wav"
        ta.save(output_file1, wav1, model.sr)
        print(f"Generated in {gen_time:.2f} seconds")
        print(f"Saved as: {output_file1}")
        
        # Example 2: Emotional speech
        print("\nExample 2: Emotional TTS")
        text2 = "This is an exciting and dramatic example of emotional speech synthesis!"
        print(f"Text: {text2}")
        
        start_time = time.time()
        wav2 = model.generate(
            text2,
            exaggeration=0.8,  # High emotion
            cfg_weight=0.3,    # Faster speech
            temperature=0.8
        )
        gen_time = time.time() - start_time
        
        output_file2 = "outputs/emotional_example.wav"
        ta.save(output_file2, wav2, model.sr)
        print(f"Generated in {gen_time:.2f} seconds")
        print(f"Saved as: {output_file2}")
        
        # Example 3: Voice cloning (if reference audio exists)
        reference_files = list(Path("reference_audio").glob("*.wav"))
        if reference_files:
            print("\nExample 3: Voice Cloning")
            reference_file = reference_files[0]
            text3 = "Now I'm speaking with a cloned voice based on the reference audio!"
            print(f"Text: {text3}")
            print(f"Reference: {reference_file}")
            
            start_time = time.time()
            wav3 = model.generate(
                text3,
                audio_prompt_path=str(reference_file),
                exaggeration=0.6,
                cfg_weight=0.4
            )
            gen_time = time.time() - start_time
            
            output_file3 = "outputs/cloned_example.wav"
            ta.save(output_file3, wav3, model.sr)
            print(f"Generated in {gen_time:.2f} seconds")
            print(f"Saved as: {output_file3}")
        else:
            print("\nNo reference audio found in 'reference_audio' folder")
            print("Add a .wav file to try voice cloning!")
        
        # Performance summary
        print("\nPerformance Summary:")
        print(f"   Device: {device}")
        print(f"   Model size: ~2.5GB")
        print(f"   Sample rate: {model.sr} Hz")
        
        memory_info = psutil.virtual_memory()
        print(f"   Memory usage: {memory_info.percent}%")
        
        print("\nExample complete!")
        print("Check the 'outputs' folder for generated audio files")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you've run the setup script first!")
        print("Run: ./setup_m1.sh")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Try running with CPU device if MPS has issues")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    main()