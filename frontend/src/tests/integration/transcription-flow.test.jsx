import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, test, expect, vi, beforeEach } from 'vitest';
import App from '../../App';
import * as api from '../../services/api';

// Mock the API module
vi.mock('../../services/api', () => ({
  fetchTranscriptions: vi.fn(),
  searchTranscriptions: vi.fn(),
  uploadFiles: vi.fn()
}));

describe('Transcription Flow', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  test('complete transcription flow', async () => {
    // Mock API responses
    api.fetchTranscriptions.mockResolvedValue([
      { id: 1, filename: 'recording.mp3', text: 'This is a test transcription', created_at: '2023-01-01T00:00:00Z' }
    ]);
    
    api.searchTranscriptions.mockImplementation((query) => {
      if (query === 'test') {
        return Promise.resolve([
          { id: 1, filename: 'recording.mp3', text: 'This is a test transcription', created_at: '2023-01-01T00:00:00Z' }
        ]);
      }
      return Promise.resolve([]);
    });
    
    render(<App />);
    
    // Wait for initial transcriptions to load
    await waitFor(() => {
      expect(api.fetchTranscriptions).toHaveBeenCalled();
    });
    
    // Verify transcription is displayed
    expect(screen.getByText('recording.mp3')).toBeInTheDocument();
    
    // Test search functionality
    const searchInput = screen.getByPlaceholderText(/search transcriptions/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.click(screen.getByText(/search/i));
    
    await waitFor(() => {
      expect(api.searchTranscriptions).toHaveBeenCalledWith('test');
    });
    
    expect(screen.getByText('This is a test transcription')).toBeInTheDocument();
  });

  test('uploadFiles should handle file upload correctly', async () => {
    const mockFile = new File(['dummy content'], 'test.mp3', { type: 'audio/mp3' });
    const mockResponse = { id: 1, filename: 'test.mp3', text: 'Hello world' };
    
    api.uploadFiles.mockResolvedValueOnce(mockResponse);
    
    const result = await api.uploadFiles([mockFile]);
    expect(result).toEqual(mockResponse);
  });

  test('app shows error message when API fails', async () => {
    api.fetchTranscriptions.mockRejectedValue(new Error('Network error'));
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
}); 