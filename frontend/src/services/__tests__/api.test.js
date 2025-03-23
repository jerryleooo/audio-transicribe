import { fetchTranscriptions, searchTranscriptions } from '../api';
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import axios from 'axios';

// Mock axios
vi.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });
  
  test('fetchTranscriptions should return transcriptions data', async () => {
    const mockData = [
      { id: 1, filename: 'test.mp3', text: 'Hello world', created_at: '2023-01-01T00:00:00Z' }
    ];
    
    axios.get.mockResolvedValueOnce({ data: mockData });
    
    const result = await fetchTranscriptions();
    expect(result).toEqual(mockData);
    expect(axios.get).toHaveBeenCalledWith('/api/transcriptions');
  });
  
  test('searchTranscriptions should return filtered transcriptions', async () => {
    const mockData = [
      { id: 1, filename: 'test.mp3', text: 'Hello world', created_at: '2023-01-01T00:00:00Z' }
    ];
    
    axios.get.mockResolvedValueOnce({ data: mockData });
    
    const result = await searchTranscriptions('test');
    expect(result).toEqual(mockData);
    expect(axios.get).toHaveBeenCalledWith('/api/search?query=test');
  });
  
  test('fetchTranscriptions should handle errors', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'));
    
    await expect(fetchTranscriptions()).rejects.toThrow('Failed to fetch transcriptions');
  });
}); 