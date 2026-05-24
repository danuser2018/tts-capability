import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

# Configuración básica de logging para toda la aplicación
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class Settings:
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/es_ES-carlfm-x_low.onnx")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
