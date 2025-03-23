from abc import ABC, abstractmethod

class BaseTranscriptionService(ABC):
    """Abstract base class for transcription services"""
    
    @abstractmethod
    def transcribe(self, audio_path):
        """
        Transcribe audio file to text
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        pass
    
    @abstractmethod
    def preprocess_audio(self, file_path):
        """
        Preprocess audio file before transcription
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            tuple: Processed audio data and sample rate
        """
        pass 