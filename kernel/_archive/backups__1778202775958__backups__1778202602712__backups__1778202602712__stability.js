const { load, save } = require("./kernel/memory_engine");
const { decayMemory, deduplicate } = require("./kernel/memory_engine");
const { execSync } = require("child_process");

let lastHealth = Date.now();

function cleanMemory(mem) {
  if (!mem.memory) mem.memory = [];

  const seen = new Set();
  mem.memory = mem.memory.filter(item => {
    const key = item.value + ":" + item.type;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  return mem;
}

function healthCheck() {
  try {
    let mem = load();

    mem = cleanMemory(mem);
    mem = decayMemory(mem);
    mem = deduplicate(mem);

    save(mem);

    lastHealth = Date.now();

    return {
      status: "ok",
      memorySize: mem.memory.length,
      heartbeat: lastHealth
    };
  } catch (e) {
    return {
      status: "error",
      error: e.message,
      heartbeat: lastHealth
    };
  }
}

function detectStall() {
  return (Date.now() - lastHealth) > 60000;
}

function smartRecover() {
  if (!detectStall()) return { skipped: true };

  try {
    execSync("pm2 restart ima-kernel");
    return { recovered: true };
  } catch (e) {
    return { recovered: false, error: e.message };
  }
}

module.exports = {
  healthCheck,
  smartRecover,
  cleanMemory,
  decayMemory,
  deduplicate,
  detectStall
};
