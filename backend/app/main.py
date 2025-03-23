from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import logging

from app.database import db
from app.models.transcription import Transcription
from app.services.transcription_service import TranscriptionService
from app.config import config
from app.error_handlers import register_error_handlers
from app.services.file_service import FileService
from app.services.transcription_db_service import TranscriptionDBService
from app.commands import register_commands

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure logging
    if not app.debug:
        # In production, log to file
        file_handler = logging.FileHandler(os.path.join(app.instance_path, 'app.log'))
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
    
    # Handle different types of config parameters
    if isinstance(config_name, dict):
        # If a dictionary is passed, update config directly
        app.config.from_mapping(config_name)
        
        # Set default values for required configs if not provided
        app.config.setdefault('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads'))
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        
        # Ensure database URL is set with absolute path
        if 'SQLALCHEMY_DATABASE_URI' not in app.config:
            db_url = os.environ.get('DATABASE_URL', 'sqlite:////app/instance/prod.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # Determine configuration type from string
        if config_name is None:
            config_name = os.environ.get('FLASK_ENV', 'default')
        
        # Load configuration from object
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
    
    # Log the database URL being used
    app.logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Initialize database on startup
    with app.app_context():
        app.logger.info(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
        app.logger.info(f"Instance path: {app.instance_path}")
        app.logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
        db.create_all()
        app.logger.info("Database tables created (if they didn't exist)")
    
    # Initialize services at application level
    app.logger.info("Initializing application services...")
    app.transcription_service = TranscriptionService()
    app.file_service = FileService()
    app.db_service = TranscriptionDBService()
    app.logger.info("Application services initialized successfully!")
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})
    
    # Transcribe audio endpoint
    @app.route('/transcribe', methods=['POST'])
    def transcribe_audio():
        """Endpoint for transcribing audio files"""
        # Validate request
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist('files')
        results = []
        
        for file in files:
            # Handle file upload
            original_filename, unique_filename, file_path = app.file_service.save_audio_file(file)
            
            # Transcribe audio
            transcribed_text = app.transcription_service.transcribe(file_path)
            
            # Save to database
            transcription = app.db_service.create_transcription(
                original_filename, 
                unique_filename, 
                transcribed_text
            )
            
            # Add to results
            results.append(transcription.to_json())
        
        return jsonify(results)
    
    # Get all transcriptions endpoint
    @app.route('/transcriptions', methods=['GET'])
    def get_transcriptions():
        """Endpoint for getting all transcriptions"""
        transcriptions = app.db_service.get_all_transcriptions()
        return jsonify([t.to_json() for t in transcriptions])
    
    # Search transcriptions endpoint
    @app.route('/search', methods=['GET'])
    def search_transcriptions():
        """Endpoint for searching transcriptions"""
        query = request.args.get('query', '')
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        transcriptions = app.db_service.search_transcriptions(query)
        
        return jsonify([t.to_json() for t in transcriptions])
    
    # Get transcription by ID
    @app.route('/transcriptions/<int:id>', methods=['GET'])
    def get_transcription(id):
        """Endpoint for getting a transcription by ID"""
        transcription = app.db_service.get_transcription_by_id(id)
        
        if not transcription:
            return jsonify({"error": "Not found", "message": f"Transcription with ID {id} not found"}), 404
        
        return jsonify(transcription.to_json())
    
    # Register custom commands
    register_commands(app)
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 