import React, { useEffect, useMemo, useState } from 'react';
import {
  askIma,
  archiveChatLearningSignal,
  getAuthConfig,
  signInWithGoogleCredential,
  getStoredGoogleUser,
  signOutIma,
  getImaRuntime,
  submitFeedback
} from './services/imaChat';
import { initializeImaAnalytics, trackImaEvent } from './services/analytics';

const BASE = '/Ima-kernel/';
const SUPPORT_URL = BASE + 'support.html';
const PRIVACY_URL = BASE + 'privacy.html';
const GOOGLE_CAMPAIGN_URL = BASE + '?campaignId=24409551537&utm_source=ima_logo';
const YOUTUBE_URL = 'https://www.youtube.com/@imaglobal-d4g';
const CLEAN_LOGO_URL = 'https://dynamic.heygen.ai/image/f057cd08143342f2994f85d847572fa8/original.png';
const copy = {
  he: {
    nav: ['לדבר', 'איך זה עובד', 'הוכחות', 'קהילה'],
    heroKicker: 'IMA — אמא · בינה אנושית',
    heroTitle: 'אמא כאן\nכדי להבין איתך.',
    heroText: 'לא עוד תפריט של יכולות. שיחה אמיתית, הקשר, בדיקה ולמידה — עם האדם במרכז.',
    ask: 'לדבר עם אמא',
    proof: 'לראות מה באמת עובד',
    prompt: 'מה תרצה לעשות עם אמא?',
    modes: ['לחשוב', 'ללמוד', 'ליצור', 'לפתור'],
    modeText: ['להבין רעיון, החלטה או מצב', 'לחקור נושא ולגלות מה חסר', 'לכתוב, לתכנן או ליצור', 'להפוך צורך לצעדים מעשיים'],
    howKicker: 'איך אמא עובדת',
    howTitle: 'פחות הבטחות. יותר בדיקה.',
    cards: [
      ['01', 'הקשבה', 'מתחילים במה שאתה באמת צריך — לא בתפריט של יכולות.'],
      ['02', 'הקשר', 'שפה, נגישות, זיכרון והעדפות יכולים להתאים אליך; הסוכנות נשארת שלך.'],
      ['03', 'אימות', 'אמא מפרידה בין מה שנבדק, מה שנבנה ומה שעדיין לא הוכח.'],
      ['04', 'למידה', 'אפשר לתקן את אמא. תרומה נכנסת למסלול אימות, לא הופכת אוטומטית לאמת.']
    ],
    proofKicker: 'חלון הוכחה',
    proofTitle: 'מה אמא יכולה עכשיו?',
    proofText: 'תיעוד אינו הוכחה. כאן מוצגים סימנים שאפשר לבדוק בזמן ריצה.',
    online: 'Runtime זמין',
    offline: 'Runtime לא אומת כרגע',
    communityKicker: 'קהילה גלובלית',
    communityTitle: 'אמא נבנית עם העולם, לא מעליו.',
    communityText: 'חוקרים, יוצרים, מפתחים, משפחות וארגונים יכולים לשאול, ללמד, לבדוק ולבנות.',
    github: 'לפתוח את GitHub',
    feedback: 'לתת משוב',
    feedbackPlaceholder: 'מה יעזור לך לחזור לאמא?',
    send: 'שליחה',
    signIn: 'כניסה אישית עם Google',
    signed: 'מחובר',
    logout: 'יציאה',
    personal: 'מרחב אישי',
    personalText: 'לאחר הכניסה אמא יכולה לשמור רציפות בהתאם להרשאות שלך.',
    install: 'התקנת אמא',
    chatOnly: 'צ׳ט בלבד',
    browser: 'דפדפן חי',
    openChat: 'פתיחת צ׳ט',
    closeChat: 'סגירת צ׳ט',
    write: 'כתוב לאמא…',
    sendChat: 'שליחה',
    saved: 'המשוב נשמר וקיבל קבלה.',
    saveFailed: 'לא הצלחתי לאמת את השמירה.',
    footer: 'IMA — אמא, by Ori Cohen · Human-centered intelligence'
  },
  en: {
    nav: ['Talk', 'How it works', 'Proof', 'Community'],
    heroKicker: 'IMA — human-centered intelligence',
    heroTitle: 'IMA is here\nto understand with you.',
    heroText: 'Not another menu of capabilities. A real conversation, context, verification and learning — with the person at the center.',
    ask: 'Talk to IMA',
    proof: 'See what is real',
    prompt: 'What would you like to do with IMA?',
    modes: ['Think', 'Learn', 'Create', 'Solve'],
    modeText: ['Explore an idea, decision or situation', 'Research a topic and find what is missing', 'Write, plan or create', 'Turn a need into practical steps'],
    howKicker: 'How IMA works',
    howTitle: 'Fewer promises. More verification.',
    cards: [
      ['01', 'Listen', 'Start with what you actually need — not a menu of capabilities.'],
      ['02', 'Context', 'Language, accessibility, memory and preferences can adapt; agency remains yours.'],
      ['03', 'Verify', 'IMA separates what is tested, implemented and still unproven.'],
      ['04', 'Learn', 'You can correct IMA. Contributions enter validation rather than becoming truth automatically.']
    ],
    proofKicker: 'Proof window',
    proofTitle: 'What can IMA do now?',
    proofText: 'Documentation is not proof. This surface shows signals that can be checked at runtime.',
    online: 'Runtime available',
    offline: 'Runtime not verified now',
    communityKicker: 'Global community',
    communityTitle: 'IMA is built with the world, not above it.',
    communityText: 'Researchers, creators, developers, families and organizations can question, teach, test and build.',
    github: 'Open GitHub',
    feedback: 'Give feedback',
    feedbackPlaceholder: 'What would make you come back to IMA?',
    send: 'Send',
    signIn: 'Personal sign-in with Google',
    signed: 'Signed in',
    logout: 'Log out',
    personal: 'Personal space',
    personalText: 'After sign-in, IMA can preserve continuity according to your permissions.',
    install: 'Install IMA',
    chatOnly: 'Chat only',
    browser: 'Live browser',
    openChat: 'Open chat',
    closeChat: 'Close chat',
    write: 'Write to IMA…',
    sendChat: 'Send',
    saved: 'Feedback saved and receipt acknowledged.',
    saveFailed: 'Could not verify that the feedback was saved.',
    footer: 'IMA — אמא, by Ori Cohen · Human-centered intelligence'
  }
};

function MamaFigure({ compact = false }) {
  return <div className={'mama-figure' + (compact ? ' compact' : '')} aria-label="אמא">
    <div className="mama-halo" />
    <div className="mama-face"><span>א</span></div>
    <div className="mama-neck" />
    <div className="mama-shoulders" />
    <div className="mama-glow" />
  </div>;
}

function GoogleButton({ user, onUser, t }) {
  const [error, setError] = useState('');
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const config = await getAuthConfig();
        if (!config?.google?.enabled || !config.google.client_id) throw new Error('Google sign-in is not configured');
        for (let i = 0; i < 40 && !window.google?.accounts?.id && !cancelled; i++) await new Promise(r => setTimeout(r, 100));
        if (!window.google?.accounts?.id || cancelled) throw new Error('Google unavailable');
        const bytes = new Uint8Array(24);
        crypto.getRandomValues(bytes);
        const nonce = Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
        window.google.accounts.id.initialize({
          client_id: config.google.client_id,
          nonce,
          callback: async response => {
            try {
              const result = await signInWithGoogleCredential(response.credential, nonce);
              onUser(result.user || null);
              trackImaEvent('ima_public_google_login', { language: document.documentElement.lang });
            } catch { setError('Sign-in could not be completed'); }
          },
          auto_select: false,
          ux_mode: 'popup'
        });
        const node = document.getElementById('ima-google-button');
        if (node) {
          node.innerHTML = '';
          window.google.accounts.id.renderButton(node, {
            type: 'standard', theme: 'outline', size: 'large', text: 'signin_with', shape: 'pill', width: 240
          });
        }
        if (!cancelled) setReady(true);
      } catch (e) { if (!cancelled) setError(e?.message || 'Google sign-in unavailable'); }
    })();
    return () => { cancelled = true; };
  }, [onUser]);
  if (user) return <div className="ima-account"><span className="ima-account-dot">{String(user.name || 'א').slice(0,1)}</span><span>{user.name || user.email || t.signed}</span><button onClick={() => { signOutIma(); onUser(null); }}>{t.logout}</button></div>;
  return <div className="ima-google"><div id="ima-google-button" aria-label={t.signIn} />{!ready && !error && <span className="tiny-status">{t.signIn}</span>}{error && <span className="tiny-error">{error}</span>}</div>;
}

function ChatPanel({ t, lang, user, onClose, chatOnly = false }) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const send = async (text = message) => {
    const value = String(text || '').trim();
    if (!value || busy) return;
    setBusy(true); setMessage('');
    setMessages(prev => [...prev, { role: 'user', text: value }]);
    trackImaEvent('ima_first_use_attempt', { language: lang });
    try {
      const response = await askIma(value, { language: lang, interface: chatOnly ? 'chat-only' : 'public-redesign', authenticated: Boolean(user) });
      setMessages(prev => [...prev, { role: 'ima', text: response }]);
      trackImaEvent('ima_first_useful_answer_candidate', { language: lang });
      await archiveChatLearningSignal(value, response, { language: lang });
    } catch {
      setMessages(prev => [...prev, { role: 'ima', text: lang === 'he' ? 'אני עדיין לא מצליחה לענות דרך החיבור הציבורי הזה. זו תקלה למדוד ולתקן — לא להסתיר.' : 'I cannot answer through the public connection right now. This is a failure to measure and fix, not to hide.' }]);
      trackImaEvent('ima_public_chat_failed', { language: lang });
    } finally { setBusy(false); }
  };
  return <section className={'chat-panel' + (chatOnly ? ' chat-only-panel' : '')} id="chat">
    <div className="chat-panel-head">
      <div className="chat-identity"><MamaFigure compact /><div><b>אמא · IMA</b><small>{user ? t.personal : (lang === 'he' ? 'שיחה ציבורית' : 'Public conversation')}</small></div></div>
      {!chatOnly && <button className="chat-close" onClick={onClose} aria-label={t.closeChat}>×</button>}
    </div>
    <div className="chat-messages" aria-live="polite">
      {!messages.length && <div className="chat-empty">{lang === 'he' ? 'שאל שאלה אמיתית. אמא תענה דרך החיבור החי של IMA.' : 'Ask a real question. IMA will answer through the live IMA connection.'}</div>}
      {messages.map((m,i) => <div key={i} className={'chat-bubble '+m.role}>{m.text}</div>)}
      {busy && <div className="chat-bubble ima muted">IMA…</div>}
    </div>
    <div className="chat-composer"><input value={message} onChange={e=>setMessage(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder={t.write} aria-label={t.write}/><button onClick={()=>send()} disabled={busy || !message.trim()}>{t.sendChat}</button></div>
  </section>;
}

export default function App() {
  const [lang, setLang] = useState(() => localStorage.getItem('ima-site-language') || (navigator.language?.startsWith('he') ? 'he' : 'en'));
  const [user, setUser] = useState(() => getStoredGoogleUser());
  const [chatOpen, setChatOpen] = useState(() => new URLSearchParams(location.search).get('chat') === '1');
  const [runtime, setRuntime] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [feedbackStatus, setFeedbackStatus] = useState('');
  const [installEvent, setInstallEvent] = useState(null);
  const [notice, setNotice] = useState('');
  const t = copy[lang];
  const chatOnly = useMemo(() => new URLSearchParams(location.search).get('chat') === '1', []);

  useEffect(() => {
    localStorage.setItem('ima-site-language', lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'he' ? 'rtl' : 'ltr';
    document.title = lang === 'he' ? 'אמא — IMA | בינה אנושית' : 'IMA — Human-Centered Intelligence';
    initializeImaAnalytics();
    trackImaEvent('ima_public_redesign_view', { language: lang });
  }, [lang]);

  useEffect(() => {
    if (user) setChatOpen(true);
  }, [user]);

  useEffect(() => {
    getImaRuntime().then(setRuntime).catch(() => setRuntime(null));
    const handler = e => { e.preventDefault(); setInstallEvent(e); };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const install = async () => {
    if (!user) { setNotice(lang === 'he' ? 'כדי להתקין את אמא יש להיכנס תחילה עם Google.' : 'Sign in with Google before installing IMA.'); return; }
    if (!installEvent) { setNotice(lang === 'he' ? 'התקנה אינה זמינה כרגע בדפדפן הזה.' : 'Installation is not available in this browser right now.'); return; }
    installEvent.prompt();
    const choice = await installEvent.userChoice;
    trackImaEvent('ima_pwa_install_choice', { outcome: choice.outcome, language: lang });
    setInstallEvent(null);
  };

  const sendFeedback = async () => {
    if (!feedback.trim()) return;
    setFeedbackStatus('');
    try {
      await submitFeedback('improvement', feedback.trim(), { language: lang, source: 'public-redesign' });
      setFeedback('');
      setFeedbackStatus(t.saved);
      trackImaEvent('ima_feedback_submitted', { language: lang });
    } catch { setFeedbackStatus(t.saveFailed); }
  };

  if (chatOnly) return <div className="ima-chat-only"><MamaFigure /><h1>{lang === 'he' ? 'אמא' : 'IMA'}</h1>{user ? <ChatPanel t={t} lang={lang} user={user} chatOnly /> : <div className="chat-login"><p>{t.personalText}</p><GoogleButton user={user} onUser={setUser} t={t}/>{user&&<button className="cta install-button" onClick={install}>{t.install}</button>}</div>}<button className="chat-only-back" onClick={()=>location.href=BASE}>{lang === 'he' ? 'חזרה לאתר' : 'Back to IMA'}</button></div>;

  return <div className="ima-site" dir={lang === 'he' ? 'rtl' : 'ltr'}>
    {notice && <div role="status" className="site-notice">{notice}</div>}
    <header className="site-header">
      <button className="wordmark" onClick={() => scrollTo({top:0,behavior:'smooth'})} aria-label="IMA home"><span className="wordmark-mark"><img src={CLEAN_LOGO_URL} alt="IMA — אמא" /></span><span><b>אמא</b><small>IMA</small></span></button>
      {user && <nav aria-label="Main navigation">{t.nav.map((item,i)=><button key={item} onClick={()=>document.getElementById(['chat','how','proof','community'][i])?.scrollIntoView({behavior:'smooth'})}>{item}</button>)}</nav>}
      <div className="header-actions"><button className="language" onClick={()=>setLang(lang==='he'?'en':'he')}>{lang==='he'?'English':'עברית'}</button><GoogleButton user={user} onUser={setUser} t={t}/></div>
    </header>
    <main id="top">
      <section className="hero-new">
        <div className="hero-new-copy"><span className="kicker">{t.heroKicker}</span><h1>{t.heroTitle.split('\n').map((x,i)=><React.Fragment key={x}>{i>0&&<br/>}{x}</React.Fragment>)}</h1><p>{t.heroText}</p><div className="hero-new-actions">{!user ? <button className="cta" onClick={()=>document.querySelector('.ima-google')?.scrollIntoView({behavior:'smooth',block:'center'})}>{t.signIn}</button> : <><button className="cta" onClick={()=>setChatOpen(true)}>{t.ask}</button><button className="ghost" onClick={()=>document.getElementById('proof')?.scrollIntoView({behavior:'smooth'})}>{t.proof}</button><button className="ghost install-button" onClick={install}>{t.install}</button><a className="ghost" href={BASE+'?chat=1'}>{t.chatOnly}</a><a className="ghost" href={BASE+'browser-bridge.html'}>{t.browser}</a></>}</div><div className="principle-row"><span>✓ {lang==='he'?'אמת לפני הכרזה':'Truth before claims'}</span><span>✓ {lang==='he'?'אישי נשאר אישי':'Personal stays personal'}</span><span>✓ {lang==='he'?'אדם נשאר בעל הסוכנות':'Human agency stays central'}</span></div></div>
        <a className="mama-hero-link clean-hero-logo" href={GOOGLE_CAMPAIGN_URL} aria-label="IMA public campaign"><img className="clean-ima-logo" src={CLEAN_LOGO_URL} alt="IMA — אמא" loading="eager" /><span>{lang==='he'?'להבין · לבדוק · ללמוד':'Understand · Verify · Learn'}</span></a>
      </section>
      {user && (chatOpen ? <ChatPanel t={t} lang={lang} user={user} onClose={()=>setChatOpen(false)} /> : <section className="chat-collapsed" aria-label={t.openChat}><button onClick={()=>setChatOpen(true)}><MamaFigure compact /><span><b>{lang==='he'?'אמא כאן':'IMA is here'}</b><small>{t.openChat}</small></span></button></section>)}
      <section className="section-new" id="how"><div className="section-intro"><span className="section-label">{t.howKicker}</span><h2>{t.howTitle}</h2></div><div className="principle-grid">{t.cards.map(([n,title,text])=><article key={n}><span>{n}</span><h3>{title}</h3><p>{text}</p></article>)}</div></section>
      <section className="proof-section" id="proof"><div className="section-intro"><span className="section-label">{t.proofKicker}</span><h2>{t.proofTitle}</h2><p>{t.proofText}</p></div><div className="proof-grid"><article><span className="proof-icon">●</span><b>{runtime?t.online:t.offline}</b><p>{runtime?JSON.stringify(runtime.capabilities||{}).slice(0,220):'IMA runtime'}</p></article><article><span className="proof-icon">01</span><b>{lang==='he'?'מקור פתוח':'Open source'}</b><p>{lang==='he'?'הקוד, הבעיות והדיון הציבורי ניתנים לבדיקה.':'Code, issues and public discussion are inspectable.'}</p></article><article><span className="proof-icon">02</span><b>{lang==='he'?'לא הכול חי':'Not everything is live'}</b><p>{lang==='he'?'יכולות מתוכננות אינן מוצגות כהוכחה.':'Planned capabilities are not presented as proof.'}</p></article></div></section>
      <section className="community-section" id="community"><div><span className="section-label">{t.communityKicker}</span><h2>{t.communityTitle}</h2><p>{t.communityText}</p>{user && <div className="community-actions"><a className="cta" href="https://github.com/imaosglobal/Ima-kernel" target="_blank" rel="noreferrer">{t.github}</a><a className="ghost" href="https://github.com/imaosglobal/Ima-kernel/issues/170" target="_blank" rel="noreferrer">{lang==='he'?'הגדרת AGI גלובלית':'Global AGI definition'}</a></div>}</div><div className="feedback-card" id="feedback-panel"><b>{t.feedback}</b><textarea value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder={t.feedbackPlaceholder} maxLength={4000}/><button className="cta" onClick={sendFeedback} disabled={!feedback.trim()}>{t.send}</button>{feedbackStatus&&<small>{feedbackStatus}</small>}</div></section>
      <section className="closing"><div className="closing-mark"><MamaFigure compact/></div><h2>Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.</h2><p>{lang==='he'?'אמא לא אמורה להיות מרכז החיים שלך. היא אמורה לעזור לך להתחזק, להבין יותר ולפעול בעצמך.':'IMA is not meant to become the center of your life. It should help you become stronger, understand more and act for yourself.'}</p></section>
    </main>
    <footer className="site-footer"><span>{t.footer}</span><span><a href="https://github.com/imaosglobal/Ima-kernel">GitHub</a> · <a href={YOUTUBE_URL}>YouTube</a></span><span id="support"><a href={SUPPORT_URL}>{lang==='he'?'תמיכה':'Support'}</a> · <a href={PRIVACY_URL}>{lang==='he'?'פרטיות':'Privacy'}</a></span><a href={GOOGLE_CAMPAIGN_URL}>{lang==='he'?'לתמוך באמא':'Support IMA'}</a><button onClick={()=>setLang(lang==='he'?'en':'he')}>{lang==='he'?'English':'עברית'}</button></footer>
  </div>;
}
