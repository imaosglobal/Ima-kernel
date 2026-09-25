import { Suspense, useEffect, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, Html, Stage, useGLTF } from '@react-three/drei';
import { useImaRuntime } from './services/imaRuntime';
import { askIma } from './services/imaChat';

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



const starters = ['מה אפשר לעשות כאן?', 'בואי נחשוב על רעיון', 'תעזרי לי ליצור משהו', 'מה את יודעת לעשות?'];

export default function App() {
  const runtime = useImaRuntime();
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [voice, setVoice] = useState(false);
  const [avatarState, setAvatarState] = useState('idle');
  const [messages, setMessages] = useState([
    { role: 'ima', text: 'אני אמא. אפשר להתחיל כאן בשיחה, רעיון, יצירה או משימה.' }
  ]);

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
      speak(response);
    } catch {
      const response = fallback(text);
      setMessages(m => [...m, { role: 'ima', text: response, fallback: true }]);
      speak(response);
    } finally { setBusy(false); }
  };

  return <main className="ima-app" dir="rtl">
    <header className="topbar">
      <a className="brand" href="#home"><span className="brand-mark">א</span><span>אמא</span></a>
      <nav><a href="#space">המרחב</a><a href="#create">יצירה</a><a href="#tools">כלים</a><a href="#about">על IMA</a></nav>
      <span className="live-pill"><i /> {runtime.status === 'active' ? 'מחוברת' : 'ממשק פעיל'}</span>
    </header>

    <section className="hero" id="home">
      <div className="hero-copy">
        <p className="eyebrow">IMA · HUMAN-CENTERED INTELLIGENCE</p>
        <h1>מקום אחד<br /><em>להיות, לחשוב וליצור.</em></h1>
        <p className="hero-text">אמא היא מרחב חי לשיחה עם אינטליגנציה שמחברת בין ידע, רעיונות, יצירה וכלים — בלי להעמיד פנים שחיבור שלא קיים כבר קיים.</p>
        <div className="hero-actions">
          <button className="primary" onClick={() => document.getElementById('chat')?.scrollIntoView({ behavior: 'smooth' })}>לדבר עם אמא <span>←</span></button>
          <button className="secondary" onClick={() => send('מה אפשר לעשות כאן?')}>לראות מה אפשר לעשות</button>
        </div>
        <div className="trust-line"><span>●</span> שקיפות ביכולות · פרטיות · שליטה אנושית</div>
      </div>
      <div className="presence-card" aria-label="נוכחות תלת ממדית">
        <div className="orb"><PresenceScene state={avatarState} /></div>
        <div className="presence-label"><span>נוכחות</span><b>IMA / NOW</b></div>
      </div>
    </section>

    <section className="chat-section" id="space">
      <div className="section-heading"><p className="eyebrow">THE SPACE</p><h2>פשוט לדבר.</h2><p>לא צריך לדעת איזה כלי נמצא מאחורי הקלעים. פשוט אומרים מה רוצים.</p></div>
      <div className="chat-shell" id="chat">
        <div className="chat-head"><div><strong>אמא</strong><span>מרחב שיחה</span></div><button className={voice ? 'voice active' : 'voice'} onClick={() => setVoice(v => !v)}>◉ {voice ? 'קול פעיל' : 'קול'}</button></div>
        <div className="messages">
          {messages.map((m, i) => <div key={i} className={'message-row ' + m.role}><div className="message">{m.text}{m.fallback && <small> · מצב מקומי</small>}</div></div>)}
          {busy && <div className="message-row ima"><div className="message typing"><i /><i /><i /></div></div>}
        </div>
        <div className="starters">{starters.map(s => <button key={s} onClick={() => send(s)}>{s}</button>)}</div>
        <div className="composer"><input value={input} disabled={busy} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="כתוב לאמא..." /><button onClick={() => send()} disabled={busy}>שליחה</button></div>
      </div>
    </section>

    <section className="principles" id="about">
      <div><span>01</span><h3>אנושית לפני טכנולוגיה</h3><p>הטכנולוגיה היא שכבה שמשרתת את האדם, לא להפך.</p></div>
      <div><span>02</span><h3>יכולות אמיתיות</h3><p>כל חיבור חדש צריך להיות מחובר ומאומת לפני שהוא מוצג כפעיל.</p></div>
      <div><span>03</span><h3>עולם שלם בהמשך</h3><p>קול, יצירה, כלים, מכשירים ושפות מתווספים כשיש להם תשתית אמיתית.</p></div>
    </section>

    <footer id="tools"><span>אמא — IMA</span><span>by Ori Cohen</span><span>Human-centered intelligence layer</span></footer>
  </main>;
}