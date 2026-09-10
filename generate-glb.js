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
