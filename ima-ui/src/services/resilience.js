const STORAGE_KEY = 'ima-resilience-tasks-v1';

export const RESILIENCE_PHASES = [
  { id:'NORMAL', he:'שגרה', en:'Normal' },
  { id:'STRESS', he:'משבר אישי/משפחתי', en:'Personal or family stress' },
  { id:'CRISIS', he:'משבר אזורי', en:'Regional crisis' },
  { id:'GLOBAL_EMERGENCY', he:'מצב חירום רחב', en:'Global emergency' }
];

export const RESILIENCE_CATEGORIES = [
  { id:'emergency', he:'סכנה או חירום', en:'Emergency or immediate danger' },
  { id:'food', he:'מזון ומצרכים בסיסיים', en:'Food and essentials' },
  { id:'housing', he:'דיור ומחסה', en:'Housing and shelter' },
  { id:'income', he:'הכנסה, זכויות וקצבאות', en:'Income, benefits and rights' },
  { id:'health', he:'בריאות וטיפול', en:'Health and care' },
  { id:'work_transition', he:'עבודה ומעבר מקצועי', en:'Work and transition' },
  { id:'documents', he:'מסמכים ושירותים ממשלתיים', en:'Documents and government services' },
  { id:'accessibility', he:'נגישות ועזרה תפקודית', en:'Accessibility and functional support' },
  { id:'community', he:'קהילה ועזרה הדדית', en:'Community and mutual aid' },
  { id:'utilities', he:'חשמל, מים ותקשורת', en:'Utilities and connectivity' },
  { id:'preparedness', he:'היערכות לאסון', en:'Disaster preparedness' }
];

const ISRAEL_OFFICIAL = {
  emergency:'https://www.gov.il/',
  income:'https://www.btl.gov.il/benefits/Unemployment/Pages/submit.aspx',
  documents:'https://www.gov.il/',
  preparedness:'https://www.oref.org.il/',
  utilities:'https://www.gov.il/'
};

export function getResiliencePlan({ phase, need }) {
  const emergency = need === 'emergency';
  const common = emergency ? [
    {id:'call-100',priority:'01',heTitle:'משטרה — 100',enTitle:'Police — 100',heText:'סכנה מיידית או אירוע ביטחוני/פלילי: פנה ישירות למוקד החירום.',enText:'Immediate danger or security/criminal emergency: contact emergency services directly.',url:'tel:100'},
    {id:'call-101',priority:'02',heTitle:'מד״א — 101',enTitle:'Ambulance — 101',heText:'אירוע רפואי דחוף: פנה ישירות למד״א.',enText:'Urgent medical emergency: contact the ambulance service directly.',url:'tel:101'},
    {id:'call-102',priority:'03',heTitle:'כבאות והצלה — 102',enTitle:'Fire & Rescue — 102',heText:'שריפה או חילוץ: פנה ישירות לכבאות והצלה.',enText:'Fire or rescue emergency: contact Fire & Rescue directly.',url:'tel:102'},
    {id:'call-104',priority:'04',heTitle:'פיקוד העורף — 104',enTitle:'Home Front Command — 104',heText:'הנחיות והתרעות בעורף בזמן אירוע חירום.',enText:'Official Home Front guidance and information during an emergency.',url:'tel:104'},
    {id:'official-emergency',priority:'05',heTitle:'מקור רשמי',enTitle:'Official emergency information',heText:'לבדיקת הנחיות רשמיות ועדכונים, פתח את המקור הממשלתי.',enText:'Open the official government source for verified guidance and updates.',url:ISRAEL_OFFICIAL.emergency}
  ] : [
    {id:'need-define',priority:'01',heTitle:'להגדיר את הצורך',enTitle:'Define the need',heText:'בחר את הבעיה המרכזית. אל תנסה לפתור הכול בבת אחת.',enText:'Choose the primary problem. Do not try to solve everything at once.'},
    {id:'official-route',priority:'02',heTitle:'לפתוח את המסלול הרשמי',enTitle:'Open the official route',heText:'העדף רשות, שירות ציבורי או ספק מאומת לפני מקור לא מוכר.',enText:'Prefer an official authority, public service or verified provider before an unknown source.'},
    {id:'documents',priority:'03',heTitle:'לאסוף מסמכים',enTitle:'Collect evidence and documents',heText:'רשום מה חסר, מה כבר קיים ומה צריך להגיש.',enText:'List what is missing, what exists and what must be submitted.'},
    {id:'backup',priority:'04',heTitle:'לבנות חלופה',enTitle:'Create a fallback',heText:'אם המסלול הראשון חסום, בחר מסלול חלופי ולא נשארים בלי פעולה.',enText:'If the first route is blocked, choose a fallback instead of stopping.'}
  ];
  const extras = {
    income:[{id:'btl-unemployment',priority:'05',heTitle:'ביטוח לאומי — אבטלה',enTitle:'National Insurance — unemployment',heText:'בדוק זכאות והגשה מקוונת לפי התנאים העדכניים.',enText:'Check current eligibility and online filing requirements.',url:ISRAEL_OFFICIAL.income}],
    preparedness:[{id:'oref',priority:'05',heTitle:'פיקוד העורף — היערכות',enTitle:'Home Front Command — preparedness',heText:'בדוק הנחיות רשמיות והכן תוכנית ביתית מראש.',enText:'Check official guidance and prepare a household plan.',url:ISRAEL_OFFICIAL.preparedness}],
    documents:[{id:'gov',priority:'05',heTitle:'שירותי ממשלה',enTitle:'Government services',heText:'פתח את שער השירותים הממשלתי וחפש את השירות המדויק.',enText:'Open the government service portal and find the exact service.',url:ISRAEL_OFFICIAL.documents}]
  };
  const phaseTask = {
    STRESS:{id:'trusted-person',priority:'05',heTitle:'לשתף אדם נוסף',enTitle:'Bring in a trusted person',heText:'במשבר אישי, בחר אדם אחד שיודע מה קורה ויכול לעזור בפועל.',enText:'In a personal crisis, involve one trusted person who can help practically.'},
    CRISIS:{id:'local-coordination',priority:'05',heTitle:'לבדוק מוקד מקומי',enTitle:'Check local coordination',heText:'חפש מוקד רשות מקומית/שירות אזורי והצלב מידע לפני פעולה.',enText:'Check local authority coordination and cross-check information before acting.'},
    GLOBAL_EMERGENCY:{id:'redundancy',priority:'05',heTitle:'לבנות יתירות',enTitle:'Build redundancy',heText:'שמור לפחות שני ערוצי מידע ושני מסלולי סיוע אפשריים.',enText:'Maintain at least two information channels and two possible aid routes.'}
  };
  return [...common, ...(extras[need] || []), ...(phaseTask[phase] ? [phaseTask[phase]] : [])].slice(0,7);
}

export function loadResiliencePlan(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
}
export function saveResiliencePlan(tasks){
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks.slice(-30))); return true; } catch { return false; }
}
