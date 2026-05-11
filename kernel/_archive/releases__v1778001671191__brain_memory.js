
const fs = require("fs");

const FILE = "/data/data/com.termux/files/home/ima_core/kernel/brain_memory.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE, "utf8"));
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

  fs.writeFileSync(FILE, JSON.stringify(data, null, 2));
}

function last(n = 20) {
  const data = load();
  return data.slice(-n);
}

module.exports = { save, last };

