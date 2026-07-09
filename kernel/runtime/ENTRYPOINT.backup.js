const kernelState = require("./KERNEL_STATE");

console.log("KERNEL ONLINE - SINGLE SOURCE MODE");

function tick() {
  kernelState.updateHeartbeat();
}

kernelState.updateHeartbeat();
setInterval(tick, 2000);
