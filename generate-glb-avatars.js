const THREE = require('three');
const fs = require('fs');
const { GLTFExporter } = require('three/examples/jsm/exporters/GLTFExporter.js');

const avatars = {
  en: { color: 0xFFDAB9, name: "Mom" },
  he: { color: 0xF5DEB3, name: "אמא" },
  fr: { color: 0xFFE4C4, name: "Maman" }
};

function createAvatar(lang, color) {
    const scene = new THREE.Scene();
    const geometry = new THREE.CapsuleGeometry(0.5,1.2,4,8);
    const material = new THREE.MeshStandardMaterial({ color: color });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    const light = new THREE.DirectionalLight(0xffffff,1);
    light.position.set(5,5,5);
    scene.add(light);

    const exporter = new GLTFExporter();
    exporter.parse(scene, function(result){
        const output = Buffer.from(result);
        const path = `public/assets/characters/${lang}/ima.glb`;
        fs.writeFileSync(path, output);
        console.log(`✅ GLB created for ${lang}: ${path}`);
    }, { binary: true });
}

for (const [lang, data] of Object.entries(avatars)) {
    createAvatar(lang, data.color);
}
