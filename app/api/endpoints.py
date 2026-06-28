from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from app.services.tts_engine import tts_engine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SynthesizeRequest(BaseModel):
    """
    Request model for speech synthesis endpoint.
    """
    msg: str = Field(
        ...,
        description="Text message to synthesize to speech.",
        json_schema_extra={"example": "Hola mundo"}
    )

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/v1/synthesize")
async def synthesize(request: SynthesizeRequest):
    """
    Synthesize text message and return a binary WAV audio file
    formatted as PCM 16-bit mono 16000 Hz.
    """
    # Clean and validate input message
    cleaned_msg = request.msg.strip()
    if not cleaned_msg:
        raise HTTPException(
            status_code=400,
            detail="The 'msg' parameter cannot be empty or consist only of whitespace."
        )

    try:
        audio_bytes = tts_engine.synthesize(cleaned_msg)
        return Response(content=audio_bytes, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Error during speech synthesis for text '{cleaned_msg}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal speech synthesis engine failure: {str(e)}"
        )
