'use strict';

/* =========================
   IMA CORE v2 (SINGLE FILE)
   - deterministic runtime
   - brain layer
   - memory persistence
   - self-heal loop
   - no cluster / no IPC
========================= */

const fs = require('fs');
const path = require('path');

/* ---------------- MEMORY ---------------- */

const STORE = path.join(__dirname, 'ima_core_v2_memory.json');

function loadMemory() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return { tasks: [], state: {} };
  }
}

function saveMemory(mem) {
  try {
    fs.writeFileSync(STORE, JSON.stringify(mem, null, 2));
  } catch {}
}

/* ---------------- STATE ---------------- */

const STATE = {
  booted: false,
  queue: [],
  history: [],
  tasks: 0,
  lastHeal: 0,
  mem: loadMemory()
};

/* ---------------- BRAIN ---------------- */

const BRAIN = {
  decide(input) {
    if (!input) return { cmd: 'status' };

    if (typeof input === 'string') {
      if (input === 'ping') return { cmd: 'ping' };
      if (input === 'status') return { cmd: 'status' };
      if (input === 'self_check') return { cmd: 'self_check' };
    }

    return { cmd: 'echo', input };
  }
};

/* ---------------- EXECUTION ---------------- */

function execute(task) {
  if (!task || !task.cmd) return { ok: false, error: 'NO_CMD' };

  switch (task.cmd) {
    case 'ping':
      return { ok: true, result: 'pong' };

    case 'status':
      return {
        ok: true,
        state: {
          booted: STATE.booted,
          queue: STATE.queue.length,
          tasks: STATE.tasks
        }
      };

    case 'self_check':
      return {
        ok: true,
        tasks: STATE.tasks,
        memoryTasks: STATE.mem.tasks.length
      };

    case 'echo':
      return { ok: true, echo: task };

    default:
      return { ok: false, error: 'UNKNOWN_CMD' };
  }
}

/* ---------------- CORE LOOP ---------------- */

function processQueue() {
  while (STATE.queue.length) {
    const task = STATE.queue.shift();
    const res = execute(task);

    STATE.tasks++;

    const record = {
      task,
      res,
      ts: Date.now()
    };

    STATE.history.push(record);
    STATE.mem.tasks.push(record);

    if (STATE.mem.tasks.length > 200) {
      STATE.mem.tasks = STATE.mem.tasks.slice(-200);
    }
  }

  saveMemory(STATE.mem);
}

/* ---------------- SELF HEAL ---------------- */

function heal() {
  const now = Date.now();
  if (now - STATE.lastHeal < 2000) return;

  STATE.lastHeal = now;

  // repair queue stuck state
  if (STATE.booted && STATE.queue.length > 1000) {
    STATE.queue = STATE.queue.slice(-100);
  }

  saveMemory(STATE.mem);
}

/* ---------------- API ---------------- */

function start() {
  if (STATE.booted) return { status: 'already_booted' };

  STATE.booted = true;

  setInterval(processQueue, 100).unref?.();
  setInterval(heal, 2000).unref?.();

  return {
    status: 'booted',
    memoryLoaded: STATE.mem.tasks.length
  };
}

function enqueue(input) {
  const task = BRAIN.decide(input);
  STATE.queue.push(task);
  return { queued: true, size: STATE.queue.length };
}

function health() {
  return {
    booted: STATE.booted,
    queue: STATE.queue.length,
    tasks: STATE.tasks,
    memory: STATE.mem.tasks.length
  };
}

function history() {
  return STATE.history.slice(-50);
}

/* ---------------- EXPORT ---------------- */

module.exports = {
  start,
  enqueue,
  health,
  history
};

/* ---------------- CLI ---------------- */

if (require.main === module) {
  console.log(start());

  enqueue('ping');
  enqueue('status');
  enqueue('self_check');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 300);
}
