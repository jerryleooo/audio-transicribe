import React from 'react';
import './TranscriptionList.css';

function TranscriptionList({ transcriptions, searchQuery }) {
  if (transcriptions.length === 0) {
    return (
      <div className="transcription-list-empty">
        {searchQuery 
          ? `No transcriptions found matching "${searchQuery}"`
          : "No transcriptions available. Upload an audio file to get started."}
      </div>
    );
  }

  return (
    <div className="transcription-list">
      {transcriptions.map((transcription) => (
        <div 
          key={transcription.id} 
          className="transcription-item"
        >
          <h3 className="transcription-title">
            {transcription.filename}
          </h3>
          <p className="transcription-text">{transcription.text}</p>
          <div className="transcription-date">
            {new Date(transcription.created_at).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
}

export default TranscriptionList; 