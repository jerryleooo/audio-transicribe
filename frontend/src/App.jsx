import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import TranscriptionList from './components/TranscriptionList';
import SearchBar from './components/SearchBar';
import { fetchTranscriptions, searchTranscriptions } from './services/api';

function App() {
  const [transcriptions, setTranscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  useEffect(() => {
    loadTranscriptions();
  }, []);
  
  const loadTranscriptions = async () => {
    setLoading(true);
    try {
      const data = await fetchTranscriptions();
      setTranscriptions(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSearch = async (query) => {
    setSearchQuery(query);
    setLoading(true);
    
    try {
      if (query) {
        const results = await searchTranscriptions(query);
        setTranscriptions(results);
      } else {
        await loadTranscriptions();
      }
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleUploadComplete = (results) => {
    setTranscriptions(prevTranscriptions => [...results, ...prevTranscriptions]);
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">Audio Transcription App</h1>
        <p className="text-gray-400 mt-2">Upload audio files and get transcriptions</p>
      </header>
      
      <FileUpload onUploadComplete={handleUploadComplete} />
      
      <div className="mt-8">
        <h2 className="text-2xl font-semibold text-white mb-4">Transcriptions</h2>
        <SearchBar onSearch={handleSearch} />
        
        {error && (
          <div className="bg-red-500 text-white p-4 rounded-md my-4">
            Error: {error}
          </div>
        )}
        
        {loading ? (
          <div className="text-gray-400 my-4">Loading transcriptions...</div>
        ) : (
          <TranscriptionList 
            transcriptions={transcriptions} 
            searchQuery={searchQuery}
          />
        )}
      </div>
    </div>
  );
}

export default App; 