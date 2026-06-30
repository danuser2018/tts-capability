# Stage 1: Download voice models to reduce final image size and simplify deployments
FROM alpine:latest AS downloader

RUN apk add --no-cache curl

WORKDIR /models

# Download Spanish voice model (carlfm x_low, natively 16kHz)
RUN curl -L -S -f -O https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/x_low/es_ES-carlfm-x_low.onnx
RUN curl -L -S -f -O https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/x_low/es_ES-carlfm-x_low.onnx.json

# Stage 2: Main Application Runtime
FROM python:3.11-slim

# Install system dependencies including espeak-ng for phonemization
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy downloaded models into local models directory
COPY --from=downloader /models /app/models

# Copy source code and tests
COPY app /app/app
COPY tests /app/tests

# Environment variables
ENV PORT=8000
ENV TTS_MODEL_NAME=es_ES-carlfm-x_low
ENV TTS_MODEL_DIR=/app/models

EXPOSE 8000

# Start server using uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
