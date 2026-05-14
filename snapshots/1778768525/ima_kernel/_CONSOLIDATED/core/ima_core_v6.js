'use strict';

const fs = require('fs');
const path = require('path');

/* =========================
   MEMORY
========================= */

const STORE = path.join(__dirname, 'ima_core_v6_memory.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(STORE, 'utf8'));
  } catch {
    return {
      goals: [],
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

  goals: [],            // multiple active goals
  activeGoal: null
};

/* =========================
   GOALS
========================= */

function createGoal(text) {
  return {
    id: Date.now() + Math.random(),
    goal: text,
    priority: 1,
    progress: 0,
    plan: null,
    done: false
  };
}

/* =========================
   LEARNING SCORE
========================= */

function scoreStep(mem, step) {
  const s = mem.stats.success[step] || 0;
  const f = mem.stats.failure[step] || 0;
  return s - f;
}

/* =========================
   PLANNER
========================= */

const PLANNER = {

  build(goal) {
    return [
      `analyze:${goal}`,
      `prepare:${goal}`,
      `execute:${goal}`,
      `verify:${goal}`
    ];
  },

  attach(goalObj, mem) {
    const steps = this.build(goalObj.goal);

    // sort steps based on learning
    steps.sort((a, b) => scoreStep(mem, b) - scoreStep(mem, a));

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
   SCHEDULER (v6 core)
========================= */

function pickGoal() {
  if (STATE.goals.length === 0) return null;

  // priority + progress bias
  STATE.goals.sort((a, b) => {
    const scoreA = a.priority - a.progress;
    const scoreB = b.priority - b.progress;
    return scoreB - scoreA;
  });

  return STATE.goals[0];
}

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
      const step = task.step;

      const success = Math.random() > 0.2;

      if (success) {
        STATE.mem.stats.success[step] =
          (STATE.mem.stats.success[step] || 0) + 1;
      } else {
        STATE.mem.stats.failure[step] =
          (STATE.mem.stats.failure[step] || 0) + 1;
      }

      save(STATE.mem);

      return { ok: success, step };
    }

    default:
      return { ok: true, echo: task };
  }
}

/* =========================
   LOOP (multi-goal attention)
========================= */

function processQueue() {

  // if no queue tasks → generate from active goal
  if (STATE.queue.length === 0) {

    const goal = pickGoal();
    STATE.activeGoal = goal;

    if (goal) {
      if (!goal.plan) {
        PLANNER.attach(goal, STATE.mem);
      }

      const step = PLANNER.next(goal);

      if (step) {
        STATE.queue.push({ cmd: 'step', step: step.action });

        // progress tracking
        goal.progress += 0.25;
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

    // failure → reduce priority
    if (task.cmd === 'step' && res.ok === false && STATE.activeGoal) {
      STATE.activeGoal.priority = Math.max(0, STATE.activeGoal.priority - 1);
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
    goals: STATE.goals.map(g => ({
      goal: g.goal,
      priority: g.priority,
      progress: g.progress
    })),
    activeGoal: STATE.activeGoal?.goal || null
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

  goal('stabilize system');
  goal('improve memory');
  goal('optimize execution');

  enqueue('ping');

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 1000);
}
