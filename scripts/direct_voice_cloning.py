#!/usr/bin/env python3
"""
Direct Python library integration (without API)
Use Chatterbox directly in your Python application
"""

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import os

class VoiceCloner:
    def __init__(self, device="mps"):
        """Initialize the voice cloner"""
        self.device = device
        self.model = None
        
    def load_model(self):
        """Load the Chatterbox model (do this once)"""
        if self.model is None:
            print("Loading Chatterbox model...")
            self.model = ChatterboxTTS.from_pretrained(device=self.device)
            print("Model loaded successfully")
    
    def clone_voice(self, text, reference_audio_path, output_path="output.wav", 
                   exaggeration=0.6, cfg_weight=0.4, temperature=0.7):
        """
        Clone a voice and generate speech
        
        Args:
            text: Text to synthesize
            reference_audio_path: Path to reference audio (10-30 seconds recommended)
            output_path: Where to save the generated audio
            exaggeration: Emotion level (0.0-1.0)
            cfg_weight: Speech control (0.0-1.0)
            temperature: Creativity (0.1-1.0)
        """
        # Ensure model is loaded
        self.load_model()
        
        # Validate reference audio exists
        if not os.path.exists(reference_audio_path):
            raise FileNotFoundError(f"Reference audio not found: {reference_audio_path}")
        
        # Generate with cloned voice
        print(f"Generating speech with cloned voice...")
        wav = self.model.generate(
            text,
            audio_prompt_path=reference_audio_path,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature
        )
        
        # Save the audio
        ta.save(output_path, wav, self.model.sr)
        print(f"Audio saved to: {output_path}")
        
        return output_path

# Example usage in your application
if __name__ == "__main__":
    # Create a voice cloner instance
    cloner = VoiceCloner(device="mps")  # Use "cpu" if MPS has issues
    
    # Clone a voice and generate speech
    cloner.clone_voice(
        text="This is generated speech using a cloned voice directly from Python.",
        reference_audio_path="reference_audio/my_voice.wav",
        output_path="direct_cloned_output.wav",
        exaggeration=0.6,
        cfg_weight=0.4
    )
    
    # You can use the same cloner for multiple generations
    # The model stays loaded in memory for faster subsequent calls
    cloner.clone_voice(
        text="This is a second generation with the same cloned voice.",
        reference_audio_path="reference_audio/my_voice.wav",
        output_path="direct_cloned_output2.wav"
    )