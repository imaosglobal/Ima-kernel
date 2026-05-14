const { loadMemory, saveMemory } = require("./memory_engine");
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
    const mem = loadMemory();
    const cleaned = cleanMemory(mem);
    saveMemory(cleaned);

    lastHealth = Date.now();

    return {
      status: "ok",
      memorySize: cleaned.memory.length,
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

// זיהוי תקיעות אמיתי
function detectStall() {
  const now = Date.now();
  const diff = now - lastHealth;

  // אם לא הייתה פעילות 60 שניות → חשוד
  return diff > 60000;
}

// restart חכם (רק אם צריך)
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
  detectStall
};
