const runtime = require("./autonomous_runtime.js");
const kernelState = require("./KERNEL_STATE");

console.log("KERNEL ONLINE - STABLE MODE");

kernelState.updateHeartbeat();

if (runtime && typeof runtime.start === "function") {
  runtime.start();
}
