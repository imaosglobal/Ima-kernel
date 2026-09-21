import { Suspense, useMemo, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Environment, Float, Html, OrbitControls } from '@react-three/drei';
import { useImaRuntime } from './services/imaRuntime';
import { askIma } from './services/imaChat';

function MotherPresence() {
  return (
    <Float speed={1.1} rotationIntensity={0.08} floatIntensity={0.18}>
      <group position={[0, -0.85, 0]}>
        <mesh position={[0, 0.1, 0]}>
          <sphereGeometry args={[0.9, 48, 48]} />
          <meshPhysicalMaterial transmission={0.28} roughness={0.18} metalness={0.12} clearcoat={1} />
        </mesh>
        <mesh position={[0, 1.28, 0]}>
          <sphereGeometry args={[0.46, 48, 48]} />
          <meshPhysicalMaterial transmission={0.2} roughness={0.2} clearcoat={1} />
        </mesh>
        <mesh position={[0, 1.55, -0.04]} scale={[0.58, 0.7, 0.48]}>
          <sphereGeometry args={[1, 48, 48]} />
          <meshStandardMaterial transparent opacity={0.42} roughness={0.28} />
        </mesh>
      </group>
    </Float>
  );
}function MotherScene() {
  return (
    <Canvas camera={{ position: [0, 0.65, 5.2], fov: 36 }} dpr={[1, 2]}>
      <ambientLight intensity={1.8} />
      <pointLight position={[2, 3, 4]} intensity={18} distance={9} />
      <pointLight position={[-3, 1, 2]} intensity={10} distance={8} />
      <Suspense fallback={<Html center>אמא מתעוררת…</Html>}>
        <MotherPresence />
        <Environment preset="studio" />
      </Suspense>
      <OrbitControls enablePan={false} minDistance={3.6} maxDistance={6.5} />
    </Canvas>
  );
}

const features = [
  ['זיכרון', 'memory'], ['למידה', 'learning'], ['קול', 'voice'],
  ['יצירה', 'creative'], ['כלים', 'tools'], ['מכשירים', 'devices']
];

export default function App() {
  const runtime = useImaRuntime();
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);  const [messages, setMessages] = useState([
    { role: 'ima', text: 'אני כאן. זה המרחב החדש של אמא. אפשר להתחיל בכל שאלה, רעיון או משימה.' },
  ]);
  const [voiceOn, setVoiceOn] = useState(false);

  const speak = (text) => {
    if (!voiceOn || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'he-IL';
    utterance.rate = 0.96;
    window.speechSynthesis.speak(utterance);
  };

  const send = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setMessages(m => [...m, { role: 'user', text }]);
    setInput('');
    setBusy(true);
    try {
      const response = await askIma(text);
      setMessages(m => [...m, { role: 'ima', text: response }]);
      speak(response);
    } catch (error) {
      setMessages(m => [...m, { role: 'system', text: 'חיבור אמא נכשל: ' + error.message }]);
    } finally {      setBusy(false);
    }
  };

  const active = runtime.status === 'active';
  const statusText = active ? 'מחוברת לליבת IMA' : 'חיבור ליבה לא זמין';
  const counts = useMemo(() => ({
    memory: runtime.memory?.records ?? 0,
    learning: runtime.learning?.records ?? 0
  }), [runtime]);

  return (
    <main dir="rtl" style={{
      minHeight: '100vh', color: '#f7f4ef', fontFamily: 'system-ui,sans-serif',
      background: 'radial-gradient(circle at 72% 18%,#5d466433,transparent 30%),#05060a'
    }}>
      <header style={{
        maxWidth: 1440, margin: 'auto', padding: '22px 28px',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
      }}>
        <div>
          <div style={{fontSize:34,fontWeight:800}}>אמא</div>
          <div style={{opacity:.62}}>אינטליגנציה אנושית־מרכזית, מחוברת לעולם</div>
        </div>
        <div style={{padding:'9px 14px',border:'1px solid #ffffff1c',borderRadius:999,fontSize:13}}>
          ● {statusText}
        </div>      </header>
      <section style={{
        maxWidth:1440, margin:'auto', padding:'10px 28px 36px',
        display:'grid', gridTemplateColumns:'1.3fr .7fr', gap:20
      }}>
        <div style={{
          minHeight:680, position:'relative', overflow:'hidden', borderRadius:30,
          border:'1px solid #ffffff14', background:'#ffffff08',
          boxShadow:'0 30px 100px #0008'
        }}>
          <div style={{position:'absolute',inset:0}}><MotherScene /></div>
          <div style={{position:'absolute',right:28,bottom:26,zIndex:2,maxWidth:500}}>
            <div style={{fontSize:12,letterSpacing:2,opacity:.5}}>IMA · PRESENT / NEXT</div>
            <h1 style={{fontSize:'clamp(38px,5vw,72px)',lineHeight:.98,margin:'10px 0'}}>
              לא עוד חלון צ׳אט.
            </h1>
            <p style={{fontSize:17,lineHeight:1.65,opacity:.72}}>
              מרחב אחד לשיחה, זיכרון, למידה, יצירה, כלים ומכשירים —
              עם התקדמות מתועדת במקום הבטחות שלא מומשו.
            </p>
            <div style={{display:'flex',flexWrap:'wrap',gap:8,marginTop:18}}>
              {features.map(([label]) => <span key={label} style={{
                padding:'8px 12px',borderRadius:999,background:'#ffffff0b',
                border:'1px solid #ffffff12',fontSize:12
              }}>{label}</span>)}
            </div>
          </div>
        </div>        <div style={{
          minHeight:680, display:'flex', flexDirection:'column',
          borderRadius:30, border:'1px solid #ffffff14',
          background:'#ffffff08', overflow:'hidden'
        }}>
          <div style={{padding:22,borderBottom:'1px solid #ffffff10'}}>
            <h2 style={{margin:'0 0 6px'}}>לדבר עם אמא</h2>
            <div style={{opacity:.52,fontSize:12}}>
              זיכרון {counts.memory.toLocaleString()} · למידה {counts.learning.toLocaleString()}
            </div>
          </div>
          <div style={{flex:1,padding:18,overflowY:'auto'}}>
            {messages.map((m,i)=><div key={i} style={{
              display:'flex',justifyContent:m.role==='user'?'flex-start':'flex-end',marginBottom:13
            }}>
              <div style={{
                maxWidth:'88%',padding:'13px 15px',borderRadius:19,lineHeight:1.55,
                background:m.role==='system'?'#542d36':m.role==='user'?'#e9e4db':'#ffffff0b',
                color:m.role==='user'?'#111':'#fff'
              }}>{m.text}</div>
            </div>)}
          </div>
          <div style={{padding:14,borderTop:'1px solid #ffffff10',display:'flex',gap:9}}>
            <button onClick={()=>setVoiceOn(v=>!v)} style={{
              border:'1px solid #ffffff12',borderRadius:17,padding:'0 12px',
              background:'#ffffff0b',color:'#fff'
            }}>{voiceOn?'קול פעיל':'קול'}</button>
            <input value={input} disabled={busy} onChange={e=>setInput(e.target.value)}
              onKeyDown={e=>e.key==='Enter'&&send()} placeholder={busy?'אמא עובדת…':'כתוב לאמא…'}
              style={{minWidth:0,flex:1,border:'1px solid #ffffff12',outline:0,
              borderRadius:17,padding:'14px 16px',background:'#ffffff09',color:'#fff',fontSize:16}} />
            <button onClick={send} disabled={busy} style={{
              border:0,borderRadius:17,padding:'0 17px',fontWeight:750
            }}>{busy?'…':'שליחה'}</button>
          </div>
        </div>
      </section>      <section style={{
        maxWidth:1440, margin:'auto', padding:'0 28px 30px',
        display:'grid',gridTemplateColumns:'repeat(6,1fr)',gap:10
      }}>
        {features.map(([label,key])=><div key={key} style={{
          padding:15,borderRadius:22,border:'1px solid #ffffff14',
          background:'#ffffff08'
        }}>
          <b>{label}</b>
          <span style={{display:'block',marginTop:5,opacity:.55,fontSize:12}}>
            {key==='memory'
              ? counts.memory.toLocaleString()+' רשומות'
              : key==='learning'
                ? counts.learning.toLocaleString()+' אירועים'
                : runtime.capabilities?.[key] || 'ממשק מוכן; חיבור אמיתי נדרש'}
          </span>
        </div>)}
      </section>
      <style>{`
        @media(max-width:900px){
          header{padding-left:14px!important;padding-right:14px!important}
          main>section:first-of-type{grid-template-columns:1fr!important;padding-left:14px!important;padding-right:14px!important}
          main>section:last-of-type{grid-template-columns:repeat(2,1fr)!important;padding-left:14px!important;padding-right:14px!important}
        }
      `}</style>
    </main>
  );
}
