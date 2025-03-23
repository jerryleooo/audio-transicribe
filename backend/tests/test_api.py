import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import tempfile
import json
from app.main import create_app
from app.database import db

@pytest.fixture
def app():
    app = create_app('testing')  # 使用预定义的测试配置
    
    # Create the database and load test data
    with app.app_context():
        from app.database import init_db
        init_db()
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "status" in data
    assert data["status"] == "ok"

def test_get_transcriptions(client):
    response = client.get("/transcriptions")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_search_transcriptions_empty_query(client):
    response = client.get("/search")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_search_transcriptions_with_results(client):
    # Create a temporary file, doesn't need to be valid audio
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        # Write some data, doesn't need to be valid audio
        temp_file.write(b"dummy audio data")
        temp_file.flush()
        
        # Upload the file
        with open(temp_file.name, "rb") as f:
            response = client.post(
                "/transcribe",
                data={"files": (f, "test_audio.wav", "audio/wav")}
            )
        
        assert response.status_code == 200
    
    # Now search for the transcription
    response = client.get("/search?query=test_audio")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_search_transcriptions_no_results(client):
    response = client.get("/search?query=nonexistent")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_transcribe_no_files(client):
    response = client.post("/transcribe")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_transcribe_audio(client):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        # Write some data
        temp_file.write(b"dummy audio data")
        temp_file.flush()
        
        # Upload the file
        with open(temp_file.name, "rb") as f:
            response = client.post(
                "/transcribe",
                data={"files": (f, "test_audio.wav", "audio/wav")}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]
        assert "filename" in data[0]
        assert "text" in data[0]
        assert data[0]["filename"] == "test_audio.wav" 