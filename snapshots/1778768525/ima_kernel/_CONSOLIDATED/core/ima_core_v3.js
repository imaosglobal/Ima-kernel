'use strict';

const fs = require('fs');
const path = require('path');

/* =========================
   MEMORY
========================= */

const STORE = path.join(__dirname, 'ima_core_v3_memory.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return {
      tasks: [],
      goals: []
    };
  }
}

function save(mem) {
  try {
    fs.writeFileSync(STORE, JSON.stringify(mem, null, 2));
  } catch {}
}

/* =========================
   STATE
========================= */

const STATE = {
  booted: false,
  queue: [],
  history: [],
  tasks: 0,
  mem: load(),
  currentGoal: null
};

/* =========================
   GOALS LAYER (v3)
========================= */

const GOALS = {
  set(goal) {
    STATE.currentGoal = {
      id: Date.now(),
      goal,
      progress: 0
    };

    STATE.mem.goals.push(STATE.currentGoal);
    save(STATE.mem);
  },

  updateProgress(delta) {
    if (!STATE.currentGoal) return;

    STATE.currentGoal.progress += delta;

    if (STATE.currentGoal.progress >= 100) {
      STATE.currentGoal.done = true;
    }

    save(STATE.mem);
  }
};

/* =========================
   BRAIN (decision → plan)
========================= */

const BRAIN = {
  decide(input) {
    if (!input) return { cmd: 'status' };

    if (typeof input === 'string') {
      if (input === 'ping') return { cmd: 'ping' };
      if (input === 'status') return { cmd: 'status' };
      if (input === 'self_check') return { cmd: 'self_check' };

      // goal commands
      if (input.startsWith('goal:')) {
        return { cmd: 'set_goal', value: input.slice(5) };
      }
    }

    return { cmd: 'echo', input };
  }
};

/* =========================
   EXECUTION
========================= */

function execute(task) {
  if (!task || !task.cmd) return { ok: false };

  switch (task.cmd) {

    case 'ping':
      return { ok: true, result: 'pong' };

    case 'status':
      return {
        ok: true,
        booted: STATE.booted,
        queue: STATE.queue.length,
        tasks: STATE.tasks,
        goal: STATE.currentGoal
      };

    case 'self_check':
      return {
        ok: true,
        tasks: STATE.tasks,
        goals: STATE.mem.goals.length
      };

    case 'set_goal':
      GOALS.set(task.value);
      return { ok: true, goal_set: task.value };

    case 'echo':
      return { ok: true, echo: task };

    default:
      return { ok: false, error: 'UNKNOWN_CMD' };
  }
}

/* =========================
   LOOP
========================= */

function processQueue() {
  while (STATE.queue.length) {
    const task = STATE.queue.shift();
    const res = execute(task);

    STATE.tasks++;

    STATE.history.push({
      task,
      res,
      ts: Date.now()
    });

    // feedback loop: reward progress
    if (STATE.currentGoal && res.ok) {
      GOALS.updateProgress(5);
    }
  }

  save(STATE.mem);
}

/* =========================
   API
========================= */

function start() {
  if (STATE.booted) return { status: 'already_booted' };

  STATE.booted = true;

  setInterval(processQueue, 100).unref?.();

  return {
    status: 'booted',
    goals: STATE.mem.goals.length
  };
}

function enqueue(input) {
  const task = BRAIN.decide(input);
  STATE.queue.push(task);
  return { queued: true };
}

function goal(input) {
  enqueue('goal:' + input);
}

function health() {
  return {
    booted: STATE.booted,
    queue: STATE.queue.length,
    tasks: STATE.tasks,
    currentGoal: STATE.currentGoal
  };
}

function history() {
  return STATE.history.slice(-50);
}

/* =========================
   EXPORT
========================= */

module.exports = {
  start,
  enqueue,
  goal,
  health,
  history
};

/* =========================
   CLI
========================= */

if (require.main === module) {
  console.log(start());

  goal('build stability');
  enqueue('ping');
  enqueue('self_check');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 400);
}
