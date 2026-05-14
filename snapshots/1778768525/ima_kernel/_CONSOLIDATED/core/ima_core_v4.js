'use strict';

const fs = require('fs');
const path = require('path');

/* =========================
   MEMORY
========================= */

const STORE = path.join(__dirname, 'ima_core_v4_memory.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return { goals: [], plans: [], history: [] };
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
  tasks: 0,
  history: [],
  mem: load(),
  activePlan: null
};

/* =========================
   PLANNER (v4 core)
========================= */

const PLANNER = {
  createPlan(goal) {
    // deterministic decomposition (simple but structured)

    const baseSteps = [
      `analyze:${goal}`,
      `prepare:${goal}`,
      `execute:${goal}`,
      `verify:${goal}`
    ];

    return {
      id: Date.now(),
      goal,
      steps: baseSteps.map((s, i) => ({
        id: i,
        action: s,
        done: false
      })),
      pointer: 0
    };
  },

  next(plan) {
    if (!plan) return null;

    const step = plan.steps[plan.pointer];
    if (!step) return null;

    plan.pointer++;
    return step;
  }
};

/* =========================
   BRAIN
========================= */

const BRAIN = {
  decide(input) {
    if (!input) return { cmd: 'status' };

    if (typeof input === 'string') {
      if (input === 'ping') return { cmd: 'ping' };
      if (input === 'status') return { cmd: 'status' };

      if (input.startsWith('goal:')) {
        return { cmd: 'goal', value: input.slice(5) };
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
        tasks: STATE.tasks,
        hasPlan: !!STATE.activePlan
      };

    case 'goal':
      STATE.activePlan = PLANNER.createPlan(task.value);

      STATE.mem.plans.push(STATE.activePlan);
      save(STATE.mem);

      return { ok: true, plan_created: task.value };

    case 'step':
      return { ok: true, step: task.step };

    case 'echo':
      return { ok: true, echo: task };

    default:
      return { ok: false };
  }
}

/* =========================
   LOOP (planner-driven)
========================= */

function processQueue() {
  // If no queue tasks, run planner
  if (!STATE.queue.length && STATE.activePlan) {
    const step = PLANNER.next(STATE.activePlan);

    if (step) {
      STATE.queue.push({ cmd: 'step', step: step.action });
    }
  }

  while (STATE.queue.length) {
    const task = STATE.queue.shift();
    const res = execute(task);

    STATE.tasks++;

    STATE.history.push({
      task,
      res,
      ts: Date.now()
    });

    // mark step done if part of plan
    if (STATE.activePlan && task.cmd === 'step') {
      const idx = STATE.activePlan.pointer - 1;
      if (STATE.activePlan.steps[idx]) {
        STATE.activePlan.steps[idx].done = true;
      }
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

  return { status: 'booted' };
}

function enqueue(input) {
  const task = BRAIN.decide(input);
  STATE.queue.push(task);
  return { queued: true };
}

function goal(g) {
  enqueue('goal:' + g);
}

function health() {
  return {
    booted: STATE.booted,
    queue: STATE.queue.length,
    tasks: STATE.tasks,
    activePlan: STATE.activePlan
      ? {
          goal: STATE.activePlan.goal,
          progress:
            STATE.activePlan.steps.filter(s => s.done).length /
            STATE.activePlan.steps.length
        }
      : null
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
   CLI TEST
========================= */

if (require.main === module) {
  console.log(start());

  goal('build stable system');
  enqueue('ping');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 500);
}
