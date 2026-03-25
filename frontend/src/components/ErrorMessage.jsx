export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-message" role="alert">
      <p>⚠️ {message}</p>
      {onRetry && <button onClick={onRetry}>Retry</button>}
    </div>
  );
}
