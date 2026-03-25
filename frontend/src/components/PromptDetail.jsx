import Button from './Button';

export default function PromptDetail({ prompt, onEdit, onDelete, onBack }) {
  return (
    <div className="prompt-detail">
      <button className="btn-link" onClick={onBack}>&larr; Back to list</button>
      <h2>{prompt.title}</h2>
      {prompt.description && <p className="prompt-desc">{prompt.description}</p>}
      {prompt.tags?.length > 0 && (
        <div className="tags">
          {prompt.tags.map((tag) => <span key={tag} className="tag">{tag}</span>)}
        </div>
      )}
      <pre className="prompt-content">{prompt.content}</pre>
      <div className="prompt-meta">
        <small>Created: {new Date(prompt.created_at).toLocaleString()}</small>
        <small>Updated: {new Date(prompt.updated_at).toLocaleString()}</small>
      </div>
      <div className="form-actions">
        <Button onClick={onEdit}>Edit</Button>
        <Button variant="danger" onClick={() => onDelete(prompt)}>Delete</Button>
      </div>
    </div>
  );
}
