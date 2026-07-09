const fs = require("fs");
const path = require("path");

const DB_PATH = path.join(__dirname, "ima_memory.json");

function load() {
  try {
    return JSON.parse(fs.readFileSync(DB_PATH, "utf8"));
  } catch (e) {
    return {};
  }
}

function save(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}

let store = load();

// 🧠 FIX: normalize old data
function normalize(user) {
  return {
    key: user.key,
    usage: user.usage || 0,
    history: user.history || [],
    feedback: user.feedback || [],
    improvementMode: user.improvementMode || false,
    createdAt: user.createdAt || Date.now()
  };
}

function getUser(key) {
  return store[key] ? normalize(store[key]) : null;
}

function createUser(key) {
  if (!store[key]) {
    store[key] = normalize({
      key,
      usage: 0,
      history: [],
      feedback: [],
      improvementMode: false
    });
    save(store);
  }
  return store[key];
}

function addEvent(key, event) {
  if (!store[key]) return;

  store[key] = normalize(store[key]);

  store[key].history.push({ ...event, ts: Date.now() });
  store[key].usage++;

  save(store);
}

function addFeedback(key, feedback) {
  if (!store[key]) return;

  store[key] = normalize(store[key]);

  store[key].feedback.push({ ...feedback, ts: Date.now() });

  save(store);
}

function getContext(key) {
  const user = store[key];
  if (!user) return {};

  const u = normalize(user);

  const tasks = u.history.map(h => h.task);

  const frequencyMap = {};
  for (const t of tasks) {
    frequencyMap[t] = (frequencyMap[t] || 0) + 1;
  }

  const topTask = Object.keys(frequencyMap)
    .sort((a, b) => frequencyMap[b] - frequencyMap[a])[0];

  const satisfactionScore =
    u.feedback.length > 0
      ? u.feedback.reduce((a, f) => a + (f.score || 0), 0) / u.feedback.length
      : null;

  return {
    usage: u.usage,
    historySize: u.history.length,
    topTask,
    satisfactionScore,
    improvementMode: u.improvementMode
  };
}

function setImprovementMode(key, value) {
  if (!store[key]) return;

  store[key] = normalize(store[key]);
  store[key].improvementMode = value;

  save(store);
}

module.exports = {
  getUser,
  createUser,
  addEvent,
  addFeedback,
  getContext,
  setImprovementMode
};
