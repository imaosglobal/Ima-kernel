const fs = require("fs");

const FILE = "./memory.json";

// ---------- LOAD ----------
function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE));
  } catch {
    return {
      profile: { name: "אורי", mood: "calm", personality: "neutral" },
      memory: []
    };
  }
}

// ---------- SAVE ----------
function save(mem) {
  fs.writeFileSync(FILE, JSON.stringify(mem, null, 2));
}

// ---------- ADD MEMORY ----------
function addMemory(mem, value, type = "fact") {
  if (!mem.memory) mem.memory = [];

  const now = Date.now();

  const found = mem.memory.find(m =>
    m.value === value && m.type === type
  );

  if (found) {
    found.hits = (found.hits || 1) + 1;
    found.weight = Math.min(1, (found.weight || 0.5) + 0.05);
    found.lastUsed = now;
    return;
  }

  mem.memory.push({
    value,
    type,
    weight: 0.5,
    hits: 1,
    created: now,
    lastUsed: now
  });
}

// ---------- DECAY ----------
function decayMemory(mem) {
  const now = Date.now();
  const DAY = 1000 * 60 * 60 * 24;

  mem.memory = mem.memory
    .map(m => {
      const ageDays = (now - m.created) / DAY;
      m.weight = Math.max(0.1, m.weight - ageDays * 0.01);
      return m;
    })
    .filter(m => m.weight > 0.15);

  return mem;
}

// ---------- DEDUP ----------
function deduplicate(mem) {
  const seen = new Set();

  mem.memory = mem.memory.filter(m => {
    const key = m.value + "::" + m.type;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  return mem;
}

module.exports = {
  load,
  save,
  addMemory,
  decayMemory,
  deduplicate
};
