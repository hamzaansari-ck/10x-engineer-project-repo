import { get, post, put, patch, del } from './client';

export const getPrompts = (params = {}) => {
  const query = new URLSearchParams();
  if (params.collection_id) query.set('collection_id', params.collection_id);
  if (params.search) query.set('search', params.search);
  if (params.tags) params.tags.forEach((t) => query.append('tag', t));
  const qs = query.toString();
  return get(`/prompts${qs ? `?${qs}` : ''}`);
};

export const getPrompt = (id) => get(`/prompts/${id}`);
export const createPrompt = (data) => post('/prompts', data);
export const updatePrompt = (id, data) => put(`/prompts/${id}`, data);
export const patchPrompt = (id, data) => patch(`/prompts/${id}`, data);
export const deletePrompt = (id) => del(`/prompts/${id}`);
