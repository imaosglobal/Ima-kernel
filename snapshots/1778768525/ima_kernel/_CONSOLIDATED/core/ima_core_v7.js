'use strict';

const fs = require('fs');
const path = require('path');

/* =========================
   MEMORY
========================= */

const STORE = path.join(__dirname, 'ima_core_v7_memory.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return {
      goals: [],
      stats: { success: {}, failure: {} }
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

  goals: [],
  activeGoal: null,

  systemLoad: 0.1
};

/* =========================
   GOAL MODEL
========================= */

function createGoal(text) {
  return {
    id: Date.now() + Math.random(),
    goal: text,
    priority: 1,
    progress: 0,
    weight: 1,
    plan: null
  };
}

/* =========================
   REASONING ENGINE (v7 core)
========================= */

const REASONER = {

  scoreGoal(goal, state) {
    // core cognitive scoring function

    const progressPenalty = goal.progress * 0.6;
    const priorityBoost = goal.priority * 1.2;
    const systemPressure = state.systemLoad;

    // stability bias: prefer low-load execution
    const stabilityBias = 1 - systemPressure;

    return (priorityBoost + stabilityBias) - progressPenalty;
  },

  chooseGoal(goals, state) {
    if (goals.length === 0) return null;

    let best = null;
    let bestScore = -Infinity;

    for (const g of goals) {
      const score = this.scoreGoal(g, state);

      if (score > bestScore) {
        bestScore = score;
        best = g;
      }
    }

    return best;
  }
};

/* =========================
   PLANNER
========================= */

const PLANNER = {

  build(goal) {
    return [
      `analyze:${goal}`,
      `structure:${goal}`,
      `execute:${goal}`,
      `validate:${goal}`
    ];
  },

  attach(goalObj, mem) {
    const steps = this.build(goalObj.goal);

    goalObj.plan = {
      steps: steps.map(s => ({ action: s, done: false })),
      pointer: 0
    };
  },

  next(goalObj) {
    if (!goalObj.plan) return null;
    return goalObj.plan.steps[goalObj.plan.pointer++] || null;
  }
};

/* =========================
   EXECUTION
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

function execute(task) {
  if (!task || !task.cmd) return { ok: false };

  switch (task.cmd) {

    case 'ping':
      return { ok: true, result: 'pong' };

    case 'status':
      return {
        ok: true,
        tasks: STATE.tasks,
        goals: STATE.goals.length,
        activeGoal: STATE.activeGoal?.goal || null
      };

    case 'goal': {
      const g = createGoal(task.value);

      STATE.goals.push(g);
      STATE.mem.goals.push(g);

      save(STATE.mem);

      return { ok: true, goal_added: task.value };
    }

    case 'step': {
      const success = Math.random() > 0.2;

      if (success) {
        STATE.mem.stats.success[task.step] =
          (STATE.mem.stats.success[task.step] || 0) + 1;
      } else {
        STATE.mem.stats.failure[task.step] =
          (STATE.mem.stats.failure[task.step] || 0) + 1;
      }

      save(STATE.mem);

      return { ok: success, step: task.step };
    }

    default:
      return { ok: true, echo: task };
  }
}

/* =========================
   COGNITIVE LOOP
========================= */

function processQueue() {

  // update system load (simple feedback simulation)
  STATE.systemLoad = STATE.queue.length / 10;

  if (STATE.queue.length === 0) {

    // COGNITIVE STEP: choose goal, not just FIFO
    const selected = REASONER.chooseGoal(STATE.goals, STATE);

    STATE.activeGoal = selected;

    if (selected) {

      if (!selected.plan) {
        PLANNER.attach(selected, STATE.mem);
      }

      const step = PLANNER.next(selected);

      if (step) {
        STATE.queue.push({ cmd: 'step', step: step.action });

        selected.progress += 0.2;
      }
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

    // feedback → adjust priority dynamically
    if (task.cmd === 'step' && res.ok === false && STATE.activeGoal) {
      STATE.activeGoal.priority += 0.5;
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

function goal(text) {
  enqueue('goal:' + text);
}

function health() {
  return {
    booted: STATE.booted,
    queue: STATE.queue.length,
    tasks: STATE.tasks,
    systemLoad: STATE.systemLoad,
    activeGoal: STATE.activeGoal?.goal || null,
    goals: STATE.goals.map(g => ({
      goal: g.goal,
      priority: g.priority,
      progress: g.progress
    }))
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

  goal('stabilize kernel');
  goal('improve reasoning');
  goal('optimize flow');

  enqueue('ping');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 1200);
}
