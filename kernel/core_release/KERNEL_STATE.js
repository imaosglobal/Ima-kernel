const state = {
  runtime: "unknown",
  lastHeartbeat: 0,
  status: "booting"
};

function updateHeartbeat() {
  state.lastHeartbeat = Date.now();
  state.runtime = "alive";
  state.status = "healthy";
}

module.exports = {
  state,
  updateHeartbeat
};
