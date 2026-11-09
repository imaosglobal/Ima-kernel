const ROOT = '/Ima-kernel/';
const VERSION_URL = ROOT + 'version.json';

function currentVersion() {
  return document.querySelector('meta[name="ima-build-version"]')?.content || '';
}

function reloadToVersion(version) {
  if (!version || !currentVersion() || version === currentVersion()) return false;
  const target = ROOT + '?v=' + encodeURIComponent(version);
  if (location.href === target) return false;
  // One-shot guard prevents a bad release from causing an infinite reload loop.
  const key = 'ima-last-auto-update';
  if (sessionStorage.getItem(key) === version) return false;
  sessionStorage.setItem(key, version);
  location.replace(target);
  return true;
}

export async function checkForImaUpdate() {
  try {
    const response = await fetch(VERSION_URL + '?ts=' + Date.now(), {
      cache: 'no-store',
      headers: { 'Cache-Control': 'no-cache' },
    });
    if (!response.ok) return { updated: false, checked: false };
    const payload = await response.json();
    return { updated: reloadToVersion(payload?.version), checked: true, version: payload?.version || '' };
  } catch {
    return { updated: false, checked: false };
  }
}

export function startImaUpdatePlane() {
  const run = () => { void checkForImaUpdate(); };
  window.addEventListener('load', run, { once: true });
  // Keep installed/open IMA clients current without asking the user to reinstall.
  const interval = window.setInterval(run, 5 * 60 * 1000);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') run();
  });
  return () => window.clearInterval(interval);
}
