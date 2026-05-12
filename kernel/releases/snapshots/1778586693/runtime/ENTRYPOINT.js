const kernelState = require("./KERNEL_STATE");
const runtime = require("./autonomous_runtime");

console.log("KERNEL ONLINE - FILE STATE MODE");

function tick() {
  kernelState.updateHeartbeat();
}

kernelState.updateHeartbeat();

if (runtime?.start) runtime.start();

setInterval(tick, 2000);
