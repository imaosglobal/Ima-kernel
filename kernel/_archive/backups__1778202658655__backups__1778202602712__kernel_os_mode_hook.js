const fs = require("fs");
const path = require("path");

function getKernelRoot() {
  return process.env.KERNEL_ROOT || path.join(process.env.HOME, "ima_core/kernel");
}

function validateKernel() {
  const root = getKernelRoot();

  const lockPath = path.join(root, "kernel_lock.json");
  const kernelPath = path.join(root, "ima_saas_full.js");

  if (!fs.existsSync(lockPath)) {
    throw new Error("KERNEL LOCK MISSING");
  }

  const lock = JSON.parse(fs.readFileSync(lockPath, "utf8"));

  if (lock.active_kernel !== "ima_saas_full.js") {
    throw new Error("INVALID ACTIVE KERNEL");
  }

  if (!fs.existsSync(kernelPath)) {
    throw new Error("KERNEL FILE MISSING");
  }

  console.log("[TERMUSBOT] KERNEL OK:", lock.active_kernel);
  return true;
}

module.exports = { validateKernel };
