
const fs = require("fs");

const LOG_FILE = "/data/data/com.termux/files/home/ima_core/kernel/brain_memory.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(LOG_FILE, "utf8"));
  } catch {
    return [];
  }
}

function save(entry) {
  const data = load();
  data.push({
    ...entry,
    ts: Date.now()
  });

  fs.writeFileSync(LOG_FILE, JSON.stringify(data, null, 2));
}

function getAll() {
  return load();
}

module.exports = { save, getAll };

