const { parentPort } = require('worker_threads');
const EXEC = require('./KERNEL_EXECUTION_LAYER_V2');

parentPort.on('message', (msg) => {
  try {
    const res = EXEC.execute(msg.cmd);
    parentPort.postMessage({
      session: msg.session,
      nodeId: msg.nodeId,
      res
    });
  } catch (e) {
    parentPort.postMessage({
      session: msg.session,
      nodeId: msg.nodeId,
      error: e.message
    });
  }
});
