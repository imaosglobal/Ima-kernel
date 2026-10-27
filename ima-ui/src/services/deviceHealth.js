const ENDPOINT = 'https://tenpzpvqvtezezaossjd.supabase.co/functions/v1/ima-device-health';
const APP_KEY = 'sb_publishable_N11sNqk4VfPFQZ_RQsyMNw_HIV04Vdt';
const DEVICE_KEY = 'ima-device-health-key-v1';
const LAST_REPORT = 'ima-device-health-last-report-v1';
const REPORT_WINDOW_MS = 20 * 60 * 60 * 1000;
const errors = [];

function deviceKey() {
  try {
    let key = localStorage.getItem(DEVICE_KEY);
    if (!key) {
      key = crypto.randomUUID();
      localStorage.setItem(DEVICE_KEY, key);
    }
    return key;
  } catch {
    return 'ephemeral-' + Math.random().toString(16).slice(2);
  }
}

function captureError(value) {
  if (errors.length >= 10) return;
  const message = value instanceof Error ? value.message : String(value || 'unknown');
  errors.push(message.slice(0, 300));
}

if (typeof window !== 'undefined') {
  window.addEventListener('error', event => captureError(event.error || event.message));
  window.addEventListener('unhandledrejection', event => captureError(event.reason));
}

async function runtimeCheck() {
  const started = performance.now();
  try {
    const response = await fetch('https://ima-915m.onrender.com/ima-api/runtime', { cache: 'no-store' });
    const data = await response.json().catch(() => ({}));
    return { ok: response.ok, status: response.status, ms: Math.round(performance.now() - started), version: data.version || 'unknown' };
  } catch (error) {
    captureError(error);
    return { ok: false, status: 0, ms: Math.round(performance.now() - started), error: String(error?.message || error).slice(0, 200) };
  }
}

function collectDom() {
  const links = [...document.querySelectorAll('a[href]')];
  const buttons = [...document.querySelectorAll('button')];
  const sameOriginLinks = links.filter(a => {
    try { return new URL(a.href, location.href).origin === location.origin; } catch { return false; }
  });
  return {
    links: links.length,
    buttons: buttons.length,
    same_origin_links: sameOriginLinks.length,
    empty_links: links.filter(a => !(a.getAttribute('href') || '').trim()).length,
    disabled_buttons: buttons.filter(b => b.disabled).length,
  };
}

async function collectPwa() {
  let serviceWorker = false;
  try { serviceWorker = 'serviceWorker' in navigator && !!(await navigator.serviceWorker.getRegistration()); } catch {}
  return {
    service_worker: serviceWorker,
    standalone: window.matchMedia?.('(display-mode: standalone)').matches || navigator.standalone === true,
    online: navigator.onLine,
  };
}

export async function reportDeviceHealth(force = false) {
  try {
    const last = Number(localStorage.getItem(LAST_REPORT) || 0);
    if (!force && Date.now() - last < REPORT_WINDOW_MS) return { accepted: false, reason: 'local_window_not_due' };

    const [runtime, pwa] = await Promise.all([runtimeCheck(), collectPwa()]);
    const payload = {
      app_version: 'ima-ui-2026.10-device-bridge-v1',
      platform: navigator.platform || 'unknown',
      user_agent: navigator.userAgent || '',
      screen: { width: innerWidth, height: innerHeight, dpr: window.devicePixelRatio || 1 },
      runtime,
      network: {
        online: navigator.onLine,
        effective_type: navigator.connection?.effectiveType || 'unknown',
        rtt: Number.isFinite(navigator.connection?.rtt) ? navigator.connection.rtt : null,
      },
      capabilities: collectDom(),
      errors,
      pwa,
      locale: document.documentElement.lang || navigator.language || 'unknown',
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'unknown',
    };
    const response = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: APP_KEY,
        'x-ima-device-key': deviceKey(),
      },
      body: JSON.stringify(payload),
      keepalive: true,
    });
    const data = await response.json().catch(() => ({}));
    if (response.ok && data.accepted !== false) localStorage.setItem(LAST_REPORT, String(Date.now()));
    return data;
  } catch (error) {
    captureError(error);
    return { accepted: false, reason: 'bridge_unavailable' };
  }
}

export function scheduleDeviceHealth() {
  const run = () => reportDeviceHealth(false);
  if (document.readyState === 'complete') setTimeout(run, 3500);
  else window.addEventListener('load', () => setTimeout(run, 3500), { once: true });
  window.setInterval(run, REPORT_WINDOW_MS);
}
