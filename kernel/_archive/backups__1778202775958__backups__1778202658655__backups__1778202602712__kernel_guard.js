const fs = require("fs");

function validateKernel() {
  const lock = JSON.parse(fs.readFileSync("./kernel_lock.json", "utf8"));

  const active = lock.active_kernel;

  if (!fs.existsSync("./" + active)) {
    throw new Error("ACTIVE KERNEL MISSING");
  }

  console.log("KERNEL VALIDATED:", active);
  return active;
}

module.exports = { validateKernel };
