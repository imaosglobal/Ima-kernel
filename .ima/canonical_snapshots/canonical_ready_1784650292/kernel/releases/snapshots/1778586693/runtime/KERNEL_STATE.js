const fs = require("fs");

const STATE_FILE = "./logs/kernel_state.json";

function load() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE));
  } catch {
    return { runtime: "booting", lastHeartbeat: 0, status: "booting" };
  }
}

let state = load();

function persist() {
  fs.mkdirSync("./logs", { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function updateHeartbeat() {
  state.runtime = "alive";
  state.lastHeartbeat = Date.now();
  state.status = "healthy";
  persist();
}

function getState() {
  return load(); // תמיד אמת מהדיסק
}

module.exports = {
  state,
  updateHeartbeat,
  getState
};
