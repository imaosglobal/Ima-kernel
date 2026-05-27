const core = require("./memory");

function load() {
  const m = core.load();
  if (!m.history) m.history = [];
  return { memory: m.history, lastSync: m.lastSync };
}

function save(mem) {
  core.save({
    history: mem.memory || [],
    lastSync: Date.now()
  });
}

function addMemory(mem, entry, type) {
  if (!mem.memory) mem.memory = [];
  mem.memory.push({
    time: Date.now(),
    entry,
    type
  });
}

module.exports = { load, save, addMemory };
