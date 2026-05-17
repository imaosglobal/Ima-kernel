const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();

const STATE = path.join(__dirname, "..", "runtime", "state.json");

function writeState() {
  fs.writeFileSync(
    STATE,
    JSON.stringify({
      status: "ONLINE",
      mode: "IMA_SINGLE_CLEAN",
      pid: process.pid,
      ts: Date.now()
    }, null, 2)
  );
}

app.get("/", (req, res) => {
  res.send("IMA SINGLE CLEAN ONLINE");
});

app.get("/health", (req, res) => {
  writeState();

  res.json({
    status: "ONLINE",
    mode: "IMA_SINGLE_CLEAN",
    pid: process.pid,
    ts: Date.now()
  });
});

const PORT = 7000;

app.listen(PORT, () => {
  writeState();
  console.log("[IMA] ONLINE :" + PORT);
});
