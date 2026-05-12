let state = {
  runtime: "booting",
  lastHeartbeat: 0,
  status: "booting"
};

function updateHeartbeat() {
  state.runtime = "alive";
  state.lastHeartbeat = Date.now();
  state.status = "healthy";
}

function getState() {
  return state;
}

module.exports = {
  state,
  updateHeartbeat,
  getState
};
