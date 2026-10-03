const API_BASE = (import.meta.env.VITE_IMA_API_BASE || '').replace(/\/$/, '');

async function getSessionToken(forceRefresh = false) {
  const key = 'ima-public-session-token';
  const cached = localStorage.getItem(key);
  if (cached && !forceRefresh) return cached;
  if (forceRefresh) localStorage.removeItem(key);
  const response = await fetch((API_BASE || '') + '/ima-api/session', { cache: 'no-store' });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || !data.token) throw new Error('IMA session unavailable');
  localStorage.setItem(key, data.token);
  return data.token;
}

async function request(path, options = {}, retry = true) {
  const url = API_BASE ? API_BASE + path : path;
  const token = await getSessionToken(retry === false);
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
  const data = await response.json().catch(() => ({}));
  if (response.status === 401 && retry) {
    localStorage.removeItem('ima-public-session-token');
    return request(path, options, false);
  }
  if (!response.ok) {
    throw new Error(data.error || `IMA HTTP ${response.status}`);
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
