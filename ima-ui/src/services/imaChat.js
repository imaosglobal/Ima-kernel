import { trackImaEvent } from './analytics';
const API_BASE = (import.meta.env.VITE_IMA_API_BASE || 'https://ima-915m.onrender.com').replace(/\/$/, '');

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
  trackImaEvent('ima_chat_started');
  const data = await request('/ima-api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
  if (!data.response) throw new Error('IMA returned no response');
  trackImaEvent('ima_chat_completed');
  return data.response;
}

export async function getImaRuntime() {
  return request('/ima-api/runtime', { cache: 'no-store' });
}


export async function getMemoryConsent() {
  return request('/ima-api/memory/consent', { cache: 'no-store' });
}

export async function setMemoryConsent(status) {
  return request('/ima-api/memory/consent', {
    method: 'PUT',
    body: JSON.stringify({ status }),
  });
}

export async function exportMemory() {
  return request('/ima-api/memory/export', { cache: 'no-store' });
}

export async function deleteMemory() {
  return request('/ima-api/memory', { method: 'DELETE' });
}


export async function getAuthConfig() {
  const response = await fetch((API_BASE || '') + '/ima-api/auth/config', { cache: 'no-store' });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || 'IMA auth config unavailable');
  return data;
}

export async function signInWithGoogleCredential(credential) {
  const response = await fetch((API_BASE || '') + '/ima-api/auth/google', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ credential }),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || !data.token) throw new Error(data.error || 'Google sign-in failed');
  localStorage.setItem('ima-public-session-token', data.token);
  if (data.user) localStorage.setItem('ima-google-user', JSON.stringify(data.user));
  trackImaEvent('ima_google_signin_completed');
  return data;
}

export function getStoredGoogleUser() {
  try { return JSON.parse(localStorage.getItem('ima-google-user') || 'null'); } catch { return null; }
}

export function signOutIma() {
  localStorage.removeItem('ima-public-session-token');
  localStorage.removeItem('ima-google-user');
}
