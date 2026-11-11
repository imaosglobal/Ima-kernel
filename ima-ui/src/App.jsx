import React, { useEffect, useState } from 'react';
import {
  askIma,
  getAuthConfig,
  signInWithGoogleCredential,
  getStoredGoogleUser,
  signOutIma,
  getImaRuntime,
  submitFeedback
} from './services/imaChat';
import { initializeImaAnalytics, trackImaEvent } from './services/analytics';

const BASE = '/Ima-kernel/';
const copy = {
  he: {
    nav: ['לדבר', 'איך זה עובד', 'הוכחות', 'קהילה'],
    heroKicker: 'IMA — אמא · בינה אנושית',
    heroTitle: 'בינה שנועדה\nלהבין אותך.',
    heroText: 'אמא לא מבקשת ממך להאמין שהיא יודעת הכול. היא מתחילה בהקשבה, מבדילה בין עובדה לאי־ודאות, ולומדת רק כשיש סיבה וראיות.',
    ask: 'לדבר עם אמא',
    proof: 'לראות מה באמת עובד',
    prompt: 'מה תרצה לעשות עם אמא?',
    modes: ['לחשוב', 'ללמוד', 'ליצור', 'לפתור'],
    modeText: ['להבין רעיון, החלטה או מצב', 'לחקור נושא ולגלות מה חסר', 'לכתוב, לתכנן או ליצור', 'להפוך צורך לצעדים מעשיים'],
    howKicker: 'איך אמא עובדת',
    howTitle: 'פחות הבטחות. יותר בדיקה.',
    cards: [
      ['01', 'הקשבה', 'מתחילים במה שאתה באמת צריך — לא בתפריט של יכולות.'],
      ['02', 'הקשר', 'שפה, נגישות, זיכרון והרגלים יכולים להתאים אליך; הסוכנות נשארת שלך.'],
      ['03', 'אימות', 'אמא מפרידה בין מה שנבדק, מה שנבנה ומה שעדיין לא הוכח.'],
      ['04', 'למידה', 'אפשר לתקן את אמא. תרומה נכנסת למסלול אימות, לא הופכת אוטומטית לאמת.']
    ],
    proofKicker: 'חלון הוכחה',
    proofTitle: 'מה אמא יכולה עכשיו?',
    proofText: 'אנחנו לא מציגים תיעוד כהוכחה. כאן מוצגים רק סימנים שניתן לבדוק בזמן אמת.',
    runtime: 'בודקת את המערכת…',
    online: 'Runtime זמין',
    offline: 'Runtime לא אומת כרגע',
    communityKicker: 'קהילה גלובלית',
    communityTitle: 'אמא נבנית עם העולם, לא מעליו.',
    communityText: 'חוקרים, יוצרים, מפתחים, משפחות וארגונים יכולים לשאול, ללמד, לבדוק ולבנות. GitHub הוא חלון הראיות הציבורי.',
    github: 'לפתוח את GitHub',
    feedback: 'לתת משוב',
    feedbackPlaceholder: 'מה יעזור לך לחזור לאמא?',
    send: 'שליחה',
    signIn: 'כניסה אישית עם Google',
    signed: 'מחובר',
    logout: 'יציאה',
    personal: 'מרחב אישי',
    personalText: 'כניסה מאפשרת חוויה אישית ושמירת הקשר לפי ההרשאות שלך.',
    footer: 'IMA — אמא, by Ori Cohen · Human-centered intelligence',
    global: 'עברית',
    language: 'English'
  },
  en: {
    nav: ['Talk', 'How it works', 'Proof', 'Community'],
    heroKicker: 'IMA — human-centered intelligence',
    heroTitle: 'Intelligence\ndesigned to understand you.',
    heroText: 'IMA does not ask you to believe it knows everything. It starts by listening, separates facts from uncertainty, and learns when there is a reason and evidence.',
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
    runtime: 'Checking system…',
    online: 'Runtime available',
    offline: 'Runtime not verified now',
    communityKicker: 'Global community',
    communityTitle: 'IMA is built with the world, not above it.',
    communityText: 'Researchers, creators, developers, families and organizations can question, teach, test and build. GitHub is the public evidence window.',
    github: 'Open GitHub',
    feedback: 'Give feedback',
    feedbackPlaceholder: 'What would make you come back to IMA?',
    send: 'Send',
    signIn: 'Personal sign-in with Google',
    signed: 'Signed in',
    logout: 'Log out',
    personal: 'Personal space',
    personalText: 'Sign in for a personal experience and continuity according to your permissions.',
    footer: 'IMA — אמא, by Ori Cohen · Human-centered intelligence',
    global: 'English',
    language: 'עברית'
  }
};

function GoogleButton({ user, onUser, t }) {
  const [error, setError] = useState('');
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const config = await getAuthConfig();
        if (!config?.google?.enabled || !config.google.client_id) {
          if (!cancelled) setError('Google sign-in is not configured');
          return;
        }
        for (let i = 0; i < 40 && !window.google?.accounts?.id && !cancelled; i++) {
          await new Promise(r => setTimeout(r, 100));
        }
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
            } catch {
              setError('Sign-in could not be completed');
            }
          },
          auto_select: false,
          ux_mode: 'popup'
        });
        const node = document.getElementById('ima-google-button');
        if (node) {
          node.innerHTML = '';
          window.google.accounts.id.renderButton(node, {
            type: 'standard',
            theme: 'outline',
            size: 'large',
            text: 'signin_with',
            shape: 'pill',
            width: 280
          });
        }
        if (!cancelled) setReady(true);
      } catch {
        if (!cancelled) setError('Google sign-in unavailable');
      }
    })();
    return () => { cancelled = true; };
  }, [onUser]);

  if (user) return (
    <div className="ima-account">
      <span className="ima-account-dot">{String(user.name || 'א').slice(0,1)}</span>
      <span>{user.name || user.email || t.signed}</span>
      <button onClick={() => { signOutIma(); onUser(null); }}>{t.logout}</button>
    </div>
  );

  return <div className="ima-google">
    <div id="ima-google-button" aria-label={t.signIn} />
    {!ready && !error && <span className="tiny-status">{t.signIn}</span>}
    {error && <span className="tiny-error">{error}</span>}
  </div>;
}

export default function App() {
  const [lang, setLang] = useState(() => localStorage.getItem('ima-site-language') || (navigator.language?.startsWith('he') ? 'he' : 'en'));
  const [user, setUser] = useState(() => getStoredGoogleUser());
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const [runtime, setRuntime] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [feedbackStatus, setFeedbackStatus] = useState('');
  const [notice, setNotice] = useState('');
  const t = copy[lang];
  const dir = lang === 'he' ? 'rtl' : 'ltr';

  useEffect(() => {
    localStorage.setItem('ima-site-language', lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = dir;
    document.title = lang === 'he' ? 'אמא — IMA | בינה אנושית' : 'IMA — Human-Centered Intelligence';
    initializeImaAnalytics();
    trackImaEvent('ima_public_redesign_view', { language: lang });
  }, [lang, dir]);

  useEffect(() => {
    getImaRuntime().then(setRuntime).catch(() => setRuntime(null));
  }, []);

  const send = async (text = message) => {
    const value = String(text || '').trim();
    if (!value || busy) return;
    setBusy(true);
    setMessage('');
    setMessages(prev => [...prev, { role: 'user', text: value }]);
    try {
      const response = await askIma(value, { language: lang, interface: 'public-redesign' });
      setMessages(prev => [...prev, { role: 'ima', text: response }]);
      trackImaEvent('ima_first_useful_answer_candidate', { language: lang });
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ima', text: lang === 'he'
        ? 'אני עדיין לא מצליחה לענות דרך החיבור הציבורי הזה. זו תקלה שאנחנו צריכים למדוד ולתקן — לא להסתיר.'
        : 'I cannot answer through the public connection right now. This is a failure to measure and fix, not something to hide.' }]);
      trackImaEvent('ima_public_chat_failed', { error: error?.message || 'unknown' });
    } finally {
      setBusy(false);
    }
  };

  const scrollTo = id => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });

  const sendFeedback = async () => {
    if (!feedback.trim()) return;
    setFeedbackStatus('');
    try {
      await submitFeedback('improvement', feedback.trim(), { language: lang, source: 'public-redesign' });
      setFeedback('');
      setFeedbackStatus(lang === 'he' ? 'המשוב נשמר.' : 'Feedback saved.');
    } catch {
      setFeedbackStatus(lang === 'he' ? 'לא הצלחתי לאמת את השמירה.' : 'Could not verify that the feedback was saved.');
    }
  };

  return (
    <div className="ima-site" dir={dir}>
      {notice && <div role="status" className="site-notice">{notice}</div>}
      <header className="site-header">
        <button className="wordmark" onClick={() => scrollTo('top')} aria-label="IMA home">
          <span className="wordmark-mark">א</span>
          <span><b>אמא</b><small>IMA</small></span>
        </button>
        <nav aria-label="Main navigation">
          <button onClick={() => scrollTo('chat')}>{t.nav[0]}</button>
          <button onClick={() => scrollTo('how')}>{t.nav[1]}</button>
          <button onClick={() => scrollTo('proof')}>{t.nav[2]}</button>
          <button onClick={() => scrollTo('community')}>{t.nav[3]}</button>
        </nav>
        <div className="header-actions">
          <button className="language" onClick={() => setLang(lang === 'he' ? 'en' : 'he')}>{t.language}</button>
          <GoogleButton user={user} onUser={setUser} t={t} />
        </div>
      </header>

      <main id="top">
        <section className="hero-new">
          <div className="hero-new-copy">
            <span className="kicker">{t.heroKicker}</span>
            <h1>{t.heroTitle.split('\n').map((x,i)=><React.Fragment key={x}>{i>0 && <br/>}{x}</React.Fragment>)}</h1>
            <p>{t.heroText}</p>
            <div className="hero-new-actions">
              <button className="cta" onClick={() => scrollTo('chat')}>{t.ask}</button>
              <button className="ghost" onClick={() => scrollTo('proof')}>{t.proof}</button>
            </div>
            <div className="principle-row">
              <span>✓ {lang === 'he' ? 'אמת לפני הכרזה' : 'Truth before claims'}</span>
              <span>✓ {lang === 'he' ? 'אישי נשאר אישי' : 'Personal stays personal'}</span>
              <span>✓ {lang === 'he' ? 'אדם נשאר בעל הסוכנות' : 'Human agency stays central'}</span>
            </div>
          </div>
          <div className="hero-orb" aria-hidden="true">
            <div className="orb-ring ring-one" />
            <div className="orb-ring ring-two" />
            <div className="orb-core"><span>א</span></div>
            <div className="orb-label">{lang === 'he' ? 'להבין · לבדוק · ללמוד' : 'Understand · Verify · Learn'}</div>
          </div>
        </section>

        <section className="try-strip" id="chat">
          <div className="section-label">{t.nav[0]}</div>
          <h2>{t.prompt}</h2>
          <div className="mode-row">
            {t.modes.map((m,i) => <button key={m} onClick={() => send(m + ': ' + t.modeText[i])}><span>0{i+1}</span><b>{m}</b><small>{t.modeText[i]}</small></button>)}
          </div>
          <div className="chat-window">
            <div className="chat-top">
              <div><span className="status-dot" /> <b>IMA</b></div>
              <span>{user ? t.personal : (lang === 'he' ? 'שיחה ציבורית' : 'Public conversation')}</span>
            </div>
            <div className="chat-messages" aria-live="polite">
              {!messages.length && <div className="chat-empty">{lang === 'he' ? 'שאל שאלה אמיתית. לא צריך לדעת איך אמא בנויה.' : 'Ask a real question. You do not need to understand how IMA is built.'}</div>}
              {messages.map((m,i) => <div key={i} className={'chat-bubble '+m.role}>{m.text}</div>)}
              {busy && <div className="chat-bubble ima muted">IMA…</div>}
            </div>
            <div className="chat-composer">
              <input value={message} onChange={e=>setMessage(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder={lang === 'he' ? 'כתוב לאמא…' : 'Write to IMA…'} aria-label="Message IMA" />
              <button onClick={()=>send()} disabled={busy || !message.trim()}>{lang === 'he' ? 'שליחה' : 'Send'}</button>
            </div>
          </div>
          {!user && <div className="personal-note"><span>{t.personal}</span><p>{t.personalText}</p><GoogleButton user={user} onUser={setUser} t={t} /></div>}
        </section>

        <section className="section-new" id="how">
          <div className="section-intro"><span className="section-label">{t.howKicker}</span><h2>{t.howTitle}</h2></div>
          <div className="principle-grid">{t.cards.map(([n,title,text]) => <article key={n}><span>{n}</span><h3>{title}</h3><p>{text}</p></article>)}</div>
        </section>

        <section className="proof-section" id="proof">
          <div className="section-intro"><span className="section-label">{t.proofKicker}</span><h2>{t.proofTitle}</h2><p>{t.proofText}</p></div>
          <div className="proof-grid">
            <article><span className="proof-icon">●</span><b>{runtime ? t.online : t.offline}</b><p>{runtime ? JSON.stringify(runtime.capabilities || {}).slice(0,220) : t.runtime}</p></article>
            <article><span className="proof-icon">01</span><b>{lang === 'he' ? 'מקור פתוח' : 'Open source'}</b><p>{lang === 'he' ? 'הקוד, הבעיות והדיון הציבורי ניתנים לבדיקה.' : 'Code, issues and public discussion are inspectable.'}</p></article>
            <article><span className="proof-icon">02</span><b>{lang === 'he' ? 'לא הכול חי' : 'Not everything is live'}</b><p>{lang === 'he' ? 'יכולות מתוכננות אינן מוצגות כהוכחה.' : 'Planned capabilities are not presented as proof.'}</p></article>
          </div>
        </section>

        <section className="community-section" id="community">
          <div>
            <span className="section-label">{t.communityKicker}</span>
            <h2>{t.communityTitle}</h2>
            <p>{t.communityText}</p>
            <div className="community-actions">
              <a className="cta" href="https://github.com/imaosglobal/Ima-kernel" target="_blank" rel="noreferrer">{t.github}</a>
              <a className="ghost" href="https://github.com/imaosglobal/Ima-kernel/issues/170" target="_blank" rel="noreferrer">{lang === 'he' ? 'הגדרת AGI גלובלית' : 'Global AGI definition'}</a>
            </div>
          </div>
          <div className="feedback-card">
            <b>{t.feedback}</b>
            <textarea value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder={t.feedbackPlaceholder} maxLength={4000} />
            <button className="cta" onClick={sendFeedback} disabled={!feedback.trim()}>{t.send}</button>
            {feedbackStatus && <small>{feedbackStatus}</small>}
          </div>
        </section>

        <section className="closing">
          <div className="closing-mark">א</div>
          <h2>{lang === 'he' ? 'Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.' : 'Use IMA. Question IMA. Teach IMA. Build IMA. Test IMA.'}</h2>
          <p>{lang === 'he' ? 'אמא לא אמורה להיות מרכז החיים שלך. היא אמורה לעזור לך להתחזק, להבין יותר ולפעול בעצמך.' : 'IMA is not meant to become the center of your life. It should help you become stronger, understand more and act for yourself.'}</p>
        </section>
      </main>

      <footer className="site-footer">
        <span>{t.footer}</span>
        <span><a href="https://github.com/imaosglobal/Ima-kernel" target="_blank" rel="noreferrer">GitHub</a></span>
        <span><a href={BASE + 'privacy.html'}>{lang === 'he' ? 'פרטיות' : 'Privacy'}</a></span>
        <button onClick={()=>setLang(lang === 'he' ? 'en' : 'he')}>{t.global}</button>
      </footer>
    </div>
  );
}
