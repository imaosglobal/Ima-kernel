import { Suspense, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Html, useGLTF } from '@react-three/drei';
import { useImaRuntime } from './services/imaRuntime';
import { askIma } from './services/imaChat';

const MODEL = '/Ima-kernel/mother_character.glb';

function Mother() {
  const { scene } = useGLTF(MODEL);
  return <primitive object={scene} scale={1.7} position={[0, -1.65, 0]} />;
}

function Loading() {
  return <Html center><div style={{ color: 'white', fontWeight: 700 }}>אמא מתעוררת…</div></Html>;
}

function MotherScene() {
  return (
    <Canvas camera={{ position: [0, 0.2, 4.8], fov: 38 }}>
      <ambientLight intensity={1.5} />
      <directionalLight position={[2, 4, 3]} intensity={2} />
      <Suspense fallback={<Loading />}>
        <Mother />
        <Environment preset="studio" />
      </Suspense>
      <OrbitControls enablePan={false} minDistance={3.5} maxDistance={6} />
    </Canvas>
  );
}

export default function App() {
  const runtime = useImaRuntime();
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'ima', text: 'אני כאן. אפשר לדבר איתי. מה תרצה לעשות יחד?' },
  ]);

  const send = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setMessages(m => [...m, { role: 'user', text }]);
    setInput('');
    setBusy(true);
    try {
      const response = await askIma(text);
      setMessages(m => [...m, { role: 'ima', text: response }]);
    } catch (error) {
      setMessages(m => [...m, { role: 'system', text: `מנוע השיחה לא זמין כרגע: ${error.message}` }]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <main dir="rtl" style={{ minHeight: '100vh', background: 'radial-gradient(circle at 50% 20%, #30303a 0, #111118 45%, #07070b 100%)', color: '#fff', fontFamily: 'system-ui, sans-serif' }}>
      <header style={{ padding: '20px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div><div style={{ fontSize: 34, fontWeight: 800 }}>אמא</div><div style={{ opacity: .72 }}>האינטליגנציה שמלווה אותך</div></div>
        <div style={{ padding: '8px 14px', borderRadius: 999, background: runtime.status === 'active' ? '#193d2a' : '#432025', fontSize: 13 }}>● {runtime.status === 'active' ? 'Runtime מחובר' : 'מתחברת…'}</div>
      </header>
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '0 18px 28px', display: 'grid', gridTemplateColumns: 'minmax(0, 1.15fr) minmax(320px, .85fr)', gap: 18 }}>
        <div style={{ minHeight: 590, borderRadius: 28, overflow: 'hidden', background: 'linear-gradient(145deg,#292934,#121219)', border: '1px solid #ffffff18', boxShadow: '0 20px 70px #0008' }}><MotherScene /></div>
        <div style={{ minHeight: 590, display: 'flex', flexDirection: 'column', borderRadius: 28, background: '#17171fdd', border: '1px solid #ffffff18', overflow: 'hidden' }}>
          <div style={{ padding: 20, borderBottom: '1px solid #ffffff14' }}><h2 style={{ margin: 0 }}>לדבר עם אמא</h2><div style={{ opacity: .6, fontSize: 13, marginTop: 5 }}>זיכרון {runtime.memory.records.toLocaleString()} · למידה {runtime.learning.records}</div></div>
          <div style={{ flex: 1, padding: 18, overflowY: 'auto' }}>{messages.map((m, i) => <div key={i} style={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-start' : 'flex-end', marginBottom: 12 }}><div style={{ maxWidth: '85%', padding: '12px 15px', borderRadius: 18, background: m.role === 'user' ? '#343440' : m.role === 'system' ? '#48272d' : '#242b38' }}>{m.text}</div></div>)}</div>
          <div style={{ padding: 14, borderTop: '1px solid #ffffff14', display: 'flex', gap: 8 }}>
            <input value={input} disabled={busy} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder={busy ? 'אמא חושבת…' : 'כתוב לאמא…'} style={{ flex: 1, border: 0, outline: 0, borderRadius: 16, padding: '13px 15px', background: '#292932', color: '#fff', fontSize: 16 }} />
            <button onClick={send} disabled={busy} style={{ border: 0, borderRadius: 16, padding: '0 20px', background: '#fff', color: '#111', fontWeight: 800, cursor: busy ? 'wait' : 'pointer' }}>{busy ? '…' : 'שליחה'}</button>
          </div>
        </div>
      </section>
      <footer style={{ maxWidth: 1180, margin: '0 auto', padding: '0 18px 24px', opacity: .55, fontSize: 12 }}>IMA runtime · זיכרון ולמידה נשמרים בצד השרת · ספקי AI חיצוניים יחוברו רק לאחר אימות חיבור אמיתי</footer>
    </main>
  );
}

useGLTF.preload(MODEL);
