import React, { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, Float, Html, useGLTF } from '@react-three/drei';

const MODEL_URL = '/Ima-kernel/mother_character.glb';

function MotherModel({ scale = 1 }) {
  const group = useRef(null);
  const { scene } = useGLTF(MODEL_URL);
  useFrame((state, delta) => {
    if (!group.current) return;
    group.current.rotation.y += delta * 0.08;
    group.current.position.y = Math.sin(state.clock.elapsedTime * 0.7) * 0.035;
  });
  return (
    <group ref={group} scale={scale}>
      <Float speed={1.1} rotationIntensity={0.08} floatIntensity={0.18}>
        <primitive object={scene} />
      </Float>
    </group>
  );
}

function HolographicRings() {
  return (
    <group rotation={[Math.PI / 2.7, 0, 0]}>
      <mesh>
        <torusGeometry args={[1.72, 0.012, 12, 96]} />
        <meshBasicMaterial color="#d9a6b0" transparent opacity={0.55} />
      </mesh>
      <mesh rotation={[0, 0, Math.PI / 2]}>
        <torusGeometry args={[1.46, 0.008, 12, 96]} />
        <meshBasicMaterial color="#b88c98" transparent opacity={0.4} />
      </mesh>
    </group>
  );
}

export default function IMA3DCompanion({ mode = 'hero', lang = 'en', onOpenChat, label, interactive = true }) {
  const compact = mode === 'floating' || mode === 'compact';
  const standalone = mode === 'standalone';
  const text = label || (lang === 'he' ? 'אמא — לפתיחת צ׳ט' : 'IMA — open chat');

  const open = () => {
    if (onOpenChat) onOpenChat();
    else if (!standalone) window.location.href = '/Ima-kernel/?chat=1';
  };

  return (
    <button
      type="button"
      className={`ima-3d-companion ima-3d-${mode}`}
      aria-label={text}
      onClick={open}
      onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } }}
    >
      <span className="ima-3d-aura" aria-hidden="true" />
      <span className="ima-3d-canvas" aria-hidden="true">
        <Canvas
          dpr={[1, compact ? 1.35 : 1.75]}
          camera={{ position: [0, 0.55, compact ? 4.8 : 5.2], fov: 35 }}
          gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
          fallback={<span className="ima-3d-fallback">אמא</span>}
        >
          <ambientLight intensity={1.4} />
          <directionalLight position={[3, 4, 4]} intensity={2.1} />
          <pointLight position={[-3, 1, 2]} intensity={1.2} color="#d99aa5" />
          <pointLight position={[2, -1, -2]} intensity={0.8} color="#a8c7ff" />
          <HolographicRings />
          <Suspense fallback={<Html center><span className="ima-3d-loading">IMA</span></Html>}>
            <MotherModel scale={compact ? 0.82 : standalone ? 1.15 : 1} />
            <Environment preset="studio" />
          </Suspense>
        </Canvas>
      </span>
      {!compact && <span className="ima-3d-caption">{lang === 'he' ? 'אמא' : 'IMA'} <small>{lang === 'he' ? 'נגיעה לפתיחת שיחה' : 'Tap to talk'}</small></span>}
    </button>
  );
}

useGLTF.preload(MODEL_URL);
