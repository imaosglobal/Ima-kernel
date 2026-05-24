const fs = require("fs");
const path = require("path");

const FILE = process.env.HOME + "/ima_kernel/kernel/cloud/memory.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE, "utf8"));
  } catch {
    return { history: [], lastSync: 0 };
  }
}

function save(data) {
  fs.writeFileSync(FILE, JSON.stringify(data, null, 2));
}

function add(entry) {
  const m = load();
  m.history.push({
    time: Date.now(),
    entry
  });

  m.lastSync = Date.now();

  save(m);
}

module.exports = { load, save, add };
