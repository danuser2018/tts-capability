import wave
from app.services.tts_engine import tts_engine
from app.core.config import settings

def main():
    print("--- STARTING LOCAL SYNTHESIS TEST ---")
    
    # 1. Load the real model
    print(f"Loading model from: {settings.MODEL_PATH} ...")
    tts_engine.load_model(settings.MODEL_PATH)
    print("Model loaded successfully.")
    
    # 2. Synthesize test sentence
    text = "Hola, esta es una prueba exitosa del servicio de síntesis de voz en local."
    print(f"Synthesizing text: '{text}' ...")
    audio_bytes = tts_engine.synthesize(text)
    print(f"Synthesis completed. Generated audio size: {len(audio_bytes)} bytes.")
    
    # 3. Save to WAV file
    output_filename = "prueba.wav"
    with open(output_filename, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio file saved to: '{output_filename}'.")
    
    # 4. Read back and verify WAV headers
    print("\nVerifying properties of the generated WAV file...")
    with wave.open(output_filename, "rb") as wav_file:
        params = wav_file.getparams()
        channels = params.nchannels
        sample_width = params.sampwidth
        sample_rate = params.framerate
        num_frames = params.nframes
        duration = num_frames / sample_rate
        
        print(f" - Channels: {channels} (expected: 1 [mono])")
        print(f" - Sample width: {sample_width} bytes (expected: 2 [16-bit])")
        print(f" - Sample rate: {sample_rate} Hz (expected: 16000 Hz)")
        print(f" - Duration: {duration:.2f} seconds")
        
        # Assert properties to guarantee correctness
        assert channels == 1, f"Error: Channels = {channels}, expected 1"
        assert sample_width == 2, f"Error: Sample width = {sample_width}, expected 2"
        assert sample_rate == 16000, f"Error: Sample rate = {sample_rate}, expected 16000"
        
    print("\n--- TEST COMPLETED SUCCESSFULLY AND FORMAT 100% VERIFIED ---")

if __name__ == "__main__":
    main()
