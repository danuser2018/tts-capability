import wave
from app.services.tts_engine import tts_engine
from app.core.config import settings

def main():
    print("--- INICIANDO PRUEBA DE SÍNTESIS LOCAL ---")
    
    # 1. Load the real model
    print(f"Cargando el modelo desde: {settings.MODEL_PATH} ...")
    tts_engine.load_model(settings.MODEL_PATH)
    print("Modelo cargado correctamente.")
    
    # 2. Synthesize test sentence
    text = "Hola, esta es una prueba exitosa del servicio de síntesis de voz en local."
    print(f"Sintetizando el texto: '{text}' ...")
    audio_bytes = tts_engine.synthesize(text)
    print(f"Síntesis completada. Tamaño del audio generado: {len(audio_bytes)} bytes.")
    
    # 3. Save to WAV file
    output_filename = "prueba.wav"
    with open(output_filename, "wb") as f:
        f.write(audio_bytes)
    print(f"Archivo de audio guardado en: '{output_filename}'.")
    
    # 4. Read back and verify WAV headers
    print("\nVerificando propiedades del archivo WAV generado...")
    with wave.open(output_filename, "rb") as wav_file:
        params = wav_file.getparams()
        channels = params.nchannels
        sample_width = params.sampwidth
        sample_rate = params.framerate
        num_frames = params.nframes
        duration = num_frames / sample_rate
        
        print(f" - Canales: {channels} (esperado: 1 [mono])")
        print(f" - Ancho de muestra: {sample_width} bytes (esperado: 2 [16-bit])")
        print(f" - Tasa de muestreo: {sample_rate} Hz (esperado: 16000 Hz)")
        print(f" - Duración: {duration:.2f} segundos")
        
        # Assert properties to guarantee correctness
        assert channels == 1, f"Error: Canales = {channels}, esperado 1"
        assert sample_width == 2, f"Error: Ancho de muestra = {sample_width}, esperado 2"
        assert sample_rate == 16000, f"Error: Tasa de muestreo = {sample_rate}, esperado 16000"
        
    print("\n--- PRUEBA COMPLETADA CON ÉXITO Y FORMATO 100% VERIFICADO ---")

if __name__ == "__main__":
    main()
