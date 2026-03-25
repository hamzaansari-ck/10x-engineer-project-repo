const BASE_URL = '/api';

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  const response = await fetch(url, config);

  if (response.status === 204) return null;

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(error.detail || `Request failed (${response.status})`);
  }

  return response.json();
}

export const get = (path) => request(path);
export const post = (path, data) => request(path, { method: 'POST', body: JSON.stringify(data) });
export const put = (path, data) => request(path, { method: 'PUT', body: JSON.stringify(data) });
export const patch = (path, data) => request(path, { method: 'PATCH', body: JSON.stringify(data) });
export const del = (path) => request(path, { method: 'DELETE' });
