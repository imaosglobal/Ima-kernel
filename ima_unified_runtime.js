const os = require("./ima_kernel_os");
const evo = require("./ima_evolving_core");

function boot(input){

  console.log("🚀 IMA UNIFIED RUNTIME START");

  // 1. Boot kernel
  const kernel = os.boot({ mode: "unified" });

  // 2. Run evolving core
  const result = evo.run(input);

  // 3. Sync memory
  os.memory.state.lastRun = result;

  console.log("✅ UNIFIED CYCLE COMPLETE");

  return {
    kernel,
    result
  };
}

module.exports = { boot };
