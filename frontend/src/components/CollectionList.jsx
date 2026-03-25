export default function CollectionList({ collections, selected, onSelect, onDelete }) {
  return (
    <ul className="collection-list" role="listbox" aria-label="Collections">
      <li
        role="option"
        aria-selected={!selected}
        className={!selected ? 'active' : ''}
        onClick={() => onSelect(null)}
        onKeyDown={(e) => e.key === 'Enter' && onSelect(null)}
        tabIndex={0}
      >
        All Prompts
      </li>
      {collections.map((c) => (
        <li
          key={c.id}
          role="option"
          aria-selected={selected === c.id}
          className={selected === c.id ? 'active' : ''}
          onClick={() => onSelect(c.id)}
          onKeyDown={(e) => e.key === 'Enter' && onSelect(c.id)}
          tabIndex={0}
        >
          <span>{c.name}</span>
          <button
            className="btn-icon"
            onClick={(e) => { e.stopPropagation(); onDelete(c); }}
            aria-label={`Delete ${c.name}`}
          >
            &times;
          </button>
        </li>
      ))}
    </ul>
  );
}
