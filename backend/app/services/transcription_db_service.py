from datetime import datetime
from app.database import db
from app.models.transcription import Transcription

class TranscriptionDBService:
    """Service for database operations related to transcriptions"""
    
    @staticmethod
    def create_transcription(filename, unique_filename, text):
        """
        Create a new transcription record in the database
        
        Args:
            filename (str): Original filename
            unique_filename (str): Unique filename for storage
            text (str): Transcribed text
            
        Returns:
            Transcription: The created transcription object
        """
        transcription = Transcription(
            filename=filename,
            unique_filename=unique_filename,
            text=text,
            created_at=datetime.now()
        )
        
        db.session.add(transcription)
        db.session.commit()
        
        return transcription
    
    @staticmethod
    def get_all_transcriptions():
        """
        Get all transcriptions ordered by creation date
        
        Returns:
            list: List of Transcription objects
        """
        return Transcription.query.order_by(Transcription.created_at.desc()).all()
    
    @staticmethod
    def get_transcription_by_id(id):
        """
        Get a transcription by ID
        
        Args:
            id (int): Transcription ID
            
        Returns:
            Transcription: The transcription object or None if not found
        """
        return Transcription.query.get(id)
    
    @staticmethod
    def search_transcriptions(query):
        """
        Search transcriptions by filename
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching Transcription objects
        """
        return Transcription.query.filter(
            Transcription.filename.like(f"%{query}%")
        ).order_by(Transcription.created_at.desc()).all() 