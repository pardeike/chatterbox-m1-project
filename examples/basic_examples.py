#!/usr/bin/env python3
"""
Basic Chatterbox TTS Examples for M1 MacBook Air
Demonstrates different features and use cases
"""

import torchaudio as ta
import torch
import time
import os
from pathlib import Path

def check_setup():
    """Check if everything is set up correctly"""
    print("🍎 Chatterbox TTS Examples - M1 MacBook Air")
    print("=" * 50)
    
    # Check PyTorch and MPS
    print(f"PyTorch version: {torch.__version__}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"MPS built: {torch.backends.mps.is_built()}")
    
    # Check Chatterbox import
    try:
        from chatterbox.tts import ChatterboxTTS
        print("✅ Chatterbox TTS imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Chatterbox import failed: {e}")
        print("Please run setup.sh first!")
        return False

def example_1_basic_tts():
    """Example 1: Basic text-to-speech"""
    print("\n📖 Example 1: Basic Text-to-Speech")
    print("-" * 40)
    
    from chatterbox.tts import ChatterboxTTS
    
    # Use MPS if available, otherwise CPU
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model (this will download ~2.5GB on first run)
    print("🤖 Loading Chatterbox model...")
    start_time = time.time()
    model = ChatterboxTTS.from_pretrained(device=device)
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.1f} seconds")
    
    # Generate speech
    text = "Hello! This is Chatterbox running on your M1 MacBook Air with Apple Silicon acceleration."
    print(f"🎙️ Generating: {text}")
    
    start_time = time.time()
    wav = model.generate(text)
    generation_time = time.time() - start_time
    
    # Save audio
    output_file = "example_1_basic.wav"
    ta.save(output_file, wav, model.sr)
    
    print(f"✅ Audio saved as: {output_file}")
    print(f"⚡ Generation time: {generation_time:.2f} seconds")
    print(f"📊 Sample rate: {model.sr} Hz")
    print(f"🔊 Audio duration: {wav.shape[-1] / model.sr:.1f} seconds")

def example_2_voice_cloning():
    """Example 2: Voice cloning with reference audio"""
    print("\n🎭 Example 2: Voice Cloning")
    print("-" * 40)
    
    # Check if reference audio exists
    reference_files = [
        "reference_voice.wav",
        "../audio_samples/reference_voice.wav",
        "audio_samples/reference_voice.wav"
    ]
    
    reference_audio = None
    for ref_file in reference_files:
        if os.path.exists(ref_file):
            reference_audio = ref_file
            break
    
    if not reference_audio:
        print("⚠️ No reference audio found. Skipping voice cloning example.")
        print("To try voice cloning:")
        print("1. Record 10-30 seconds of clear speech")
        print("2. Save as 'reference_voice.wav' in this directory")
        print("3. Run this example again")
        return
    
    from chatterbox.tts import ChatterboxTTS
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = ChatterboxTTS.from_pretrained(device=device)
    
    # Generate with cloned voice
    text = "Now I'm speaking with a cloned voice! This is amazing technology running on Apple Silicon."
    print(f"🎙️ Generating with cloned voice: {text}")
    print(f"🎧 Using reference: {reference_audio}")
    
    start_time = time.time()
    wav_cloned = model.generate(
        text, 
        audio_prompt_path=reference_audio,
        exaggeration=0.6,  # Slight emotion boost
        cfg_weight=0.4,    # Good balance for M1
        temperature=0.7
    )
    generation_time = time.time() - start_time
    
    output_file = "example_2_cloned.wav"
    ta.save(output_file, wav_cloned, model.sr)
    
    print(f"✅ Cloned voice audio saved as: {output_file}")
    print(f"⚡ Generation time: {generation_time:.2f} seconds")

def example_3_multilingual():
    """Example 3: Multilingual text-to-speech"""
    print("\n🌍 Example 3: Multilingual TTS")
    print("-" * 40)
    
    try:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    except ImportError:
        print("⚠️ Multilingual model not available. Install with:")
        print("pip install chatterbox-tts[multilingual]")
        return
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print("🤖 Loading multilingual model...")
    
    start_time = time.time()
    multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    load_time = time.time() - start_time
    print(f"✅ Multilingual model loaded in {load_time:.1f} seconds")
    
    # Test different languages
    languages = [
        ("fr", "Bonjour! Ceci est un exemple en français avec Chatterbox."),
        ("es", "¡Hola! Este es un ejemplo en español con Chatterbox."),
        ("de", "Hallo! Das ist ein Beispiel auf Deutsch mit Chatterbox."),
        ("zh", "你好！这是使用Chatterbox的中文示例。")
    ]
    
    for lang_code, text in languages:
        print(f"🎙️ Generating {lang_code.upper()}: {text}")
        
        start_time = time.time()
        wav = multilingual_model.generate(text, language_id=lang_code)
        generation_time = time.time() - start_time
        
        output_file = f"example_3_{lang_code}.wav"
        ta.save(output_file, wav, multilingual_model.sr)
        
        print(f"✅ {lang_code.upper()} audio saved as: {output_file} ({generation_time:.2f}s)")

def example_4_performance_test():
    """Example 4: Performance benchmarking"""
    print("\n⚡ Example 4: Performance Benchmarking")
    print("-" * 40)
    
    import psutil
    from chatterbox.tts import ChatterboxTTS
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = ChatterboxTTS.from_pretrained(device=device)
    
    # Test texts of different lengths
    test_cases = [
        ("Short", "Hello world!"),
        ("Medium", "This is a medium length sentence to test generation speed."),
        ("Long", "This is a much longer sentence that will test how well Chatterbox performs on your M1 MacBook Air when generating longer pieces of text with more complex content.")
    ]
    
    print(f"🔧 Testing on device: {device}")
    print(f"💾 Available memory: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    
    for test_name, text in test_cases:
        print(f"\n📝 Testing {test_name} text ({len(text)} characters)")
        
        # Measure memory before
        memory_before = psutil.Process().memory_info().rss / (1024**2)  # MB
        
        # Warm up (exclude from timing)
        if test_name == "Short":
            model.generate("Warm up.")
        
        # Benchmark generation
        start_time = time.time()
        wav = model.generate(text)
        generation_time = time.time() - start_time
        
        # Measure memory after
        memory_after = psutil.Process().memory_info().rss / (1024**2)  # MB
        memory_used = memory_after - memory_before
        
        # Calculate metrics
        chars_per_second = len(text) / generation_time
        audio_duration = wav.shape[-1] / model.sr
        realtime_factor = audio_duration / generation_time
        
        print(f"   ⏱️  Generation time: {generation_time:.2f}s")
        print(f"   🎵 Audio duration: {audio_duration:.2f}s")
        print(f"   📈 Realtime factor: {realtime_factor:.1f}x")
        print(f"   🚀 Speed: {chars_per_second:.1f} chars/second")
        print(f"   💾 Memory used: {memory_used:+.1f} MB")
        
        # Save sample
        output_file = f"example_4_performance_{test_name.lower()}.wav"
        ta.save(output_file, wav, model.sr)

def example_5_batch_generation():
    """Example 5: Efficient batch processing"""
    print("\n📚 Example 5: Batch Text Processing")
    print("-" * 40)
    
    from chatterbox.tts import ChatterboxTTS
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = ChatterboxTTS.from_pretrained(device=device)
    
    # Sample texts for batch processing
    texts = [
        "Welcome to the first chapter of our audio book.",
        "This is the second paragraph with different content.",
        "Here we continue with the third section of text.",
        "And finally, this is the conclusion of our demo."
    ]
    
    print(f"🔄 Processing {len(texts)} text segments...")
    
    audio_chunks = []
    total_start_time = time.time()
    
    for i, text in enumerate(texts, 1):
        print(f"   Processing {i}/{len(texts)}: {text[:40]}...")
        
        wav = model.generate(text)
        audio_chunks.append(wav)
        
        # Add small silence between chunks (0.5 seconds)
        silence_samples = int(0.5 * model.sr)
        silence = torch.zeros(wav.shape[0], silence_samples)
        audio_chunks.append(silence)
    
    total_time = time.time() - total_start_time
    
    # Concatenate all audio
    final_audio = torch.cat(audio_chunks, dim=-1)
    
    # Save combined audio
    output_file = "example_5_batch_combined.wav"
    ta.save(output_file, final_audio, model.sr)
    
    total_duration = final_audio.shape[-1] / model.sr
    total_chars = sum(len(text) for text in texts)
    
    print(f"✅ Batch processing complete!")
    print(f"   📁 Combined audio saved as: {output_file}")
    print(f"   ⏱️  Total processing time: {total_time:.2f}s")
    print(f"   🎵 Total audio duration: {total_duration:.2f}s")
    print(f"   📝 Total characters: {total_chars}")
    print(f"   🚀 Average speed: {total_chars/total_time:.1f} chars/second")

def main():
    """Run all examples"""
    if not check_setup():
        return
    
    print("\n🚀 Starting Chatterbox Examples...")
    print("Note: First run will download models (~2.5GB)")
    print("This may take a few minutes on first execution.\n")
    
    try:
        # Run examples
        example_1_basic_tts()
        example_2_voice_cloning()
        example_3_multilingual()
        example_4_performance_test()
        example_5_batch_generation()
        
        print("\n🎉 All examples completed successfully!")
        print("\n📁 Generated audio files:")
        
        # List generated files
        wav_files = [f for f in os.listdir('.') if f.endswith('.wav') and f.startswith('example_')]
        for wav_file in sorted(wav_files):
            file_size = os.path.getsize(wav_file) / (1024**2)  # MB
            print(f"   🎵 {wav_file} ({file_size:.1f} MB)")
        
        print("\n💡 Tips:")
        print("   • Listen to the generated audio files")
        print("   • Try different settings in the examples")
        print("   • Use ./start_server.sh for the web interface")
        
    except KeyboardInterrupt:
        print("\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check that conda environment is activated and dependencies are installed")

if __name__ == "__main__":
    main()
