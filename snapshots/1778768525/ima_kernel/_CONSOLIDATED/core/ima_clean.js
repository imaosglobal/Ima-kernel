'use strict';

const STATE = {
  booted: false,
  queue: [],
  history: [],
  tasks: 0
};

function execute(task) {
  if (!task || !task.cmd) return { ok: false, error: 'NO_CMD' };

  if (task.cmd === 'ping') return { ok: true, result: 'pong' };

  if (task.cmd === 'status') {
    return {
      ok: true,
      state: {
        booted: STATE.booted,
        queue: STATE.queue.length,
        tasks: STATE.tasks
      }
    };
  }

  if (task.cmd === 'self_check') {
    return { ok: true, tasks: STATE.tasks };
  }

  return { ok: true, echo: task };
}

function processQueue() {
  while (STATE.queue.length) {
    const task = STATE.queue.shift();
    const res = execute(task);

    STATE.tasks++;
    STATE.history.push({ task, res, ts: Date.now() });
  }
}

function start() {
  if (STATE.booted) return { status: 'already_booted' };

  STATE.booted = true;
  setInterval(processQueue, 100).unref?.();

  return { status: 'booted' };
}

function enqueue(task) {
  STATE.queue.push(task);
  return { queued: true };
}

function health() {
  return {
    booted: STATE.booted,
    queue: STATE.queue.length,
    tasks: STATE.tasks
  };
}

function history() {
  return STATE.history;
}

module.exports = { start, enqueue, health, history };

if (require.main === module) {
  console.log(start());

  enqueue({ cmd: 'ping' });
  enqueue({ cmd: 'status' });
  enqueue({ cmd: 'self_check' });

  setTimeout(() => {
    console.log('HEALTH:', health());
    console.log('HISTORY:', history());
  }, 300);
}
