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


setInterval(() => {
  try {
  } catch (e) {
    console.log("[EVOLVE ERROR]", e.message);
  }
}, 30000);



// ===== START =====
require("./run_bridge")(app);
app.listen(4000, () => {
  console.log("IMA RUNNING ON 4000");
});

// ===== INTELLIGENCE LAYER =====

setInterval(() => {
  try {
  } catch (e) {
  }
}, 60000);

// ==============================


setInterval(() => {
  try {
  } catch (e) {
    console.log("[PRODUCT ERROR]", e.message);
  }
}, 60000);



setInterval(() => {
  try {
  } catch (e) {
    console.log("[EXECUTION ERROR]", e.message);
  }
}, 60000);



setInterval(() => {
  try {
  } catch (e) {
    console.log("[CODE ERROR]", e.message);
  }
}, 60000);



setInterval(() => {
  try {
  } catch (e) {
    console.log("[SAFETY ERROR]", e.message);
  }
}, 60000);


// ===== ROUTE FIX =====



// SAFE ROUTES MOUNT (single source of truth)



// === SINGLE ROUTE BINDING (CLEAN) ===
const taskRoutes = require("./task_routes");
const productRoutes = require("./product_routes");

app.use("/v2", taskRoutes);
app.use("/v2", productRoutes);

// ===================================

app.get("/v2/health", (req, res) => {
  res.json({
    ok: true,
    status: "alive",
    uptime: process.uptime()
  });
});

