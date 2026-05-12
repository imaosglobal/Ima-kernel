const fs = require("fs");
const { execSync } = require("child_process");

const MEMORY = "ima_memory.json";
const STATE = "ima_state.json";

function readJSON(path, fallback = []) {
  try {
    const data = JSON.parse(fs.readFileSync(path, "utf-8"));
    return Array.isArray(data) ? data : fallback;
  } catch {
    return fallback;
  }
}

function writeJSON(path, data) {
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
}

function scoreSystem(events) {
  const errors = events.filter(e => e.type === "error").length;
  const requests = events.filter(e => e.type === "request").length;
  if (requests === 0) return 1;
  return 1 - (errors / requests);
}

function decideAction(score) {
  if (score < 0.7) return "REPAIR";
  if (score < 0.9) return "OPTIMIZE";
  return "STABLE";
}

function act(action) {
  try {
    if (action === "REPAIR") {
      execSync("ima restart", { stdio: "ignore", shell: "/data/data/com.termux/files/usr/bin/bash" });
    }
    if (action === "OPTIMIZE") {
      execSync("ima update", { stdio: "ignore", shell: "/data/data/com.termux/files/usr/bin/bash" });
    }
  } catch {}
}

function evolve() {
  const events = readJSON(MEMORY, []);
  const state = {};

  const score = scoreSystem(events);
  const action = decideAction(score);

  state.last_score = score;
  state.last_action = action;
  state.last_evolution = new Date().toString();

  writeJSON(STATE, state);

  act(action);

  console.log("[EVOLUTION]", score, action);
}

module.exports = { evolve };
