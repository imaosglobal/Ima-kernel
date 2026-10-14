const STORAGE_KEY = 'ima-analytics-anonymous-id';
const API_URL = (import.meta.env.VITE_IMA_ANALYTICS_URL || '').replace(/\/$/, '');
const GA4_ID = import.meta.env.VITE_GA4_MEASUREMENT_ID || '';

function anonymousId() {
  try {
    let id = localStorage.getItem(STORAGE_KEY);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(STORAGE_KEY, id);
    }
    return id;
  } catch {
    return 'ephemeral';
  }
}

function loadGA4() {
  if (!GA4_ID || document.querySelector('script[data-ima-ga4]')) return;
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA4_ID)}`;
  script.dataset.imaGa4 = '1';
  document.head.appendChild(script);
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA4_ID, { send_page_view: false });
}

export function trackImaEvent(name, properties = {}) {
  const payload = {
    name,
    anonymous_id: anonymousId(),
    occurred_at: new Date().toISOString(),
    path: window.location.pathname,
    language: document.documentElement.lang || navigator.language || 'unknown',
    properties,
  };

  if (API_URL) {
    try {
      navigator.sendBeacon?.(
        `${API_URL}/events`,
        new Blob([JSON.stringify(payload)], { type: 'application/json' })
      );
    } catch (error) { void error; }
  }

  if (GA4_ID) {
    loadGA4();
    window.gtag?.('event', name, { ...properties, ima_anonymous_id: payload.anonymous_id });
  }
}

export function initializeImaAnalytics() {
  trackImaEvent('ima_visit');
}
