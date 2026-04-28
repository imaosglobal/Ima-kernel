const http = require("http");

const server = http.createServer((req, res) => {

  res.setHeader("Content-Type", "text/html; charset=utf-8");

  res.end(`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IMA SAFE 3D</title>

<style>
body { margin:0; overflow:hidden; background:black; }
#loading { position:absolute; top:20px; left:20px; color:#0ff; }
</style>

</head>
<body>

<div id="loading">IMA LOADING...</div>

<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0,1.5,4);

const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0xffffff, 1.2));

const light = new THREE.DirectionalLight(0xffffff, 2);
light.position.set(2,3,2);
scene.add(light);

/* SAFE BODY */
const body = new THREE.Group();

const head = new THREE.Mesh(
  new THREE.SphereGeometry(0.5, 32, 32),
  new THREE.MeshStandardMaterial({ color: 0x66ccff })
);
head.position.y = 1.5;

const torso = new THREE.Mesh(
  new THREE.CylinderGeometry(0.6, 0.8, 1.5, 32),
  new THREE.MeshStandardMaterial({ color: 0x2288ff })
);
torso.position.y = 0.3;

body.add(head, torso);
scene.add(body);

function animate(){
  requestAnimationFrame(animate);
  body.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

</script>

</body>
</html>
  `);

});

server.listen(3000, () => {
  console.log("IMA SAFE RUNNING http://localhost:3000");
});
