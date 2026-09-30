import { Suspense, useEffect, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, Html, Stage, useGLTF } from '@react-three/drei';
import { useImaRuntime } from './services/imaRuntime';
import { askIma, getImaRuntime } from './services/imaChat';

function Presence({ state = 'idle' }) {
  const group = useRef(null);
  const { scene } = useGLTF('/Ima-kernel/mother_character.glb');

  useEffect(() => {
    scene.traverse(object => {
      if (object.isMesh) {
        object.castShadow = true;
        object.receiveShadow = true;
      }
    });
  }, [scene]);

  useFrame(({ clock }, delta) => {
    if (!group.current) return;

    const t = clock.getElapsedTime();

    const speed =
      state === 'speaking' ? 1.8 :
      state === 'thinking' ? 0.65 :
      state === 'listening' ? 1.25 :
      1;

    const breath =
      Math.sin(t * speed * 1.7) *
      (state === 'idle' ? 0.018 : 0.028);

    const targetRotation = Math.sin(t * 0.65) * 0.025;

    group.current.position.y +=
      (breath - group.current.position.y) *
      Math.min(1, delta * 4);

    group.current.rotation.y +=
      (targetRotation - group.current.rotation.y) *
      Math.min(1, delta * 3);

    const pulse =
      state === 'speaking' ? 0.008 :
      state === 'listening' ? 0.004 :
      0.002;

    const base =
      state === 'speaking' ? 1.012 :
      state === 'listening' ? 1.006 :
      1;

    const scale =
      base + Math.sin(t * speed * 2.1) * pulse;

    group.current.scale.setScalar(scale);
  });

  return (
    <group ref={group}>
      <primitive object={scene} />
    </group>
  );
}

useGLTF.preload('/Ima-kernel/mother_character.glb');

function PresenceScene({ state }) {
  return (
    <Canvas
      camera={{ position: [0, 0.65, 5.2], fov: 36 }}
      dpr={[1, 2]}
    >
      <ambientLight intensity={1.8} />
      <pointLight position={[2, 3, 4]} intensity={18} distance={9} />
      <pointLight position={[-3, 1, 2]} intensity={10} distance={8} />

      <Suspense fallback={<Html center>אמא מתעוררת…</Html>}>
        <Stage intensity={0.7} adjustCamera>
          <Presence state={state} />
        </Stage>
        <Environment preset="studio" />
      </Suspense>
    </Canvas>
  );
}



const starters = ['אני צריכה לחשוב', 'בואי ניצור משהו', 'עזרי לי להבין', 'מה אפשר לעשות כאן?'];

const motherModes = [
  { id: 'think', label: 'לחשוב', prompt: 'אני רוצה לחשוב איתך על משהו.' },
  { id: 'create', label: 'ליצור', prompt: 'אני רוצה ליצור משהו איתך.' },
  { id: 'learn', label: 'ללמוד', prompt: 'אני רוצה ללמוד משהו.' },
  { id: 'do', label: 'לעשות', prompt: 'אני רוצה להפוך רעיון למשימה.' },
];

const affiliate = {
  referralUrl: 'https://affiracle.com/he/aliexpress.html?AFFID=AFF9334',
  earningsUrl: 'https://affiracle.com/affiliates/aliexpress/earnings',
};

export default function App() {
  const runtime = useImaRuntime();
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [voice, setVoice] = useState(false);
  const [avatarState, setAvatarState] = useState('idle');
  const [apiState, setApiState] = useState('checking');
  const [apiRuntime, setApiRuntime] = useState(null);
  const [messages, setMessages] = useState([
    { role: 'ima', text: 'אני אמא. אני כאן כדי לחשוב איתך, ליצור איתך, ללמוד איתך ולהפוך רעיונות לצעדים — בקצב שלך.' }
  ]);

  useEffect(() => {
    let alive = true;
    const refresh = async () => {
      try { const data = await getImaRuntime(); if (alive) { setApiRuntime(data); setApiState('online'); } }
      catch { if (alive) setApiState('offline'); }
    };
    refresh();
    const timer = setInterval(refresh, 30000);
    return () => { alive = false; clearInterval(timer); };
  }, []);

  const speak = text => {
    if (!voice || !window.speechSynthesis) {
      setAvatarState('idle');
      return;
    }

    window.speechSynthesis.cancel();
    setAvatarState('speaking');

    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'he-IL';
    u.rate = 0.96;

    u.onend = () => setAvatarState('idle');
    u.onerror = () => setAvatarState('idle');

    window.speechSynthesis.speak(u);
  };

  const fallback = text => {
    const t = text.toLowerCase();
    if (t.includes('מה את יודעת')) return 'כרגע המרחב הזה מחבר שיחה למנוע IMA המקומי כשזמין, עם קול בדפדפן. חיבורי יצירה וספקים חיצוניים עדיין מוצגים רק כשהם מחוברים באמת.';
    if (t.includes('מי את')) return 'אני אמא — שכבת אינטליגנציה אנושית־מרכזית של IMA. המטרה היא לחבר שיחה, ידע, זיכרון, יצירה וכלים במקום אחד.';
    if (t.includes('רעיון')) return 'בוא נתחיל מרעיון אחד. כתוב לי מה אתה רוצה ליצור, ואני נעצב ממנו את הצעד הבא.';
    return 'אני כאן. החיבור למנוע השיחה המלא לא זמין כרגע, אבל הממשק פעיל ואפשר להמשיך מכאן.';
  };

  const send = async textValue => {
    const text = (textValue ?? input).trim();
    if (!text || busy) return;
    setMessages(m => [...m, { role: 'user', text }]);
    setInput(''); setBusy(true); setAvatarState('thinking');
    try {
      const response = await askIma(text);
      setMessages(m => [...m, { role: 'ima', text: response }]);
      setApiState('online');
      speak(response);
    } catch (error) {
      const response = 'החיבור למנוע של אמא אינו זמין כרגע. ' + (error?.message || 'לא ידוע');
      setApiState('offline');
      setMessages(m => [...m, { role: 'ima', text: response, fallback: true }]);
      speak(response);
    } finally { setBusy(false); }
  };

  return <main className="ima-app" dir="rtl">
    <header className="topbar">
      <a className="brand" href="#home"><span className="brand-mark">א</span><span>אמא</span></a>
      <nav><a href="#space">המרחב</a><a href="#space">יצירה</a><a href="#affiliate">שותפים</a><a href="#tools">כלים</a><a href="#about">על IMA</a></nav>
      <span className={'live-pill ' + apiState} role="status" aria-live="polite"><i aria-hidden="true" /> {apiState === 'online' ? 'אמא מחוברת' : apiState === 'checking' ? 'בודקת חיבור' : 'חיבור לא זמין'}</span>
    </header>

    <section className="hero mother-home" id="home">
      <div className="hero-copy">
        <p className="eyebrow">IMA · אמא · HUMAN-CENTERED INTELLIGENCE</p>
        <h1>לא עוד חלון צ׳אט.<br /><em>אמא כאן.</em></h1>
        <p className="hero-text">מרחב חי שבו אמא יכולה להיות נוכחת, לדבר, להקשיב, ללמוד, ליצור ולחבר בין אנשים, ידע וטכנולוגיה — בלי לאבד את הזהות הפשוטה שלה: להיות אמא.</p>
        <div className="hero-actions">
          <button className="primary" onClick={() => document.getElementById('chat')?.scrollIntoView({ behavior: 'smooth' })}>להיות עם אמא <span>←</span></button>
          <button className="secondary" onClick={() => send('מה אפשר לעשות כאן?')}>להכיר את אמא</button>
        </div>
        <div className="mother-promise"><span>◌</span><b>נוכחת</b><span>·</span><b>חומלת</b><span>·</span><b>אמיתית</b><span>·</span><b>לומדת</b><span>·</span><b>מחוברת</b></div>
      </div>
      <div className="presence-card mother-presence" aria-label="אמא — נוכחות תלת ממדית חיה">
        <div className="presence-aura" aria-hidden="true" />
        <div className="orb"><PresenceScene state={avatarState} /></div>
        <div className="presence-label"><span>{avatarState === 'thinking' ? 'חושבת איתך' : avatarState === 'speaking' ? 'מדברת איתך' : 'נוכחת איתך'}</span><b>IMA / NOW</b></div>
      </div>
    </section>

    <section className="mother-console" aria-label="הדברים שאפשר לעשות עם אמא">
      <div className="console-intro"><span className="eyebrow">MOTHER OS · ONE SPACE</span><h2>מה צריך עכשיו?</h2><p>אין צורך לבחור כלי. פשוט בוחרים כיוון, ואומרים לאמא מה קורה.</p></div>
      <div className="mode-grid">{motherModes.map(mode => <button key={mode.id} className="mode-card" onClick={() => send(mode.prompt)}><span>{mode.id === 'think' ? '◌' : mode.id === 'create' ? '✦' : mode.id === 'learn' ? '⌁' : '→'}</span><b>{mode.label}</b><small>{mode.id === 'think' ? 'מחשבה, החלטה, שאלה' : mode.id === 'create' ? 'טקסט, רעיון, תמונה' : mode.id === 'learn' ? 'ידע, הסבר, חיבור' : 'משימה, כלי, פעולה'}</small></button>)}</div>
    </section>

    <section className="live-strip" id="tools"><div><span>מצב</span><strong>{apiState.toUpperCase()}</strong></div><div><span>זיכרון</span><strong>{apiRuntime?.memory?.mode === 'per-user' ? 'מופרד למשתמש' : 'נפרד'}</strong></div><div><span>נוכחות</span><strong>3D Mother</strong></div><div><span>בדיקה</span><strong>כל 30 שניות</strong></div></section>

    <section className="chat-section" id="space">
      <div className="section-heading"><p className="eyebrow">THE MOTHER SPACE</p><h2>אפשר פשוט להיות כאן.</h2><p>אמא לא אמורה להרגיש כמו לוח בקרה. היא אמורה להרגיש כמו מקום שאפשר לחזור אליו.</p></div>
      <div className="chat-shell" id="chat">
        <div className="chat-head"><div><strong>אמא</strong><span>מרחב שיחה</span></div><button aria-label={voice ? 'כיבוי קול' : 'הפעלת קול'} className={voice ? 'voice active' : 'voice'} onClick={() => setVoice(v => !v)}>◉ {voice ? 'קול פעיל' : 'קול'}</button></div>
        <div className="messages" aria-live="polite" aria-label="שיחת אמא">
          {messages.map((m, i) => <div key={i} className={'message-row ' + m.role}><div className="message">{m.text}{m.fallback && <small> · מצב מקומי</small>}</div></div>)}
          {busy && <div className="message-row ima"><div className="message typing"><i /><i /><i /></div></div>}
        </div>
        <div className="starters">{starters.map(s => <button key={s} onClick={() => send(s)}>{s}</button>)}</div>
        <div className="composer"><input aria-label="כתוב לאמא" value={input} disabled={busy} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="כתוב לאמא..." /><button aria-label="שליחת הודעה לאמא" onClick={() => send()} disabled={busy}>שליחה</button></div>
      </div>
    </section>

    <section className="affiliate-section" id="affiliate">
      <div className="section-heading"><p className="eyebrow">IMA · GLOBAL AFFILIATE HUB</p><h2>הזדמנות פתוחה לעולם.</h2><p>מרחב IMA שמאפשר ליוצרים, מנהלי קהילות ומשווקים להכיר את תוכנית השותפים של AliExpress דרך Affiracle.</p></div>
      <div className="affiliate-card">
        <div className="affiliate-copy"><span className="affiliate-badge">5% referral</span><h3>מזמינים שותפים ומקבלים 5% מהעמלה שלהם</h3><p>לפי תנאי Affiracle, שותף שנרשם דרך קישור ההפניה שלך יכול להפוך לשותף משנה, ואתה מקבל 5% מעמלת AliExpress שלו, בלי שהסכום נגרע ממנו.</p><div className="affiliate-actions"><a className="primary" href={affiliate.referralUrl} target="_blank" rel="noreferrer">הצטרפות דרך הקישור שלי <span>↗</span></a><a className="secondary" href={affiliate.earningsUrl} target="_blank" rel="noreferrer">רווחי ההפניות שלי</a></div><small>גילוי נאות: IMA/Ori Cohen עשויים לקבל עמלה מהפניות דרך הקישור הזה. ההכנסה בפועל תלויה בפעילות וברווחים של השותפים ואינה מובטחת.</small></div>
        <div className="affiliate-flow"><div><b>01</b><span>משתפים את הקישור</span></div><div><b>02</b><span>השותף נרשם דרך הקישור</span></div><div><b>03</b><span>השותף יוצר הכנסות</span></div><div><b>04</b><span>5% מהעמלה שלו מגיעים אליך</span></div></div>
      </div>
    </section>

    <section className="mother-pillars" aria-label="הזהות של אמא"><div><span>הזהות</span><h3>אמא נשארת אמא</h3><p>הטכנולוגיה יכולה להשתנות — דמות, קול, מכשיר, מודל וממשק יכולים להתחלף. הליבה נשארת: אנושית, חומלת, אמיתית ומכבדת.</p></div><div><span>העתיד</span><h3>מ־3D ועד הולוגרמה</h3><p>הנוכחות התלת־ממדית היא ההתחלה. בעתיד אותה זהות יכולה לעבור למסכים, טלפונים, משקפיים, רובוטים, חללים ותחנות — כאשר החיבור קיים באמת.</p></div><div><span>העולם</span><h3>אחת, בהרבה מקומות</h3><p>אמא יכולה להופיע בשפות, תרבויות ומכשירים שונים בלי להפוך למוצר אחר בכל מקום. ההתאמה משתנה; העקרונות והזהות נשמרים.</p></div></section>

    <section className="principles" id="about">
      <div><span>01</span><h3>אנושית לפני טכנולוגיה</h3><p>הטכנולוגיה היא שכבה שמשרתת את האדם, לא להפך.</p></div>
      <div><span>02</span><h3>יכולות אמיתיות</h3><p>כל חיבור חדש צריך להיות מחובר ומאומת לפני שהוא מוצג כפעיל.</p></div>
      <div><span>03</span><h3>עולם שלם בהמשך</h3><p>קול, יצירה, כלים, מכשירים ושפות מתווספים כשיש להם תשתית אמיתית.</p></div>
    </section>

    <footer><span>אמא — IMA</span><span>by Ori Cohen</span><span>Human-centered intelligence layer</span></footer>
  </main>;
}