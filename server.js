const express = require("express");
const fs = require("fs");
const app = express();

const LOCK = __dirname + "/runtime/instance.lock";

// --- single instance guard ---
try {
  if (fs.existsSync(LOCK)) {
    const pid = parseInt(fs.readFileSync(LOCK, "utf8"));
    try {
      process.kill(pid, 0);
      console.log("[IMA] already running:", pid);
      process.exit(0);
    } catch {}
  }

  fs.mkdirSync(__dirname + "/runtime", { recursive: true });
  fs.writeFileSync(LOCK, process.pid.toString());
} catch (e) {
  console.log("[IMA] lock error:", e.message);
}

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "alive", time: Date.now() });
});

app.get("/", (req, res) => {
  res.json({
    status: "IMA LIVE",
    pid: process.pid
  });
});

app.listen(3000, () => {
  console.log("🧠 IMA KERNEL RUNNING");
});
