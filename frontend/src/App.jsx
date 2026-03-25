import { useState, useEffect, useCallback } from 'react';
import Layout from './components/Layout';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import PromptList from './components/PromptList';
import PromptDetail from './components/PromptDetail';
import PromptForm from './components/PromptForm';
import CollectionForm from './components/CollectionForm';
import Modal from './components/Modal';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import * as promptsApi from './api/prompts';
import * as collectionsApi from './api/collections';

export default function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedCollection, setSelectedCollection] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [view, setView] = useState('list'); // list | detail | create | edit

  const [showCollectionForm, setShowCollectionForm] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (selectedCollection) params.collection_id = selectedCollection;
      if (searchQuery) params.search = searchQuery;
      const [promptRes, colRes] = await Promise.all([
        promptsApi.getPrompts(params),
        collectionsApi.getCollections(),
      ]);
      setPrompts(promptRes.prompts);
      setCollections(colRes.collections);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [selectedCollection, searchQuery]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleCreatePrompt = async (data) => {
    try {
      await promptsApi.createPrompt(data);
      setView('list');
      fetchData();
    } catch (err) { setError(err.message); }
  };

  const handleUpdatePrompt = async (data) => {
    try {
      await promptsApi.updatePrompt(selectedPrompt.id, data);
      setView('list');
      setSelectedPrompt(null);
      fetchData();
    } catch (err) { setError(err.message); }
  };

  const handleDeletePrompt = async () => {
    try {
      await promptsApi.deletePrompt(confirmDelete.id);
      setConfirmDelete(null);
      if (view === 'detail') setView('list');
      setSelectedPrompt(null);
      fetchData();
    } catch (err) { setError(err.message); }
  };

  const handleCreateCollection = async (data) => {
    try {
      await collectionsApi.createCollection(data);
      setShowCollectionForm(false);
      fetchData();
    } catch (err) { setError(err.message); }
  };

  const handleDeleteCollection = async (col) => {
    if (!window.confirm(`Delete collection "${col.name}"? Prompts will be kept.`)) return;
    try {
      await collectionsApi.deleteCollection(col.id);
      if (selectedCollection === col.id) setSelectedCollection(null);
      fetchData();
    } catch (err) { setError(err.message); }
  };

  const renderContent = () => {
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} onRetry={fetchData} />;

    if (view === 'create') {
      return (
        <PromptForm collections={collections} onSubmit={handleCreatePrompt} onCancel={() => setView('list')} />
      );
    }

    if (view === 'edit' && selectedPrompt) {
      return (
        <PromptForm prompt={selectedPrompt} collections={collections} onSubmit={handleUpdatePrompt} onCancel={() => setView('detail')} />
      );
    }

    if (view === 'detail' && selectedPrompt) {
      return (
        <PromptDetail
          prompt={selectedPrompt}
          onEdit={() => setView('edit')}
          onDelete={(p) => setConfirmDelete(p)}
          onBack={() => { setView('list'); setSelectedPrompt(null); }}
        />
      );
    }

    return (
      <>
        <SearchBar onSearch={(q) => setSearchQuery(q)} />
        <PromptList
          prompts={prompts}
          onSelect={(p) => { setSelectedPrompt(p); setView('detail'); }}
          onDelete={(p) => setConfirmDelete(p)}
        />
      </>
    );
  };

  return (
    <>
      <Layout
        header={<Header onNewPrompt={() => { setSelectedPrompt(null); setView('create'); }} />}
        sidebar={
          <Sidebar
            collections={collections}
            selectedCollection={selectedCollection}
            onSelectCollection={(id) => { setSelectedCollection(id); setView('list'); setSelectedPrompt(null); }}
            onDeleteCollection={handleDeleteCollection}
            onNewCollection={() => setShowCollectionForm(true)}
          />
        }
      >
        {renderContent()}
      </Layout>

      {showCollectionForm && (
        <Modal title="New Collection" onClose={() => setShowCollectionForm(false)}>
          <CollectionForm onSubmit={handleCreateCollection} onCancel={() => setShowCollectionForm(false)} />
        </Modal>
      )}

      {confirmDelete && (
        <Modal title="Confirm Delete" onClose={() => setConfirmDelete(null)}>
          <p>Delete &quot;{confirmDelete.title}&quot;? This cannot be undone.</p>
          <div className="form-actions">
            <button className="btn btn-danger" onClick={handleDeletePrompt}>Delete</button>
            <button className="btn btn-secondary" onClick={() => setConfirmDelete(null)}>Cancel</button>
          </div>
        </Modal>
      )}
    </>
  );
}
