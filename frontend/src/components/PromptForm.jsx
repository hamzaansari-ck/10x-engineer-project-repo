import { useState, useEffect } from 'react';
import Button from './Button';

export default function PromptForm({ prompt, collections, onSubmit, onCancel }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [description, setDescription] = useState('');
  const [collectionId, setCollectionId] = useState('');
  const [tagsInput, setTagsInput] = useState('');
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (prompt) {
      setTitle(prompt.title || '');
      setContent(prompt.content || '');
      setDescription(prompt.description || '');
      setCollectionId(prompt.collection_id || '');
      setTagsInput((prompt.tags || []).join(', '));
    }
  }, [prompt]);

  const validate = () => {
    const errs = {};
    if (!title.trim()) errs.title = 'Title is required';
    if (!content.trim()) errs.content = 'Content is required';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    const tags = tagsInput.split(',').map((t) => t.trim()).filter(Boolean);
    onSubmit({
      title: title.trim(),
      content: content.trim(),
      description: description.trim() || null,
      collection_id: collectionId || null,
      tags,
    });
  };

  return (
    <form className="prompt-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input id="title" value={title} onChange={(e) => setTitle(e.target.value)} aria-invalid={!!errors.title} />
        {errors.title && <span className="form-error">{errors.title}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="content">Content *</label>
        <textarea id="content" rows={6} value={content} onChange={(e) => setContent(e.target.value)} aria-invalid={!!errors.content} />
        {errors.content && <span className="form-error">{errors.content}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <input id="description" value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div className="form-group">
        <label htmlFor="collection">Collection</label>
        <select id="collection" value={collectionId} onChange={(e) => setCollectionId(e.target.value)}>
          <option value="">None</option>
          {collections.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="tags">Tags (comma-separated)</label>
        <input id="tags" value={tagsInput} onChange={(e) => setTagsInput(e.target.value)} placeholder="python, ai, code-review" />
      </div>
      <div className="form-actions">
        <Button type="submit">{prompt ? 'Update' : 'Create'}</Button>
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
      </div>
    </form>
  );
}
