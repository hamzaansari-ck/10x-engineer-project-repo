import PromptCard from './PromptCard';

export default function PromptList({ prompts, onSelect, onDelete }) {
  if (prompts.length === 0) {
    return <div className="empty-state">No prompts yet. Create your first one!</div>;
  }

  return (
    <div className="prompt-grid">
      {prompts.map((p) => (
        <PromptCard key={p.id} prompt={p} onClick={onSelect} onDelete={onDelete} />
      ))}
    </div>
  );
}
