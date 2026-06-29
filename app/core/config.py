import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Basic logging configuration for the entire application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class Settings:
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/es_ES-carlfm-x_low.onnx")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
