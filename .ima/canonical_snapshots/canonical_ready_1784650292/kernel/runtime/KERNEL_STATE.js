const fs = require("fs");
const path = require("path");

const STATE_FILE = path.join(__dirname, "kernel_state.json");

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE));
  } catch {
    return {
      runtime: "booting",
      lastHeartbeat: 0,
      status: "booting"
    };
  }
}

function save(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function updateHeartbeat() {
  const state = load();
  state.runtime = "alive";
  state.lastHeartbeat = Date.now();
  state.status = "healthy";
  save(state);
}

function getState() {
  return load();
}

module.exports = {
  updateHeartbeat,
  getState
};
