const express = require("express");
const app = express();

const mode = process.argv[2];
const env = process.env.IMA_MODE;

if (mode === "health") {
  console.log("OK");
  process.exit(0);
}

if (mode === "dry" || env === "ci") {
  console.log("[CI MODE] no server start");
  process.exit(0);
}

if (mode === "start" || !mode) {
  app.get("/", (req, res) => {
    res.json({ status: "running" });
  });

  const PORT = process.env.PORT || 4000;

  app.listen(PORT, () => {
    console.log("GLOBAL API PRODUCT RUNNING ON", PORT);
  });
}
