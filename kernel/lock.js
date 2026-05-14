const fs = require("fs");
const path = require("path");

const LOCK = path.join(__dirname, "../runtime/kernel.lock");

function lock() {
  if (fs.existsSync(LOCK)) {
    const pid = fs.readFileSync(LOCK, "utf-8");
    try {
      process.kill(parseInt(pid), 0);
      console.log("KERNEL ALREADY RUNNING");
      process.exit(1);
    } catch {
      fs.writeFileSync(LOCK, String(process.pid));
    }
  } else {
    fs.writeFileSync(LOCK, String(process.pid));
  }
}

module.exports = { lock };
