export default function PromptCard({ prompt, onClick, onDelete }) {
  return (
    <div className="prompt-card" onClick={() => onClick(prompt)} role="button" tabIndex={0} onKeyDown={(e) => e.key === 'Enter' && onClick(prompt)}>
      <h3>{prompt.title}</h3>
      {prompt.description && <p className="prompt-desc">{prompt.description}</p>}
      {prompt.tags?.length > 0 && (
        <div className="tags">
          {prompt.tags.map((tag) => <span key={tag} className="tag">{tag}</span>)}
        </div>
      )}
      <div className="prompt-card-footer">
        <small>{new Date(prompt.created_at).toLocaleDateString()}</small>
        <button
          className="btn btn-danger btn-sm"
          onClick={(e) => { e.stopPropagation(); onDelete(prompt); }}
          aria-label={`Delete ${prompt.title}`}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
