const BUS_KEY = 'ima-unified-learning-bus-v1';
const PROFILE_KEY = 'ima-unified-learning-profile-v1';
const MAX_EVENTS = 120;

function safeParse(value, fallback) {
  try { return JSON.parse(value); } catch { return fallback; }
}

function readEvents() {
  if (typeof localStorage === 'undefined') return [];
  return safeParse(localStorage.getItem(BUS_KEY) || '[]', []);
}

function writeEvents(events) {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(BUS_KEY, JSON.stringify(events.slice(-MAX_EVENTS)));
}

function normalizeSignal(signal = {}) {
  return {
    type: String(signal.type || 'observation'),
    source: String(signal.source || 'unknown'),
    at: new Date().toISOString(),
    outcome: signal.outcome ? String(signal.outcome) : undefined,
    tags: Array.isArray(signal.tags) ? signal.tags.map(String).slice(0, 12) : [],
    data: signal.data && typeof signal.data === 'object' ? signal.data : {},
  };
}

export function observeIma(signal) {
  const event = normalizeSignal(signal);
  const events = readEvents();
  events.push(event);
  writeEvents(events);
  return event;
}

export function getImaLearningState() {
  const events = readEvents();
  const profile = safeParse(
    typeof localStorage === 'undefined' ? '{}' : localStorage.getItem(PROFILE_KEY) || '{}',
    {}
  );
  const counts = {};
  for (const event of events) {
    counts[event.type] = (counts[event.type] || 0) + 1;
  }
  return { version: 1, eventCount: events.length, counts, profile };
}

export function deriveImaAdaptations() {
  const { counts, profile } = getImaLearningState();
  const adaptations = [];
  if ((counts.feedback || 0) > 0) adaptations.push('feedback-informed');
  if ((counts.chat_completed || 0) > 0) adaptations.push('conversation-informed');
  if ((counts.runtime_checked || 0) > 0) adaptations.push('runtime-aware');
  if ((counts.accessibility_changed || 0) > 0) adaptations.push('accessibility-aware');
  if ((counts.memory_changed || 0) > 0) adaptations.push('memory-aware');
  return { adaptations, profile };
}

export function recordImaPreference(key, value) {
  if (typeof localStorage === 'undefined' || !key) return;
  const current = safeParse(localStorage.getItem(PROFILE_KEY) || '{}', {});
  current[String(key)] = String(value);
  localStorage.setItem(PROFILE_KEY, JSON.stringify(current));
  observeIma({ type: 'preference_changed', source: 'personalization', data: { key: String(key), value: String(value) } });
}

export function clearImaLearningState() {
  if (typeof localStorage === 'undefined') return;
  localStorage.removeItem(BUS_KEY);
  localStorage.removeItem(PROFILE_KEY);
}
