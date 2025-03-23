import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import tempfile
from app.services.transcription_service import TranscriptionService

class TestTranscriptionService:
    def test_transcribe(self):
        # Create a mock audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(b"dummy audio data")
            temp_file_path = temp_file.name
        
        try:
            # Ensure test environment variable is set
            os.environ['TESTING'] = 'True'
            
            # Create transcription service
            service = TranscriptionService()
            
            # Test transcription
            result = service.transcribe(temp_file_path)
            assert result == "This is a test transcription"
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path) 