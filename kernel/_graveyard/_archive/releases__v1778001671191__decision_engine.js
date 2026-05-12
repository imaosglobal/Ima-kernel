
const stateProvider = require("./state_provider");

function score(state) {
  let s = 100;

  if (!state.health?.ok) s -= 40;
  if ((state.queue?.queue || []).length > 10) s -= 20;

  return Math.max(0, s);
}

async function decide(action) {
  const state = {
    health: await stateProvider.health(),
    queue: await stateProvider.queue()
  };

  const s = score(state);

  let decision = "ALLOW";

  if (s < 40) decision = "BLOCK";
  else if (s < 70) decision = "DEFER";

  return {
    state,
    score: s,
    action,
    decision
  };
}

(async () => {
  const action = process.argv[2] || "unknown";
  console.log(JSON.stringify(await decide(action), null, 2));
})();

