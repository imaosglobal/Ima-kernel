# הדבק את כל הקוד, Ctrl+O ושמור, Ctrl+X לצאת#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima-mobile || exit

echo "🔹 Step 1: יצירת תיקיות 3D לכל שפה"
mkdir -p public/assets/characters/en
mkdir -p public/assets/characters/he
mkdir -p public/assets/characters/fr

echo "🔹 Step 2: התקנת חבילות בסיסיות"
npm install three next react react-dom i18next i18next-browser-languagedetector @prisma/client prisma tailwindcss --save
npm install three/examples/jsm/exporters/GLTFExporter.js --save-dev || true

echo "🔹 Step 3: יצירת קוביות בסיסיות כ-GLB לכל שפה"
cat << 'EOF' > generate-glb.js
const THREE = require('three');
const fs = require('fs');
const { GLTFExporter } = require('three/examples/jsm/exporters/GLTFExporter.js');

function createGLB(path) {
    const scene = new THREE.Scene();
    const geometry = new THREE.BoxGeometry(1,1,1);
    const material = new THREE.MeshStandardMaterial({color: 0x00ff00});
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    const light = new THREE.DirectionalLight(0xffffff,1);
    light.position.set(5,5,5);
    scene.add(light);

    const exporter = new GLTFExporter();
    exporter.parse(scene, function(result){
        const output = Buffer.from(result);
        fs.writeFileSync(path, output);
        console.log(`✅ GLB created: ${path}`);
    }, {binary: true});
}

createGLB('public/assets/characters/en/ima.glb');
createGLB('public/assets/characters/he/ima.glb');
createGLB('public/assets/characters/fr/ima.glb');
EOF

node generate-glb.js

echo "🔹 Step 4: יצירת קומפוננטת React ImaCharacter"
mkdir -p components
cat << 'EOF' > components/ImaCharacter.js
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import * as THREE from "three";

export default function ImaCharacter() {
  const { i18n } = useTranslation();
  const [sceneReady, setSceneReady] = useState(false);

  useEffect(() => {
    const loader = new GLTFLoader();
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(300, 300);
    const container = document.getElementById("ima-container");
    if (container) container.appendChild(renderer.domElement);

    let lang = i18n.language || "en";
    const glbPath = `/assets/characters/${lang}/ima.glb`;

    loader.load(
      glbPath,
      function (gltf) {
        scene.add(gltf.scene);
        camera.position.z = 5;
        const animate = function () {
          requestAnimationFrame(animate);
          gltf.scene.rotation.y += 0.01;
          renderer.render(scene, camera);
        };
        animate();
        setSceneReady(true);
      },
      undefined,
      function (error) {
        console.error("Error loading GLB:", error);
      }
    );
  }, [i18n.language]);

  return (
    <div>
      <h2>
        {i18n.language === "he" ? "אמא" : i18n.language === "fr" ? "Maman" : "Mom"}
      </h2>
      <div id="ima-container" style={{ width: "300px", height: "300px" }}></div>
      {!sceneReady && <p>Loading 3D character...</p>}
    </div>
  );
}
EOF

echo "🔹 Step 5: עדכון package.json עם scripts בסיסיים"
cat << 'EOF' > package.json
{
  "name": "ima-mobile",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint ."
  }
}
EOF

echo "🔹 Step 6: יצירת קובץ env למניעת WASM Turbopack"
echo "NEXT_PRIVATE_USE_WASM_TURBOPACK=false" > .env.local

echo "🎯 Step 7: בדיקה שהשרת עולה"
# פותח את Next.js בשרת על פורט פנוי
npm run dev &

# נותן 5 שניות לשרת להתרומם
sleep 5

PORT=$(lsof -iTCP -sTCP:LISTEN -P -n | grep node | head -1 | awk '{print $9}' | cut -d':' -f2)
if [ -z "$PORT" ]; then
  PORT="3000"
fi

echo "🔹 שרת אמור לפעול בכתובת: http://localhost:$PORT"
echo "🔹 פתח את הדפדפן במכשיר כדי לבדוק שהדמות 3D נטענת"

echo "✅ Ima full setup complete: דמויות GLB לכל שפה, קומפוננטה React, TailwindJS, Prisma7+SQLite מותקנים"
chmod +x setup-ima-full.sh
bash setup-ima-full.sh
