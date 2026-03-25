import { useState } from 'react';

export default function SearchBar({ onSearch, placeholder = 'Search prompts…' }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(value.trim());
  };

  const handleClear = () => {
    setValue('');
    onSearch('');
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit} role="search">
      <input
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
      />
      <button type="submit">Search</button>
      {value && <button type="button" onClick={handleClear} className="btn-link">Clear</button>}
    </form>
  );
}
