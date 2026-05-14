const fs = require('fs');
const path = require('path');

const LOG_PATH = path.join(__dirname, 'kernel_event_log.jsonl');

function append(event) {
  fs.appendFileSync(LOG_PATH, JSON.stringify(event) + '\n');
}

function readAll() {
  if (!fs.existsSync(LOG_PATH)) return [];
  return fs.readFileSync(LOG_PATH, 'utf-8')
    .split('\n')
    .filter(Boolean)
    .map(l => JSON.parse(l));
}

// -------------------------
// WRITE EVENT
// -------------------------
function logRequest(cmd, meta = {}) {
  const event = {
    type: 'REQUEST',
    ts: Date.now(),
    cmd,
    meta
  };
  append(event);
  return event;
}

// -------------------------
// WRITE RESULT
// -------------------------
function logResult(nodeId, result, status) {
  const event = {
    type: 'RESULT',
    ts: Date.now(),
    nodeId,
    status,
    result
  };
  append(event);
  return event;
}

// -------------------------
// REPLAY ENGINE
// -------------------------
function replay(handler) {
  const events = readAll();

  const state = {
    executed: 0,
    failed: 0,
    results: []
  };

  for (const e of events) {

    if (e.type === 'REQUEST') {
      try {
        const res = handler(e.cmd);

        state.executed++;

        state.results.push({
          cmd: e.cmd,
          res
        });

      } catch (err) {
        state.failed++;
      }
    }
  }

  return state;
}

// -------------------------
// SNAPSHOT
// -------------------------
function snapshot() {
  return {
    events: readAll().length
  };
}

module.exports = {
  logRequest,
  logResult,
  replay,
  snapshot
};
