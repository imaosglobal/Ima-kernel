const { updateHeartbeat } = require("./KERNEL_STATE");
const { healAll } = require("./KERNEL_SELF_HEAL");

console.log("KERNEL ONLINE - SELF HEAL ENABLED");

// heartbeat loop
setInterval(() => {
  try {
    updateHeartbeat();
  } catch (e) {
    console.log("[HEARTBEAT ERROR]", e.message);
  }
}, 2000);

// self-healing supervisor loop
setInterval(() => {
  try {
    const state = require("./KERNEL_STATE").getState();

    if (!state.lastHeartbeat || state.runtime !== "alive") {
      console.log("[SELF-HEAL] detected unstable runtime");
      healAll();
    }
  } catch (e) {
    console.log("[SELF-HEAL ERROR]", e.message);
    healAll();
  }
}, 10000);
