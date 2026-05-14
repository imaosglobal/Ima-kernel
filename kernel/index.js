const express = require("express");
const fs = require("fs");

const app = express();
app.use(express.json());

const STATE_PATH = __dirname + "/state.json";

function loadState() {
  if (!fs.existsSync(STATE_PATH)) {
    fs.writeFileSync(STATE_PATH, JSON.stringify({
      mode: "IMA_KERNEL_V1",
      users: 0,
      events: 0
    }, null, 2));
  }
  return JSON.parse(fs.readFileSync(STATE_PATH));
}

function save(state) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

let state = loadState();

app.get("/health", (_, res) => {
  res.json({
    ok: true,
    mode: state.mode,
    users: state.users,
    events: state.events
  });
});

app.listen(3000, () => {
  console.log("IMA KERNEL RUNNING");
});
