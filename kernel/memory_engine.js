const fs = require("fs");

const FILE = "./memory.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE));
  } catch {
    return { profile: { name: "אורי", mood: "calm", personality: "neutral" }, memory: [] };
  }
}

function save(mem) {
  fs.writeFileSync(FILE, JSON.stringify(mem, null, 2));
}

function addMemory(mem, value, type="fact") {
  const found = mem.memory.find(m => m.value === value);

  if (found) {
    found.hits++;
    found.weight = Math.min(1, found.weight + 0.1);
    found.lastUsed = Date.now();
  } else {
    mem.memory.push({
      value,
      type,
      weight: 0.5,
      hits: 1,
      created: Date.now(),
      lastUsed: Date.now()
    });
  }
}

module.exports = { load, save, addMemory };
