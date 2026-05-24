import io
import wave
import logging
from typing import Optional
import numpy as np
from piper import PiperVoice

logger = logging.getLogger(__name__)

class TTSEngine:
    """
    Wrapper class around Piper TTS engine.
    Handles loading the ONNX voice model and synthesizing text
    to PCM 16-bit mono 16000 Hz WAV format with dynamic resampling.
    """
    def __init__(self):
        self.voice: Optional[PiperVoice] = None

    def load_model(self, model_path: str) -> None:
        """
        Load the Piper voice model from the specified ONNX file path.
        """
        logger.info(f"Loading Piper voice model from: {model_path}")
        try:
            # PiperVoice.load automatically locates the corresponding .json config file
            # in the same directory as the .onnx file.
            self.voice = PiperVoice.load(model_path)
            logger.info("Piper voice model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Piper voice model from {model_path}: {e}", exc_info=True)
            raise RuntimeError(f"Error loading voice model: {e}")

    def synthesize(self, text: str) -> bytes:
        """
        Synthesize the input text into a 16-bit PCM mono 16000 Hz WAV file.
        Automatically resamples the output if the model's native rate is different.
        """
        if not self.voice:
            raise RuntimeError("TTS Engine voice model is not loaded. Call load_model() first.")

        # 1. Synthesize text to an in-memory WAV buffer at the model's native sample rate
        native_wav_io = io.BytesIO()
        with wave.open(native_wav_io, "wb") as wav_file:
            self.voice.synthesize(text, wav_file)
        
        native_wav_io.seek(0)

        # 2. Extract raw audio frames and native format parameters
        with wave.open(native_wav_io, "rb") as wav_file:
            params = wav_file.getparams()
            n_channels = params.nchannels
            samp_width = params.sampwidth
            frame_rate = params.framerate
            n_frames = params.nframes
            raw_frames = wav_file.readframes(n_frames)

        # 3. Resample the audio data to 16000 Hz if the native rate is different
        target_sample_rate = 16000
        if frame_rate != target_sample_rate:
            logger.info(f"Resampling synthesized audio dynamically from {frame_rate}Hz to {target_sample_rate}Hz")
            resampled_frames = self._resample_pcm(raw_frames, frame_rate, target_sample_rate)
        else:
            resampled_frames = raw_frames

        # 4. Pack the resampled PCM frames into a standard WAV container
        output_wav_io = io.BytesIO()
        with wave.open(output_wav_io, "wb") as wav_file:
            # Enforce 1 channel (mono), 2 bytes per sample (16-bit), and 16000 Hz sample rate
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(target_sample_rate)
            wav_file.writeframes(resampled_frames)

        return output_wav_io.getvalue()

    def _resample_pcm(self, audio_bytes: bytes, orig_sr: int, target_sr: int) -> bytes:
        """
        Resample 16-bit signed PCM audio bytes from orig_sr to target_sr
        using linear interpolation via NumPy.
        """
        # Convert raw bytes to numpy array of 16-bit signed integers
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        
        # Calculate original duration and total target samples
        duration = len(audio_data) / orig_sr
        num_target_samples = int(duration * target_sr)
        
        # Use dynamic linear interpolation for fast and robust resampling
        resampled_data = np.interp(
            np.linspace(0, duration, num_target_samples, endpoint=False),
            np.linspace(0, duration, len(audio_data), endpoint=False),
            audio_data
        )
        
        # Cast back to int16 and return raw bytes
        return resampled_data.astype(np.int16).tobytes()

# Global singleton instance
tts_engine = TTSEngine()
