const { execSync } = require("child_process");

function killOnlyKernel() {
  try {
    console.log("CHECKING KERNEL INSTANCES...");

    let output = "";
    try {
      output = execSync("pgrep -f ima_saas_full.js || true")
        .toString()
        .trim();
    } catch (e) {
      output = "";
    }

    if (!output) {
      console.log("NO KERNELS FOUND");
      return;
    }

    const pids = output.split("\n").filter(Boolean);

    if (pids.length > 1) {
      console.log("DUP KERNELS:", pids);

      pids.slice(1).forEach(pid => {
        try {
          process.kill(parseInt(pid), "SIGKILL");
          console.log("KILLED PID:", pid);
        } catch (e) {}
      });
    }

    console.log("KERNEL GUARD OK");
  } catch (e) {
    console.log("GUARD ERROR:", e.message);
  }
}

module.exports = { killOnlyKernel };
