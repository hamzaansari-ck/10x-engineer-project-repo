import { useState } from 'react';
import Button from './Button';

export default function CollectionForm({ onSubmit, onCancel }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) { setError('Name is required'); return; }
    onSubmit({ name: name.trim(), description: description.trim() || null });
  };

  return (
    <form className="prompt-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="col-name">Name *</label>
        <input id="col-name" value={name} onChange={(e) => setName(e.target.value)} aria-invalid={!!error} />
        {error && <span className="form-error">{error}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="col-desc">Description</label>
        <input id="col-desc" value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div className="form-actions">
        <Button type="submit">Create Collection</Button>
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
      </div>
    </form>
  );
}
