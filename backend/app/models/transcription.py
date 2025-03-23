from datetime import datetime
from app.database import db

class Transcription(db.Model):
    __tablename__ = "transcriptions"

    id = db.Column(db.Integer, primary_key=True, index=True)
    filename = db.Column(db.String(255), nullable=False, index=True)
    unique_filename = db.Column(db.String(255), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Transcription {self.filename}>'

    def to_json(self):
        """Convert model to JSON serializable dictionary"""
        return {
            "id": self.id,
            "filename": self.filename,
            "unique_filename": self.unique_filename,
            "text": self.text,
            "created_at": self.created_at.isoformat()
        } 