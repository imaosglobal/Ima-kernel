const app = require("./apply_fix");

const PORT = 4000;

process.on("uncaughtException", e => console.log("[CRASH SAFE]", e));
process.on("unhandledRejection", e => console.log("[PROMISE SAFE]", e));

app.listen(PORT, () => {
  console.log("IMA RUNNING ON", PORT);
});

// HEALTH CHECK (critical)
app.get("/health", (req, res) => {
  res.json({
    ok: true,
    status: "alive",
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
});


const productRoutes = require("./product_routes");
productRoutes(app);




// === IMA V2 ROUTES FIX ===

// ensure app exists
if (typeof app !== "undefined") {
}

// === IMA V2 ROUTES (CLEAN) ===
const taskRoutes = require("./task_routes");
taskRoutes(app);
