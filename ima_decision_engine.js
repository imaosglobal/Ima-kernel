const fs = require("fs");

function load() {
  return JSON.parse(fs.readFileSync("./ima_state.json"));
}

function save(state) {
  fs.writeFileSync("./ima_state.json", JSON.stringify(state, null, 2));
}

function evaluate() {
  const state = load();

  if (state.last_score < 45) {
    state.learning_rate *= 0.9;
    state.mode = "stabilize";
  } else if (state.last_score > 55) {
    state.learning_rate *= 1.1;
    state.mode = "expand";
  } else {
    state.mode = "steady";
  }

  save(state);
  console.log("🧠 decision updated:", state);
}

evaluate();
