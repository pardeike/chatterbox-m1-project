#!/usr/bin/env python3
"""
Voice Cloning Example for M1 MacBook Air
Shows how to clone voices using reference audio
Created by Claude for Michael Koker
"""

import torchaudio as ta
import torch
from pathlib import Path
import time
import os

def main():
    print("🎭 Chatterbox Voice Cloning Example")
    print("=" * 40)
    
    # Check for reference audio files
    reference_dir = Path("reference_audio")
    audio_files = list(reference_dir.glob("*.wav")) + list(reference_dir.glob("*.mp3"))
    
    if not audio_files:
        print("❌ No reference audio found!")
        print("💡 To use voice cloning:")
        print("   1. Record a 10-30 second audio sample")
        print("   2. Save as .wav or .mp3 in the 'reference_audio' folder")
        print("   3. Run this script again")
        print("")
        print("📝 Tips for good reference audio:")
        print("   • Clear, noise-free recording")
        print("   • Single speaker only")
        print("   • Natural speaking pace")
        print("   • Good microphone quality")
        return
    
    # Setup device
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"🔧 Using device: {device}")
    
    try:
        # Load model
        print("🤖 Loading Chatterbox model...")
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device=device)
        print("✅ Model loaded!")
        
        # Create outputs directory
        os.makedirs("outputs", exist_ok=True)
        
        # Process each reference audio file
        for i, reference_file in enumerate(audio_files, 1):
            print(f"\n🎭 Voice Clone {i}: {reference_file.name}")
            print("-" * 30)
            
            # Different test texts to show voice consistency
            test_texts = [
                "Hello! This is a test of voice cloning using your reference audio.",
                "The weather today is absolutely beautiful, don't you think?",
                "I'm excited to demonstrate the power of AI voice synthesis!",
                "Thank you for trying out Chatterbox on your M1 MacBook Air."
            ]
            
            for j, text in enumerate(test_texts, 1):
                print(f"   Generating sample {j}: {text[:30]}...")
                
                start_time = time.time()
                
                # Generate with different settings to show versatility
                if j == 1:
                    # Natural speech
                    wav = model.generate(
                        text,
                        audio_prompt_path=str(reference_file),
                        exaggeration=0.5,
                        cfg_weight=0.5,
                        temperature=0.7
                    )
                    style = "natural"
                elif j == 2:
                    # Emotional speech
                    wav = model.generate(
                        text,
                        audio_prompt_path=str(reference_file),
                        exaggeration=0.8,
                        cfg_weight=0.3,
                        temperature=0.8
                    )
                    style = "emotional"
                elif j == 3:
                    # Fast speech
                    wav = model.generate(
                        text,
                        audio_prompt_path=str(reference_file),
                        exaggeration=0.4,
                        cfg_weight=0.3,
                        speed_factor=1.3
                    )
                    style = "fast"
                else:
                    # Slow, deliberate speech
                    wav = model.generate(
                        text,
                        audio_prompt_path=str(reference_file),
                        exaggeration=0.6,
                        cfg_weight=0.7,
                        speed_factor=0.8
                    )
                    style = "deliberate"
                
                gen_time = time.time() - start_time
                
                # Save with descriptive filename
                output_name = f"clone_{i}_{style}_sample_{j}.wav"
                output_path = f"outputs/{output_name}"
                ta.save(output_path, wav, model.sr)
                
                print(f"   ✅ Saved as {output_name} ({gen_time:.2f}s)")
        
        print(f"\n🎉 Voice cloning complete!")
        print(f"📁 Generated {len(audio_files) * len(test_texts)} audio samples")
        print("🎧 Check the 'outputs' folder to hear the results")
        
        # Performance summary
        print(f"\n📊 Summary:")
        print(f"   Reference files processed: {len(audio_files)}")
        print(f"   Device used: {device}")
        print(f"   Model sample rate: {model.sr} Hz")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you've run ./setup_m1.sh first!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try running with CPU device if MPS has issues")

if __name__ == "__main__":
    main()