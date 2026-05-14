const express = require("express");

const app = express();
app.use(express.json());

console.log("📡 FEEDBACK ENGINE BOOTING");

app.post("/ima/feedback", (req, res) => {
  res.json({ ok: true });
});

app.get("/ima/feedback/summary", (req, res) => {
  res.json({
    status: "alive",
    time: Date.now()
  });
});

// חשוב מאוד: לוג לפני listen
console.log("⏳ starting listener...");

const server = app.listen(5000, () => {
  console.log("📡 FEEDBACK ENGINE RUNNING ON 5000");
});

// מניעת exit שקט
process.on("uncaughtException", (err) => {
  console.log("⚠️ UNCAUGHT:", err);
});

process.on("unhandledRejection", (err) => {
  console.log("⚠️ PROMISE ERROR:", err);
});

// מחזיק process חי בכוח (debug safety)
setInterval(() => {
  // heartbeat
}, 10000);
