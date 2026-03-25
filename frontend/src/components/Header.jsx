export default function Header({ onNewPrompt }) {
  return (
    <header className="app-header">
      <h1>🧪 PromptLab</h1>
      <button className="btn btn-primary" onClick={onNewPrompt}>+ New Prompt</button>
    </header>
  );
}
