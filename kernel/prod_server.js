const express = require("express");
const fs = require("fs");

const app = express();
app.use(express.json());

// ===== BASIC HEALTH =====
app.get("/health", (req, res) => {
  res.json({ ok: true, status: "alive", uptime: process.uptime() });
});

// ===== BASIC TEST ROUTE =====
app.post("/v2/test", (req, res) => {
  res.json({
    ok: true,
    result: "Processed: " + (req.body.task || "no task")
  });
});

// ===== LOGGING =====
function logEvent(event) {
  try {
    const file = "ima_memory.json";
    let data = [];
    if (fs.existsSync(file)) {
      data = JSON.parse(fs.readFileSync(file));
    }
    data.push(event);
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
  } catch (e) {}
}

// ===== REQUEST LOG =====
app.use((req, res, next) => {
  logEvent({
    type: "request",
    path: req.path,
    method: req.method,
    ts: Date.now()
  });
  next();
});

// ===== EVOLUTION LOOP =====
const { evolve } = require("./evolution_engine");

setInterval(() => {
  try {
    evolve();
  } catch (e) {
    console.log("[EVOLVE ERROR]", e.message);
  }
}, 30000);

// ===== START =====
app.listen(4000, () => {
  console.log("IMA RUNNING ON 4000");
});

// ===== INTELLIGENCE LAYER =====
const { run } = require("./release_manager");

setInterval(() => {
  try {
    run();
  } catch (e) {
    console.log("[AI LAYER ERROR]", e.message);
  }
}, 60000);

// ==============================
