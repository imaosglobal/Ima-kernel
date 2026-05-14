const fs = require("fs");

function loadFeedback() {
  if (!fs.existsSync("feedback_log.json")) return [];
  return JSON.parse(fs.readFileSync("feedback_log.json"));
}

function integrateFeedback() {
  const data = loadFeedback();

  console.log("🧠 INTEGRATING HUMAN FEEDBACK");

  let positives = data.filter(d => d.rating >= 4).length;
  let negatives = data.filter(d => d.rating <= 2).length;

  let insight = {
    total: data.length,
    positives,
    negatives,
    trustScore: positives / (data.length || 1)
  };

  fs.writeFileSync("human_insights.json", JSON.stringify(insight, null, 2));

  console.log("📊 HUMAN INSIGHTS UPDATED:", insight);
}

integrateFeedback();
