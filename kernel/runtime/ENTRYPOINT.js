const kernelState = require("./KERNEL_STATE");
const runtime = require("./autonomous_runtime");

console.log("KERNEL ONLINE - FIXED STATE MODE");

kernelState.updateHeartbeat();

if (runtime && runtime.start) {
  runtime.start();
}

setInterval(() => {
  kernelState.updateHeartbeat();
}, 2000);
