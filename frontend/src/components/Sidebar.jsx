import CollectionList from './CollectionList';
import Button from './Button';

export default function Sidebar({ collections, selectedCollection, onSelectCollection, onDeleteCollection, onNewCollection }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Collections</h2>
        <Button variant="secondary" onClick={onNewCollection}>+ New</Button>
      </div>
      <CollectionList
        collections={collections}
        selected={selectedCollection}
        onSelect={onSelectCollection}
        onDelete={onDeleteCollection}
      />
    </aside>
  );
}
