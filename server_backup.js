const http = require("http");
const core = require("./ima_core");

core.start();

const server = http.createServer((req, res) => {

  if (req.url.startsWith("/learn")) {
    const q = decodeURIComponent(req.url.split("=")[1] || "");
    core.learn(q);
    res.end("ok");
    return;
  }

  if (req.url === "/state") {
    res.setHeader("Content-Type","application/json");
    res.end(JSON.stringify(core.state));
    return;
  }

  res.setHeader("Content-Type","text/html; charset=utf-8");

  res.end(`
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>IMA FULL BODY</title>
<style>
body { margin:0; overflow:hidden; background:black; }
canvas { display:block; }
</style>
</head>
<body>

<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

/* ===== SCENE ===== */
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, innerWidth/innerHeight, 0.1, 1000);
camera.position.z = 6;

const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

/* LIGHT */
const light = new THREE.PointLight(0x66ccff, 2);
light.position.set(5,5,5);
scene.add(light);

const mat = new THREE.MeshStandardMaterial({ color:0x3399ff });

/* ===== BODY ===== */
const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.7,0.9,2.2,24), mat);
scene.add(torso);

const head = new THREE.Mesh(new THREE.SphereGeometry(0.55,32,32), mat);
head.position.y = 1.8;
scene.add(head);

/* ===== LIMBS ===== */
function arm(x){
  const u = new THREE.Mesh(new THREE.BoxGeometry(0.25,0.8,0.25),mat);
  const l = new THREE.Mesh(new THREE.BoxGeometry(0.22,0.8,0.22),mat);

  u.position.set(x,0.5,0);
  l.position.set(x,-0.3,0);

  scene.add(u); scene.add(l);
  return {u,l};
}

function leg(x){
  const u = new THREE.Mesh(new THREE.BoxGeometry(0.3,0.9,0.3),mat);
  const l = new THREE.Mesh(new THREE.BoxGeometry(0.28,0.9,0.28),mat);

  u.position.set(x,-1.8,0);
  l.position.set(x,-2.7,0);

  scene.add(u); scene.add(l);
  return {u,l};
}

const LArm = arm(-1.1);
const RArm = arm(1.1);
const LLeg = leg(-0.4);
const RLeg = leg(0.4);

/* ===== STATE ===== */
let state = {cycle:0,mood:0};

async function update(){
  state = await fetch("/state").then(r=>r.json());
}
setInterval(update,200);

/* ===== LOOP ===== */
function animate(){
  requestAnimationFrame(animate);

  const t = state.cycle * 0.02;
  const mood = state.mood || 0;

  const breath = Math.sin(t) * 0.1;

  torso.scale.y = 1 + breath;

  head.position.y = 1.8 + Math.sin(t*2)*0.05;
  head.scale.set(1+mood*0.05,1+mood*0.05,1+mood*0.05);

  LArm.u.rotation.z = Math.sin(t)*0.6;
  RArm.u.rotation.z = -Math.sin(t)*0.6;
  LArm.l.rotation.z = Math.sin(t+1)*0.4;
  RArm.l.rotation.z = -Math.sin(t+1)*0.4;

  LLeg.u.rotation.x = Math.sin(t)*0.6;
  RLeg.u.rotation.x = -Math.sin(t)*0.6;
  LLeg.l.rotation.x = Math.sin(t+1)*0.4;
  RLeg.l.rotation.x = -Math.sin(t+1)*0.4;

  renderer.render(scene,camera);
}

animate();
</script>

</body>
</html>
  `);
});

server.listen(3000, () => {
  console.log("IMA FULL BODY RUNNING : http://localhost:3000");
});
