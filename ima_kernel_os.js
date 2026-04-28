const fs = require("fs");
const path = require("path");

/* ---------------- MEMORY LAYER ---------------- */
const memory = {
  state: {},
  events: []
};

/* ---------------- EVENT BUS ---------------- */
function emit(event, data){
  memory.events.push({ event, data, time: Date.now() });
}

/* ---------------- MODULE LOADER ---------------- */
function loadModules(){
  const modules = [];

  const dirs = [
    "./ima_product/plugins",
    "./ima_product",
    "./ima_core"
  ];

  for(const dir of dirs){
    if(fs.existsSync(dir)){
      modules.push(dir);
    }
  }

  return modules;
}

/* ---------------- BOOT SEQUENCE ---------------- */
function boot(config){

  console.log("🧠 IMA KERNEL INIT");
  console.log("⚙️ Config:", config);

  emit("boot/start", config);

  const modules = loadModules();

  console.log("📦 Loaded modules:", modules);

  memory.state.booted = true;

  emit("boot/complete", {
    modules,
    time: Date.now()
  });

  console.log("✅ IMA OS READY");

  return {
    memory,
    modules
  };
}

/* ---------------- HEALTH CHECK ---------------- */
function health(){
  return {
    status: memory.state.booted ? "healthy" : "not_booted",
    events: memory.events.length
  };
}

module.exports = {
  boot,
  health,
  memory
};
