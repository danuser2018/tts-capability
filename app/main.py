from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.services.tts_engine import tts_engine
from app.api.endpoints import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the voice model during server startup
    tts_engine.load_model(settings.MODEL_PATH)
    yield
    # No shutdown cleanup is required for ONNX Runtime session

app = FastAPI(
    title="Local Text-to-Speech (TTS) REST API",
    description="On-premise private speech synthesis service using FastAPI and Piper TTS.",
    version="1.0.0",
    lifespan=lifespan
)

# Include the endpoints router
app.include_router(api_router)
