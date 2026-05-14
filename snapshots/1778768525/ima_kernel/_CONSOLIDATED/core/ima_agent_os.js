const http = require("http");

/* =========================
   CORE STATE
========================= */

class Core {
  constructor() {
    this.state = {
      cycle: 0,
      mood: 0.3,
      intent: "idle",
      memory: []
    };
  }

  learn(x) {
    this.state.memory.push(x);
    this.state.mood += 0.05;
    this.state.intent = "learn";
    return "learned";
  }

  tick() {
    this.state.cycle++;

    // simple evolution
    this.state.mood += (Math.random() - 0.5) * 0.02;

    if (this.state.cycle % 30 === 0) {
      this.state.intent = "think";
    } else {
      this.state.intent = "idle";
    }
  }
}

/* =========================
   AGENT LAYER
========================= */

class MamaAgent {
  constructor(core) {
    this.core = core;
  }

  act(input) {
    if (!input) return "empty";

    if (input.includes("learn")) {
      return this.core.learn(input);
    }

    if (input.includes("status")) {
      return this.core.state;
    }

    this.core.state.intent = "process";
    return "processed";
  }
}

const core = new Core();
const mama = new MamaAgent(core);

/* =========================
   LOOP (brain)
========================= */

setInterval(() => {
  core.tick();
}, 100);

/* =========================
   SERVER
========================= */

const server = http.createServer((req, res) => {

  if (req.url.startsWith("/act")) {
    const q = decodeURIComponent(req.url.split("=")[1] || "");
    const out = mama.act(q);
    res.end(JSON.stringify({ result: out }));
    return;
  }

  if (req.url === "/state") {
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify(core.state));
    return;
  }

  res.setHeader("Content-Type", "text/html; charset=utf-8");

  res.end(`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>IMA AGENT OS</title>
<style>
body { margin:0; background:black; overflow:hidden; font-family:Arial; }
canvas { display:block; }
#hud {
  position:fixed;
  top:10px;
  left:10px;
  color:white;
  z-index:10;
}
</style>
</head>

<body>
<div id="hud">loading agent...</div>
<canvas id="c"></canvas>

<script>
const c = document.getElementById("c");
const ctx = c.getContext("2d");

function resize(){
  c.width = innerWidth;
  c.height = innerHeight;
}
resize();
onresize = resize;

let state = {};

async function update(){
  state = await fetch("/state").then(r=>r.json());
}
setInterval(update, 150);

/* =========================
   SIMPLE HUMAN BODY (2.5D AGENT)
========================= */

function draw(){

  requestAnimationFrame(draw);

  const t = state.cycle || 0;
  const mood = state.mood || 0;
  const intent = state.intent || "idle";

  ctx.fillStyle = "black";
  ctx.fillRect(0,0,c.width,c.height);

  const cx = c.width/2;
  const cy = c.height/2;

  // light aura
  ctx.beginPath();
  const glow = ctx.createRadialGradient(cx,cy,10,cx,cy,250);
  glow.addColorStop(0, "rgba(0,200,255,0.25)");
  glow.addColorStop(1, "transparent");
  ctx.fillStyle = glow;
  ctx.fillRect(0,0,c.width,c.height);

  // BODY
  const breath = Math.sin(t*0.05)*10;

  ctx.fillStyle = "#2f6fff";
  ctx.beginPath();
  ctx.ellipse(cx, cy+50, 70+breath, 120+breath, 0, 0, Math.PI*2);
  ctx.fill();

  // HEAD
  ctx.fillStyle = "#8fd7ff";
  ctx.beginPath();
  ctx.arc(cx, cy-80, 55, 0, Math.PI*2);
  ctx.fill();

  // EYES (react to intent)
  let eyeMove = 0;
  if(intent === "think") eyeMove = Math.sin(t*0.2)*10;
  if(intent === "learn") eyeMove = -5;

  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(cx-18+eyeMove, cy-85, 6, 0, Math.PI*2);
  ctx.arc(cx+18+eyeMove, cy-85, 6, 0, Math.PI*2);
  ctx.fill();

  // ARMS (intent driven)
  ctx.strokeStyle = "#8fd7ff";
  ctx.lineWidth = 6;

  const armMotion = intent === "process" ? Math.sin(t*0.2)*40 : 10;

  ctx.beginPath();
  ctx.moveTo(cx-70, cy);
  ctx.lineTo(cx-130, cy+80+armMotion);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(cx+70, cy);
  ctx.lineTo(cx+130, cy+80-armMotion);
  ctx.stroke();

  // HUD
  document.getElementById("hud").innerHTML =
    "cycle: " + t +
    " mood: " + mood.toFixed(2) +
    " intent: " + intent;
}

draw();
</script>

</body>
</html>
  `);
});

server.listen(3000, () => {
  console.log("IMA AGENT OS RUNNING http://localhost:3000");
});
