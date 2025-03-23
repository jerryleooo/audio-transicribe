import React, { useState } from 'react';
import { uploadFiles } from '../services/api';
import './FileUpload.css';

function FileUpload({ onUploadComplete }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (files.length === 0) {
      setError('Please select at least one file');
      return;
    }
    
    setUploading(true);
    setProgress(0);
    
    try {
      const results = await uploadFiles(files, (progressPercentage) => {
        setProgress(progressPercentage);
      });
      
      setFiles([]);
      setUploading(false);
      setProgress(0);
      
      if (onUploadComplete) {
        onUploadComplete(results);
      }
    } catch (error) {
      setError(error.message || 'Upload failed');
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            disabled={uploading}
            className="file-input"
            accept="audio/*"
          />
          <button 
            type="submit" 
            disabled={uploading || files.length === 0}
            className="upload-button"
          >
            {uploading ? 'Uploading...' : 'Upload Files'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        {uploading && (
          <div className="progress-container">
            <div 
              className="progress-bar" 
              style={{ width: `${progress}%` }}
            ></div>
            <div className="progress-text">{Math.round(progress)}%</div>
          </div>
        )}
        
        {files.length > 0 && (
          <div className="selected-files">
            <h3>Selected Files:</h3>
            <ul>
              {files.map((file, index) => (
                <li key={index}>{file.name}</li>
              ))}
            </ul>
          </div>
        )}
      </form>
    </div>
  );
}

export default FileUpload; 