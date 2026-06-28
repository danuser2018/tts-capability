import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test successful call to healthcheck
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_synthesize_success():
    """
    Test successful speech synthesis using mock.
    """
    dummy_wav = b"RIFF\x00\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00u\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    with patch("app.api.endpoints.tts_engine.synthesize", return_value=dummy_wav) as mock_synth:
        response = client.post("/v1/synthesize", json={"msg": "Hola mundo"})
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"
        assert response.content == dummy_wav
        mock_synth.assert_called_once_with("Hola mundo")

def test_synthesize_empty_message():
    """
    Test error response when message is empty or whitespace only.
    """
    response = client.post("/v1/synthesize", json={"msg": "   "})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_synthesize_missing_msg_field():
    """
    Test validation error when 'msg' field is missing.
    """
    response = client.post("/v1/synthesize", json={})
    assert response.status_code == 422

def test_synthesize_error_handling():
    """
    Test server error propagation when the synthesis engine raises an exception.
    """
    with patch("app.api.endpoints.tts_engine.synthesize", side_effect=Exception("ONNX Runtime error")):
        response = client.post("/v1/synthesize", json={"msg": "Hola"})
        assert response.status_code == 500
        assert "speech synthesis engine failure" in response.json()["detail"]
