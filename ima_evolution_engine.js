const fs = require("fs");

const FILE = "./ima_evolution_state.json";

function load() {
  return JSON.parse(fs.readFileSync(FILE));
}

function save(s) {
  fs.writeFileSync(FILE, JSON.stringify(s, null, 2));
}

// סימולציה של מדד ביצועים (מחובר אצלך כבר ל־avg response)
function getScore() {
  return 40 + Math.random() * 30;
}

function evolve() {
  const state = load();

  const score = getScore();
  state.score_history.push(score);

  if (state.score_history.length > 20) {
    state.score_history.shift();
  }

  // עדכון best
  if (score > state.best_score) {
    state.best_score = score;
  }

  // החלטת אבולוציה
  if (score < 45) {
    state.mutation_rate *= 0.95;
    state.mode = "stabilize";
  } else if (score > 55) {
    state.mutation_rate *= 1.05;
    state.mode = "explore";
  } else {
    state.mode = "steady";
  }

  // דור חדש כל ריצה טובה
  if (score > 60) {
    state.generation += 1;
  }

  save(state);

  console.log("🧠 EVOLUTION STEP");
  console.log("score:", score.toFixed(2));
  console.log("generation:", state.generation);
  console.log("mode:", state.mode);
}

evolve();
