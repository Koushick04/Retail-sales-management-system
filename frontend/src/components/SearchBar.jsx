// src/components/SearchBar.jsx

function SearchBar({ value, onChange, onSearch, suggestions = [], onSelectSuggestion }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  return (
    <div className="card search-bar">
      <label className="label">Search</label>
      <div className="search-row">
        <input
          type="text"
          placeholder="Search by customer name or phone..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input search-input"
        />
        <button type="button" className="primary-button" onClick={onSearch}>
          Search
        </button>
      </div>

      {suggestions.length > 0 && (
        <div className="suggestions-panel">
          {suggestions.map((name) => (
            <button
              key={name}
              type="button"
              className="suggestion-item"
              onClick={() => onSelectSuggestion(name)}
            >
              {name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
