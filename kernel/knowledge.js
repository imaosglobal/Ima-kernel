const fs = require("fs");

function loadKnowledge() {
  try {
    return JSON.parse(fs.readFileSync("./learning_log.json", "utf8"));
  } catch (e) {
    return [];
  }
}

function summarize() {
  const data = loadKnowledge();

  return {
    totalRepos: data.length,
    avgPatterns: data.reduce((a, b) => a + (b.patterns || 0), 0) / (data.length || 1)
  };
}

module.exports = { loadKnowledge, summarize };
