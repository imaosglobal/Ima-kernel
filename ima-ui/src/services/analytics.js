const STORAGE_KEY = 'ima-analytics-anonymous-id';
const API_URL = (import.meta.env.VITE_IMA_ANALYTICS_URL || 'https://ima-915m.onrender.com/ima-api/analytics').replace(/\/$/, '');
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
      const token = localStorage.getItem('ima-public-session-token') || '';
      fetch(API_URL, {method:'POST',keepalive:true,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},body:JSON.stringify({event:name.replace(/^ima_/,'').slice(0,64),properties:{...properties,language:payload.language,timezone:Intl.DateTimeFormat().resolvedOptions().timeZone||'unknown',locale:navigator.language||'unknown',path:payload.path}})}).catch(()=>{});
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
