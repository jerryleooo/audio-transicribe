import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

class FileService:
    """Service for handling file operations"""
    
    @staticmethod
    def save_audio_file(file):
        """
        Save an uploaded audio file to disk
        
        Args:
            file: The uploaded file object
            
        Returns:
            tuple: (original_filename, unique_filename, file_path)
        """
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save file to disk using the configured upload folder
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        return original_filename, unique_filename, file_path 