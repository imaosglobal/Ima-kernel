// MARKET-ENTRY-001: canonical acquisition -> activation -> retention -> referral measurement.
// This layer never claims users, revenue, eligibility or conversion unless measured by an actual source.

export const MARKET_USE_CASES = [
  { id:'think', heLabel:'לחשוב על משהו שמעסיק אותי', enLabel:'Think through something on my mind', heText:'לסדר מחשבות, החלטה או שיחה קשה.', enText:'Untangle thoughts, a decision or a difficult conversation.' },
  { id:'learn', heLabel:'ללמוד ולהבין', enLabel:'Learn and understand', heText:'להסביר מושג, לחקור נושא ולבדוק מקורות.', enText:'Explain a concept, research a topic and check sources.' },
  { id:'create', heLabel:'ליצור משהו', enLabel:'Create something', heText:'לכתוב, לתכנן, לשיר, לבנות או להפוך רעיון לדבר ממשי.', enText:'Write, plan, compose, build or turn an idea into something real.' },
  { id:'solve', heLabel:'לפתור צורך אמיתי', enLabel:'Solve a real need', heText:'להפוך בעיה לצעדים מעשיים ולנתב לגורם מתאים כשצריך.', enText:'Turn a problem into practical steps and route to the right service when needed.' }
];

export function getMarketCampaign(search='') {
  try {
    const p = new URLSearchParams(search);
    return p.get('campaign') || p.get('utm_campaign') || p.get('ref') || 'organic';
  } catch { return 'organic'; }
}

export function buildShareUrl(base, {use='think', ref='share', campaign='share'}={}) {
  const url = new URL(base, window.location.origin);
  url.searchParams.set('use', use);
  url.searchParams.set('ref', ref);
  url.searchParams.set('campaign', campaign);
  return url.toString();
}

export function recordMarketEvent(event, data={}) {
  const payload = { event, at:new Date().toISOString(), ...data };
  try {
    const key = 'ima-market-events-v1';
    const previous = JSON.parse(localStorage.getItem(key) || '[]');
    previous.push(payload);
    localStorage.setItem(key, JSON.stringify(previous.slice(-200)));
  } catch { /* local storage unavailable */ }
  try { window.dispatchEvent(new CustomEvent('ima:market-event', { detail: payload })); } catch { /* intentionally ignored */ }
  return payload;
}
