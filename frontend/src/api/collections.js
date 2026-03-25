import { get, post, del } from './client';

export const getCollections = () => get('/collections');
export const createCollection = (data) => post('/collections', data);
export const deleteCollection = (id) => del(`/collections/${id}`);
