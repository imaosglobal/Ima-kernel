const fs = require("fs");
const path = require("path");

const LOCK = path.join(__dirname, "kernel.lock");

function acquireLock() {
  try {
    if (fs.existsSync(LOCK)) {
      const pid = fs.readFileSync(LOCK, "utf8");

      try {
        process.kill(parseInt(pid), 0);
        console.log("KERNEL ALREADY RUNNING:", pid);
        process.exit(0);
      } catch {
        console.log("STALE LOCK REMOVED");
      }
    }

    fs.writeFileSync(LOCK, process.pid.toString());
    console.log("LOCK ACQUIRED:", process.pid);
  } catch (e) {
    console.log("LOCK ERROR:", e.message);
  }
}

process.on("exit", () => {
  try {
    fs.unlinkSync(LOCK);
  } catch {}
});

module.exports = { acquireLock };
