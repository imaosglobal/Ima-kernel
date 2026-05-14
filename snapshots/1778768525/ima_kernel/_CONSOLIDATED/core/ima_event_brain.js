const fs = require("fs");
const { EventEmitter } = require("events");

/* ---------- SAFE LOAD ---------- */
function load(p, fb){
  try { return JSON.parse(fs.readFileSync(p)); }
  catch { return fb; }
}

function save(p, d){
  fs.writeFileSync(p, JSON.stringify(d,null,2));
}

const MEMORY_FILE = "./ima_memory.json";
const STATE_FILE = "./ima_state.json";

/* ---------- SAFE STATE ---------- */
let memory = load(MEMORY_FILE, { events: [] });
if(!memory.events) memory.events = [];

let state = load(STATE_FILE, { mode: "stable" });

const bus = new EventEmitter();

/* ---------- BRAIN ---------- */
function brain(event){
  return `processed: ${event.type}`;
}

/* ---------- MEMORY SAFE ---------- */
function remember(event, response){
  if(!memory.events) memory.events = [];

  memory.events.push({
    event,
    response,
    time: Date.now()
  });

  if(memory.events.length > 200){
    memory.events.shift();
  }
}

/* ---------- EVOLUTION ---------- */
function evolve(){
  const size = memory.events.length;

  if(size > 30) state.mode = "adaptive";
  if(size > 80) state.mode = "learning";
}

/* ---------- PERSIST ---------- */
function persist(){
  save(MEMORY_FILE, memory);
  save(STATE_FILE, state);
}

/* ---------- EVENTS ---------- */
bus.on("event", (event)=>{
  const res = brain(event);

  remember(event, res);
  evolve();
  persist();

  console.log("📡", event.type, "=>", res);
  console.log("🧠 MODE:", state.mode);
});

/* ---------- LOOP ---------- */
setInterval(()=>{
  bus.emit("event", { type: "tick", time: Date.now() });
}, 2000);

console.log("🧠 IMA EVENT BRAIN RUNNING");
