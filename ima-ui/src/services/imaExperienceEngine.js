// IMA EXPERIENCE ENGINE — universal product lessons translated into humane product behavior.
// Mission + experience are first-class modes. This is not an addiction/retention engine.
// The person owns the goal, experience, progress, memory and decision to continue.

const KEY = 'ima-experience-missions-v2';
const EXPERIENCE_TYPES = ['discover','create','play','story','music','world','collaborate','reflect','learn','explore'];
const MAX = 50;

function read() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; }
}
function write(items) {
  try { localStorage.setItem(KEY, JSON.stringify(items.slice(-MAX))); } catch { /* storage unavailable */ }
}

function classify(text='') {
  const v=String(text).toLowerCase();
  if (/ללמוד|להבין|research|learn|explain/.test(v)) return 'learn';
  if (/לכתוב|שיר|ליצור|build|create|write|design/.test(v)) return 'create';
  if (/בעיה|לתקן|לפתור|fix|solve|problem/.test(v)) return 'solve';
  if (/להחליט|שיחה|מחשבה|think|decision|conversation/.test(v)) return 'think';
  return 'explore';
}

export function beginImaMission(goal='', options={}) {
  const mission = {
    id: 'mission-' + Date.now() + '-' + Math.random().toString(36).slice(2,8),
    mode: options.mode || 'mission',
    experienceType: options.experienceType || null,
    type: classify(goal),
    goal: String(goal).slice(0, 500),
    startedAt: new Date().toISOString(),
    status: 'active',
    steps: ['goal_understood', 'first_value', 'optional_next_step'],
    completedSteps: []
  };
  const items=read(); items.push(mission); write(items);
  try { window.dispatchEvent(new CustomEvent('ima:mission-started',{detail:mission})); } catch { /* event bridge unavailable */ }
  return mission;
}

export function completeImaMission(missionId, outcome={}) {
  const items=read();
  const mission=items.find(x=>x.id===missionId);
  if (!mission) return null;
  mission.status='value_delivered';
  mission.completedSteps=['goal_understood','first_value'];
  mission.completedAt=new Date().toISOString();
  mission.outcome={useful:Boolean(outcome.useful), responseLength:Number(outcome.responseLength||0)};
  write(items);
  try { window.dispatchEvent(new CustomEvent('ima:mission-completed',{detail:mission})); } catch { /* event bridge unavailable */ }
  return mission;
}

export function beginImaExperience(intent='', experienceType='explore') {
  const type = EXPERIENCE_TYPES.includes(experienceType) ? experienceType : 'explore';
  return beginImaMission(intent, { mode:'experience', experienceType:type });
}

export function getImaMissions() { return read(); }
export function getImaExperienceTypes() { return [...EXPERIENCE_TYPES]; }
