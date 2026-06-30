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
    def __init__(self):
        self.TTS_MODEL_NAME: str = os.getenv("TTS_MODEL_NAME", "es_ES-carlfm-x_low")
        self.TTS_MODEL_DIR: str = os.getenv("TTS_MODEL_DIR", "models")
        self.PORT: int = int(os.getenv("PORT", "8000"))
        
        # Validation
        if not self.TTS_MODEL_NAME.strip():
            raise ValueError("TTS_MODEL_NAME cannot be empty or consist only of whitespace.")

    @property
    def model_path(self) -> str:
        """Returns the path to the ONNX model file, prioritizing deprecated MODEL_PATH if set."""
        env_model_path = os.getenv("MODEL_PATH")
        if env_model_path:
            return env_model_path
        return os.path.join(self.TTS_MODEL_DIR, f"{self.TTS_MODEL_NAME}.onnx")

    @property
    def config_path(self) -> str:
        """Returns the path to the JSON config file, prioritizing deprecated MODEL_PATH if set."""
        env_model_path = os.getenv("MODEL_PATH")
        if env_model_path:
            return f"{env_model_path}.json"
        return os.path.join(self.TTS_MODEL_DIR, f"{self.TTS_MODEL_NAME}.onnx.json")

settings = Settings()
