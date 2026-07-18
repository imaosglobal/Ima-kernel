import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF, OrbitControls, Stage, Html } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/mother_character.glb');
  return <primitive object={scene} />;
}

export default function IMAAvatar() {
  return (
    <div style={{ height: '400px', width: '100%', background: '#0a0a0a' }}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <Suspense fallback={<Html center>טוענת אמת...</Html>}>
          <Stage intensity={0.5}>
            <Model />
          </Stage>
        </Suspense>
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
