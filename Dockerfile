FROM python:3.11-slim

# Install system dependencies including espeak-ng for phonemization
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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
