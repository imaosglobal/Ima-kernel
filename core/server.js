const express = require("express");

const app = express();

app.get("/health", (req, res) => {
  res.json({
    status: "ONLINE",
    mode: "IMA_SINGLE_KERNEL",
    ts: Date.now()
  });
});

app.get("/", (req, res) => {
  res.send("IMA KERNEL ACTIVE");
});

const PORT = 7000;

app.listen(PORT, () => {
  console.log("[IMA] SERVER ONLINE :" + PORT);
});
