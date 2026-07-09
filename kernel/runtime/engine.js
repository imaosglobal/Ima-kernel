const fs = require("fs");

const STATE_FILE = "./kernel/state.json";

let state = { modules: {} };

function load() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      state = JSON.parse(fs.readFileSync(STATE_FILE));
    }
  } catch {
    state = { modules: {} };
  }
}

function save() {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function validate() {
  if (!state || typeof state !== "object") {
    state = { modules: {} };
  }
  if (!state.modules) {
    state.modules = {};
  }
}

function boot() {
  load();
  validate();
  console.log("[ENGINE] boot OK | modules:", Object.keys(state.modules).length);
}

function status() {
  validate();
  return {
    ok: true,
    modules: state.modules,
    count: Object.keys(state.modules).length,
    valid: true,
    ts: Date.now()
  };
}

function enable(name) {
  validate();
  state.modules[name] = {
    enabled: true,
    createdAt: Date.now()
  };
  save();
  return { ok: true, enabled: name };
}

function disable(name) {
  validate();
  if (state.modules[name]) {
    state.modules[name].enabled = false;
    save();
  }
  return { ok: true, disabled: name };
}

function reload(name) {
  validate();
  if (state.modules[name]) {
    state.modules[name].reloadedAt = Date.now();
    save();
  }
  return { ok: true, reloaded: name };
}

module.exports = { boot, status, enable, disable, reload };
