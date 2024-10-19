import os
from TTS.api import TTS
from io import BytesIO
import torch
from pydub import AudioSegment
import soundfile as sf  # Ensure this is imported

class TTSHandler:
    def __init__(self, model_name='tts_models/en/jenny/jenny'):
        # Determine if CUDA is available and set the gpu flag
        self.use_cuda = torch.cuda.is_available()
        # Initialize TTS model for /synthesize endpoint
        self.tts_engine = TTS(model_name=model_name, progress_bar=False, gpu=self.use_cuda)
        self.clone_engine = None  # Will be initialized when needed
        self.max_chunk_length = 500  # Adjust as needed

    def split_text_into_chunks(self, text, max_chunk_length):
        words = text.split()
        chunks = []
        current_chunk = ''

        for word in words:
            if len(word) > max_chunk_length:
                # Split long words (rare, but to handle edge cases)
                for i in range(0, len(word), max_chunk_length):
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = ''
                    chunks.append(word[i:i+max_chunk_length])
            else:
                # If adding the next word exceeds the max chunk length
                if len(current_chunk) + len(word) + 1 > max_chunk_length:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = ''
                current_chunk += word + ' '
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def text_to_speech(self, text):
        try:
            # Split text into acceptable chunks
            chunks = self.split_text_into_chunks(text, self.max_chunk_length)
            # Initialize an empty AudioSegment
            combined_audio = AudioSegment.empty()

            for chunk in chunks:
                # Generate speech with the Jenny model
                wav_chunk = self.tts_engine.tts(chunk)
                sample_rate = self.tts_engine.synthesizer.output_sample_rate

                # Save chunk to BytesIO object
                with BytesIO() as chunk_bytes:
                    sf.write(chunk_bytes, wav_chunk, sample_rate, format='WAV')
                    chunk_bytes.seek(0)
                    # Load chunk into AudioSegment
                    audio_segment = AudioSegment.from_file(chunk_bytes, format='wav')
                    # Append to combined_audio
                    combined_audio += audio_segment

            # Export combined_audio to BytesIO
            with BytesIO() as output_bytes:
                combined_audio.export(output_bytes, format='wav')
                output_bytes.seek(0)
                return output_bytes.read()

        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            return None

    def clone_speech(
        self,
        text,
        speaker_wav,
        language='en',
        clone_model_name='tts_models/multilingual/multi-dataset/xtts_v2'
    ):
        try:
            # Initialize clone engine if not already done
            if self.clone_engine is None:
                self.clone_engine = TTS(
                    model_name=clone_model_name,
                    progress_bar=False,
                    gpu=self.use_cuda
                )
            # Split text into acceptable chunks
            chunks = self.split_text_into_chunks(text, self.max_chunk_length)
            # Initialize an empty AudioSegment
            combined_audio = AudioSegment.empty()

            for chunk in chunks:
                # Generate cloned speech for each chunk
                wav_chunk = self.clone_engine.tts(
                    chunk,
                    speaker_wav=speaker_wav,
                    language=language
                )
                sample_rate = self.clone_engine.synthesizer.output_sample_rate

                # Save chunk to BytesIO object
                with BytesIO() as chunk_bytes:
                    sf.write(chunk_bytes, wav_chunk, sample_rate, format='WAV')
                    chunk_bytes.seek(0)
                    # Load chunk into AudioSegment
                    audio_segment = AudioSegment.from_file(chunk_bytes, format='wav')
                    # Append to combined_audio
                    combined_audio += audio_segment

            # Export combined_audio to BytesIO
            with BytesIO() as output_bytes:
                combined_audio.export(output_bytes, format='wav')
                output_bytes.seek(0)
                return output_bytes.read()

        except Exception as e:
            print(f"Error during voice cloning: {e}")
            return None
