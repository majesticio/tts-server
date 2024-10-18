# tts_handler.py

import os
from TTS.api import TTS
from io import BytesIO
import soundfile as sf
import torch

class TTSHandler:
    def __init__(self, model_name='tts_models/en/jenny/jenny'):
        # Check if CUDA is available and set the device accordingly
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_engine = TTS(model_name=model_name, progress_bar=False).to(self.device)

    def text_to_speech(self, text):
        try:
            # Generate speech and get the correct sample rate from the model
            wav = self.tts_engine.tts(text)
            sample_rate = self.tts_engine.synthesizer.output_sample_rate  # Fetch correct sample rate

            # Save audio to in-memory bytes
            with BytesIO() as output_bytes:
                sf.write(output_bytes, wav, sample_rate, format='WAV')
                output_bytes.seek(0)
                return output_bytes.getvalue()
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            return None
