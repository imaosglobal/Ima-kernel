const API_BASE = (import.meta.env.VITE_IMA_API_BASE || '').replace(/\/$/, '');

function getUserId() {
  const key = 'ima-public-user-id';
  let value = localStorage.getItem(key);
  if (!value) {
    value = crypto?.randomUUID?.() ||
      ('ima-' + Date.now() + '-' + Math.random().toString(36).slice(2));
    localStorage.setItem(key, value);
  }
  return value;
}

async function request(path, options = {}) {
  const url = API_BASE ? API_BASE + path : path;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-IMA-User': getUserId(),
      ...(options.headers || {}),
    },
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || data.detail || `IMA HTTP ${response.status}`);
  }
  return data;
}

export async function askIma(message) {
  const data = await request('/ima-api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
  if (!data.response) throw new Error('IMA returned no response');
  return data.response;
}

export async function getImaRuntime() {
  return request('/ima-api/runtime', { cache: 'no-store' });
}
