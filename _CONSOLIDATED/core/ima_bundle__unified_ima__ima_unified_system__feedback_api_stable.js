const express = require("express");

const app = express();
app.use(express.json());

let running = true;

app.post("/ima/feedback", (req, res) => {
  res.json({ ok: true });
});

app.get("/ima/feedback/summary", (req, res) => {
  res.json({ status: "alive" });
});

// חשוב: לא exit, לא crash
process.on("uncaughtException", (err) => {
  console.log("⚠️ ERROR CAUGHT:", err.message);
});

process.on("SIGTERM", () => {
  console.log("🛑 SHUTDOWN SAFE");
  running = false;
});

app.listen(5000, () => {
  console.log("📡 FEEDBACK ENGINE STABLE ON 5000");
});
