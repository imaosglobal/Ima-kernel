function loadMemory() {
  const fs = require("fs");
  try {
    return JSON.parse(fs.readFileSync("./memory.json", "utf8"));
  } catch {
    return { memory: [], profile: { personality: "neutral", mood: "calm" } };
  }
}

function saveMemory(mem) {
  const fs = require("fs");
  fs.writeFileSync("./memory.json", JSON.stringify(mem, null, 2));
}

function remember(mem, text) {
  mem.memory.push({ value: text, time: Date.now() });
  if (mem.memory.length > 50) mem.memory.shift();
  return mem;
}

module.exports = { loadMemory, saveMemory, remember };
