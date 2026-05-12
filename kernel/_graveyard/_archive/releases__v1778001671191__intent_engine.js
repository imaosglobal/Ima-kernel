function analyzeIntent(task, context = {}) {

  const text = (task || "").toLowerCase();

  let intent = "general";

  if (text.includes("fix") || text.includes("error")) intent = "debugging";
  if (text.includes("build") || text.includes("create")) intent = "creation";
  if (text.includes("how") || text.includes("explain")) intent = "learning";
  if (text.includes("help")) intent = "assistance";

  return {
    intent,
    confidence: 0.7,
    inferredNeed: mapNeed(intent)
  };
}

function mapNeed(intent) {
  switch (intent) {
    case "debugging": return "problem_solving";
    case "creation": return "builder_mode";
    case "learning": return "teacher_mode";
    case "assistance": return "guided_support";
    default: return "general_support";
  }
}

module.exports = analyzeIntent;
