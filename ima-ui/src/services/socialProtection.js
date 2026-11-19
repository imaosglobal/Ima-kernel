// SOCIAL-PROTECTION-001: country-aware social-insurance and benefits routing.
// No eligibility is inferred from country alone; official sources must be verified before action.

const STORAGE_KEY = 'ima-social-protection-context-v1';

export const SOCIAL_PROTECTION_DOMAINS = [
  'unemployment','disability','old_age','survivors','sickness','maternity','parental',
  'children_family','work_injury','contributions','housing','food','minimum_income','care',
  'employment_services','crisis_assistance'
];

const COUNTRY_SOURCES = {
  IL:{name:'Israel',languages:['he'],portal:'https://www.gov.il/',insurance:'https://www.btl.gov.il/'},
  US:{name:'United States',languages:['en'],portal:'https://www.usa.gov/benefits',insurance:'https://www.ssa.gov/'},
  CA:{name:'Canada',languages:['en','fr'],portal:'https://www.canada.ca/en/services/benefits.html',insurance:'https://www.canada.ca/en/services/benefits/publicpensions.html'},
  GB:{name:'United Kingdom',languages:['en'],portal:'https://www.gov.uk/browse/benefits',insurance:'https://www.gov.uk/browse/benefits'},
  IE:{name:'Ireland',languages:['en','ga'],portal:'https://www.gov.ie/en/category/social-welfare/',insurance:'https://www.gov.ie/en/category/social-welfare/'},
  AU:{name:'Australia',languages:['en'],portal:'https://www.servicesaustralia.gov.au/',insurance:'https://www.servicesaustralia.gov.au/'},
  NZ:{name:'New Zealand',languages:['en','mi'],portal:'https://www.workandincome.govt.nz/',insurance:'https://www.workandincome.govt.nz/'},
  DE:{name:'Germany',languages:['de'],portal:'https://www.arbeitsagentur.de/',insurance:'https://www.deutsche-rentenversicherung.de/'},
  FR:{name:'France',languages:['fr'],portal:'https://www.service-public.fr/',insurance:'https://www.ameli.fr/'},
  ES:{name:'Spain',languages:['es'],portal:'https://administracion.gob.es/',insurance:'https://www.seg-social.es/'},
  PT:{name:'Portugal',languages:['pt'],portal:'https://www2.gov.pt/',insurance:'https://www.seg-social.pt/'},
  IT:{name:'Italy',languages:['it'],portal:'https://www.inps.it/',insurance:'https://www.inps.it/'},
  NL:{name:'Netherlands',languages:['nl'],portal:'https://www.government.nl/topics/social-security',insurance:'https://www.uwv.nl/'},
  BE:{name:'Belgium',languages:['nl','fr','de'],portal:'https://www.belgium.be/en/work/social_security',insurance:'https://www.socialsecurity.be/'},
  CH:{name:'Switzerland',languages:['de','fr','it'],portal:'https://www.ch.ch/en/work/social-insurances/',insurance:'https://www.ahv-iv.ch/'},
  AT:{name:'Austria',languages:['de'],portal:'https://www.oesterreich.gv.at/en/themen/soziales/soziale_sicherheit.html',insurance:'https://www.sozialversicherung.at/'},
  SE:{name:'Sweden',languages:['sv'],portal:'https://www.forsakringskassan.se/'},
  NO:{name:'Norway',languages:['no'],portal:'https://www.nav.no/'},
  DK:{name:'Denmark',languages:['da'],portal:'https://lifeindenmark.borger.dk/'},
  FI:{name:'Finland',languages:['fi','sv'],portal:'https://www.kela.fi/'},
  PL:{name:'Poland',languages:['pl'],portal:'https://www.gov.pl/web/family',insurance:'https://www.zus.pl/'},
  CZ:{name:'Czechia',languages:['cs'],portal:'https://www.mpsv.cz/'},
  SK:{name:'Slovakia',languages:['sk'],portal:'https://www.slovensko.sk/'},
  HU:{name:'Hungary',languages:['hu'],portal:'https://magyarorszag.hu/'},
  RO:{name:'Romania',languages:['ro'],portal:'https://www.mmuncii.ro/'},
  BG:{name:'Bulgaria',languages:['bg'],portal:'https://asp.government.bg/'},
  GR:{name:'Greece',languages:['el'],portal:'https://www.gov.gr/'},
  HR:{name:'Croatia',languages:['hr'],portal:'https://gov.hr/'},
  SI:{name:'Slovenia',languages:['sl'],portal:'https://www.gov.si/'},
  EE:{name:'Estonia',languages:['et'],portal:'https://www.eesti.ee/'},
  LV:{name:'Latvia',languages:['lv'],portal:'https://www.latvija.gov.lv/'},
  LT:{name:'Lithuania',languages:['lt'],portal:'https://www.sodra.lt/'},
  IS:{name:'Iceland',languages:['is'],portal:'https://island.is/'},
  LU:{name:'Luxembourg',languages:['lb','fr','de'],portal:'https://guichet.public.lu/'},
  MT:{name:'Malta',languages:['mt','en'],portal:'https://socialsecurity.gov.mt/'},
  CY:{name:'Cyprus',languages:['el','tr'],portal:'https://www.gov.cy/'},
  JP:{name:'Japan',languages:['ja'],portal:'https://www.nenkin.go.jp/'},
  KR:{name:'South Korea',languages:['ko'],portal:'https://www.gov.kr/'},
  CN:{name:'China',languages:['zh'],portal:'https://www.gov.cn/'},
  TW:{name:'Taiwan',languages:['zh'],portal:'https://www.gov.tw/'},
  IN:{name:'India',languages:['hi','en'],portal:'https://www.india.gov.in/'},
  SG:{name:'Singapore',languages:['en','ms','zh','ta'],portal:'https://www.gov.sg/'},
  MY:{name:'Malaysia',languages:['ms'],portal:'https://www.malaysia.gov.my/'},
  PH:{name:'Philippines',languages:['en','fil'],portal:'https://www.gov.ph/'},
  ID:{name:'Indonesia',languages:['id'],portal:'https://www.indonesia.go.id/'},
  TH:{name:'Thailand',languages:['th'],portal:'https://www.thaigov.go.th/'},
  VN:{name:'Vietnam',languages:['vi'],portal:'https://xaydungchinhsach.chinhphu.vn/'},
  BR:{name:'Brazil',languages:['pt'],portal:'https://www.gov.br/'},
  MX:{name:'Mexico',languages:['es'],portal:'https://www.gob.mx/'},
  AR:{name:'Argentina',languages:['es'],portal:'https://www.argentina.gob.ar/'},
  CL:{name:'Chile',languages:['es'],portal:'https://www.chileatiende.gob.cl/'},
  CO:{name:'Colombia',languages:['es'],portal:'https://www.gov.co/'},
  PE:{name:'Peru',languages:['es'],portal:'https://www.gob.pe/'},
  ZA:{name:'South Africa',languages:['en'],portal:'https://www.gov.za/'},
  NG:{name:'Nigeria',languages:['en'],portal:'https://www.gov.ng/'},
  KE:{name:'Kenya',languages:['en','sw'],portal:'https://www.gov.ke/'},
  GH:{name:'Ghana',languages:['en'],portal:'https://www.gov.gh/'},
  MA:{name:'Morocco',languages:['ar','fr'],portal:'https://www.maroc.ma/'},
  EG:{name:'Egypt',languages:['ar'],portal:'https://www.gov.eg/'},
  AE:{name:'United Arab Emirates',languages:['ar','en'],portal:'https://u.ae/'},
  SA:{name:'Saudi Arabia',languages:['ar'],portal:'https://www.my.gov.sa/'},
  JO:{name:'Jordan',languages:['ar'],portal:'https://portal.jordan.gov.jo/'},
  TR:{name:'Türkiye',languages:['tr'],portal:'https://www.turkiye.gov.tr/'},
  UA:{name:'Ukraine',languages:['uk'],portal:'https://diia.gov.ua/'},
  RU:{name:'Russia',languages:['ru'],portal:'https://www.gosuslugi.ru/'}
};

const LANGUAGE_TO_COUNTRY = {
  he:'IL', ar:'EG', fa:'IR', ur:'PK', hi:'IN', bn:'BD', ja:'JP', ko:'KR', zh:'CN',
  th:'TH', vi:'VN', id:'ID', ms:'MY', tr:'TR', uk:'UA', ru:'RU', pl:'PL', cs:'CZ',
  sk:'SK', hu:'HU', ro:'RO', bg:'BG', el:'GR', hr:'HR', sl:'SI', et:'EE', lv:'LV',
  lt:'LT', is:'IS', sv:'SE', no:'NO', da:'DK', fi:'FI', nl:'NL', de:'DE', fr:'FR',
  es:'ES', pt:'PT', it:'IT', en:'US'
};

const TIMEZONE_COUNTRIES = {
  'Asia/Jerusalem':'IL','Europe/London':'GB','Europe/Berlin':'DE','Europe/Paris':'FR',
  'Europe/Rome':'IT','Europe/Madrid':'ES','Europe/Amsterdam':'NL','Europe/Brussels':'BE',
  'Europe/Zurich':'CH','Europe/Vienna':'AT','Europe/Stockholm':'SE','Europe/Oslo':'NO',
  'Europe/Copenhagen':'DK','Europe/Helsinki':'FI','Europe/Warsaw':'PL','Europe/Prague':'CZ',
  'Europe/Budapest':'HU','Europe/Bucharest':'RO','Europe/Sofia':'BG','Europe/Athens':'GR',
  'Europe/Zagreb':'HR','Europe/Ljubljana':'SI','Europe/Tallinn':'EE','Europe/Riga':'LV',
  'Europe/Vilnius':'LT','Europe/Reykjavik':'IS','Europe/Luxembourg':'LU','Europe/Malta':'MT',
  'Asia/Tokyo':'JP','Asia/Seoul':'KR','Asia/Shanghai':'CN','Asia/Taipei':'TW',
  'Asia/Kolkata':'IN','Asia/Singapore':'SG','Asia/Kuala_Lumpur':'MY','Asia/Manila':'PH',
  'Asia/Jakarta':'ID','Asia/Bangkok':'TH','Asia/Ho_Chi_Minh':'VN','Asia/Istanbul':'TR',
  'America/Toronto':'CA','America/Vancouver':'CA','America/New_York':'US','America/Chicago':'US',
  'America/Denver':'US','America/Los_Angeles':'US','America/Mexico_City':'MX',
  'America/Sao_Paulo':'BR','America/Argentina/Buenos_Aires':'AR','America/Santiago':'CL',
  'America/Bogota':'CO','America/Lima':'PE','Africa/Johannesburg':'ZA','Africa/Lagos':'NG',
  'Africa/Nairobi':'KE','Africa/Accra':'GH','Africa/Cairo':'EG','Africa/Casablanca':'MA',
  'Asia/Dubai':'AE','Asia/Riyadh':'SA','Asia/Amman':'JO','Europe/Kyiv':'UA','Europe/Moscow':'RU',
  'Pacific/Auckland':'NZ','Australia/Sydney':'AU'
};

function normalizeLanguage(value){
  return String(value || '').toLowerCase().split('-')[0];
}

export function detectImaLocale({ user, language } = {}){
  const browserLocale = String(language || navigator.language || 'en-US');
  const locale = browserLocale.replace('_','-');
  let region = '';
  try { region = new Intl.Locale(locale).region || ''; } catch {}
  const lang = normalizeLanguage(locale);
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
  const country = /^[A-Z]{2}$/.test(region) ? region : (TIMEZONE_COUNTRIES[timezone] || LANGUAGE_TO_COUNTRY[lang] || 'US');
  const preferredLanguage = lang || normalizeLanguage(user?.language) || COUNTRY_SOURCES[country]?.languages?.[0] || 'en';
  return { country, language: preferredLanguage, timezone, source: region ? 'device-locale' : (TIMEZONE_COUNTRIES[timezone] ? 'device-timezone' : 'language-fallback') };
}

export function getSocialProtectionContext({ user, language } = {}){
  const detected = detectImaLocale({ user, language });
  const source = COUNTRY_SOURCES[detected.country] || {name:null,languages:[detected.language],portal:null,insurance:null};
  let localizedCountryName = source.name;
  try { localizedCountryName = new Intl.DisplayNames([detected.language], { type:'region' }).of(detected.country) || source.name || detected.country; } catch {}
  const preferred = source.languages.includes(detected.language) ? detected.language : (source.languages[0] || detected.language);
  return { ...detected, countryName:localizedCountryName || detected.country, languages:source.languages, portal:source.portal, insurance:source.insurance, preferredLanguage:preferred, sourceConfigured:Boolean(source.portal || source.insurance), domains:SOCIAL_PROTECTION_DOMAINS };
}

export function buildSocialProtectionTasks(context){
  const label = context.language === 'he' ? 'ביטוח לאומי וזכויות' : context.language === 'de' ? 'Sozialversicherung und Leistungen' : context.language === 'fr' ? 'Protection sociale et prestations' : context.language === 'es' ? 'Seguridad social y prestaciones' : context.language === 'pt' ? 'Segurança social e benefícios' : context.language === 'ar' ? 'الضمان الاجتماعي والمزايا' : context.language === 'ja' ? '社会保障・給付' : context.language === 'zh' ? '社会保障与福利' : 'Social insurance and benefits';
  const detail = context.portal
    ? (context.language === 'he' ? 'מקור רשמי למדינה שזוהתה מהמכשיר. בדוק זכאות, מסמכים והגשה לפני פעולה.' : 'Official source for the country detected from this device. Check eligibility, documents and filing requirements before acting.')
    : (context.language === 'he' ? 'לא נמצא מקור רשמי מוכר אוטומטית. אמא לא תמציא כתובת; יש לאמת את הרשות המקומית.' : 'No verified official source is configured for this country. IMA will not invent an address; the responsible authority must be verified.');
  return [
    {id:'social-protection-country',priority:'01',title:label,heTitle:label,enTitle:'Social insurance and benefits',text:detail,heText:detail,enText:detail,url:context.portal},
    {id:'social-protection-unemployment',priority:'02',title:'Unemployment',heTitle:'אבטלה',enTitle:'Unemployment',text:'',heText:'בדוק דמי אבטלה, שירותי תעסוקה, תנאי זכאות ומועד הגשה.',enText:'Check unemployment benefits, employment services, eligibility and filing deadlines.'},
    {id:'social-protection-disability',priority:'03',title:'Disability',heTitle:'נכות ואובדן כושר',enTitle:'Disability and work capacity',text:'',heText:'בדוק קצבאות/ביטוח נכות, התאמות ושירותי שיקום לפי המדינה.',enText:'Check disability, work-capacity, accommodation and rehabilitation programs available in the country.'},
    {id:'social-protection-family',priority:'04',title:'Family',heTitle:'ילדים ומשפחה',enTitle:'Children and family',text:'',heText:'בדוק קצבאות ילדים, לידה, הורות וטיפול בבני משפחה.',enText:'Check child, maternity, parental and family-care benefits.'},
    {id:'social-protection-age',priority:'05',title:'Pension',heTitle:'זקנה ופנסיה',enTitle:'Old age and pensions',text:'',heText:'בדוק זכויות זקנה, פנסיה, שאירים והשלמת הכנסה לפי המערכת המקומית.',enText:'Check old-age, pension, survivor and minimum-income programs.'},
    {id:'social-protection-injury',priority:'06',title:'Work injury',heTitle:'פגיעה בעבודה',enTitle:'Work injury',text:'',heText:'בדוק מסלול דיווח, טיפול ופיצוי במקרה של פגיעה או מחלת עבודה.',enText:'Check reporting, care and compensation routes for work injury or occupational illness.'},
    {id:'social-protection-crisis',priority:'07',title:'Crisis support',heTitle:'סיוע חירום',enTitle:'Crisis assistance',text:'',heText:'אם ההכנסה או הדיור נפגעו, בדוק גם סיוע מזון, דיור, שירותים מקומיים ותמיכה זמנית.',enText:'If income or housing is affected, also check food, housing, local services and temporary assistance.'}
  ];
}

export function saveSocialProtectionContext(context){
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify({...context, savedAt:new Date().toISOString()})); return true; } catch { return false; }
}

export function loadSocialProtectionContext(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch { return null; }
}
