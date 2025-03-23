import axios from 'axios';

const API_BASE_URL = '/api';

export async function fetchTranscriptions() {
  try {
    const response = await axios.get(`${API_BASE_URL}/transcriptions`);
    return response.data;
  } catch (error) {
    if (process.env.NODE_ENV !== 'test') {
      console.error('Error fetching transcriptions:', error);
    }
    throw new Error('Failed to fetch transcriptions');
  }
}

export async function searchTranscriptions(query) {
  try {
    const response = await axios.get(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    if (process.env.NODE_ENV !== 'test') {
      console.error('Error searching transcriptions:', error);
    }
    throw new Error('Failed to search transcriptions');
  }
}

export async function uploadFiles(files, onProgress) {
  try {
    const formData = new FormData();
    
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });
    
    const response = await axios.post(`${API_BASE_URL}/transcribe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: progressEvent => {
        if (onProgress) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      }
    });
    
    return response.data;
  } catch (error) {
    if (process.env.NODE_ENV !== 'test') {
      console.error('Error uploading files:', error);
    }
    throw new Error(`Failed to upload files: ${error.message}`);
  }
} 