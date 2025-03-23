import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };
  
  const handleClear = () => {
    setQuery('');
    onSearch('');
  };
  
  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} role="form">
        <input
          type="text"
          className="search-input"
          placeholder="Search transcriptions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="search-button">
          Search
        </button>
        {query && (
          <button
            type="button"
            onClick={handleClear}
            className="clear-button"
          >
            Clear
          </button>
        )}
      </form>
    </div>
  );
}

export default SearchBar; 