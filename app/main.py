from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

# Error name mapping according to status code for ADR-004
ERROR_NAMES = {
    400: "BadRequest",
    401: "Unauthorized",
    403: "Forbidden",
    404: "NotFound",
    422: "ValidationError",
    500: "InternalServerError",
}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle FastAPI HTTPExceptions and format them according to ADR-004.
    """
    error_name = ERROR_NAMES.get(exc.status_code, "HTTPException")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_name,
            "message": exc.detail,
            "status": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle FastAPI validation errors and format them according to ADR-004.
    """
    errors_summary = "; ".join([f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in exc.errors()])
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": f"Validation failed: {errors_summary}",
            "status": 422
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors and format them according to ADR-004.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": f"An unexpected error occurred: {str(exc)}",
            "status": 500
        }
    )

# Include the endpoints router
app.include_router(api_router)
