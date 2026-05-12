const kernelState = require("../runtime/KERNEL_STATE");

function start() {
  console.log("RUNTIME ACTIVE");

  setInterval(() => {
    kernelState.updateHeartbeat();
    console.log("HEARTBEAT", new Date().toISOString());
  }, 2000);
}

module.exports = { start };
