const express = require("express");
const app = express();

const mode = process.argv[2];

if (mode === "health") {
  console.log("OK");
  process.exit(0);
}

if (mode === "start" || !mode) {
  app.get("/", (req, res) => {
    res.json({ status: "running" });
  });

  const PORT = process.env.PORT || 4000;

  const server = app.listen(PORT, () => {
    console.log("GLOBAL API PRODUCT RUNNING ON", PORT);
  });

  server.on("error", (err) => {
    if (err.code === "EADDRINUSE") {
      console.error("PORT IN USE:", PORT);
      process.exit(1);
    }
    throw err;
  });
}

if (mode && !["start", "health"].includes(mode)) {
  console.log("ima usage:");
  console.log("  ima start");
  console.log("  ima health");
}
