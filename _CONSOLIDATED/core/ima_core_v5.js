'use strict';

const fs = require('fs');
const path = require('path');

/* =========================
   MEMORY
========================= */

const STORE = path.join(__dirname, 'ima_core_v5_memory.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return {
      goals: [],
      plans: [],
      stats: {
        success: {},
        failure: {}
      }
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
  activePlan: null
};

/* =========================
   ADAPTIVE PLANNER (v5 core)
========================= */

const PLANNER = {

  basePlan(goal) {
    return [
      `analyze:${goal}`,
      `prepare:${goal}`,
      `execute:${goal}`,
      `verify:${goal}`
    ];
  },

  adaptivePlan(goal, mem) {
    const stats = mem.stats;

    // simple heuristic learning
    const failureRate = (step) => {
      const f = stats.failure[step] || 0;
      const s = stats.success[step] || 0;
      return f / (s + f + 1);
    };

    let steps = this.basePlan(goal);

    // reorder: prioritize more successful steps
    steps.sort((a, b) => {
      return failureRate(a) - failureRate(b);
    });

    return {
      id: Date.now(),
      goal,
      steps: steps.map(s => ({ action: s, done: false })),
      pointer: 0,
      failed: false
    };
  },

  next(plan) {
    if (!plan) return null;
    return plan.steps[plan.pointer++] || null;
  }
};

/* =========================
   LEARNING ENGINE
========================= */

function learn(mem, step, success) {
  const key = step;

  if (success) {
    mem.stats.success[key] = (mem.stats.success[key] || 0) + 1;
  } else {
    mem.stats.failure[key] = (mem.stats.failure[key] || 0) + 1;
  }
}

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
      STATE.activePlan = PLANNER.adaptivePlan(task.value, STATE.mem);

      STATE.mem.plans.push(STATE.activePlan);
      save(STATE.mem);

      return { ok: true, plan_created: task.value };

    case 'step': {
      const step = task.step;

      // simulate execution outcome
      const success = Math.random() > 0.15;

      learn(STATE.mem, step, success);

      save(STATE.mem);

      return {
        ok: success,
        step,
        success
      };
    }

    default:
      return { ok: true, echo: task };
  }
}

/* =========================
   LOOP
========================= */

function processQueue() {

  // if no queue tasks → pull next step from plan
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

    // replanning logic
    if (task.cmd === 'step' && res.success === false) {
      STATE.activePlan.failed = true;

      // regenerate plan dynamically
      STATE.activePlan = PLANNER.adaptivePlan(
        STATE.activePlan.goal,
        STATE.mem
      );
    }
  }
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
    plan: STATE.activePlan
      ? {
          goal: STATE.activePlan.goal,
          pointer: STATE.activePlan.pointer,
          steps: STATE.activePlan.steps
        }
      : null,
    learning: STATE.mem.stats
  };
}

function history() {
  return STATE.history.slice(-30);
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

  goal('build resilient system');
  enqueue('ping');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 800);
}
