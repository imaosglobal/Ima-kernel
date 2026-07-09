module.exports = function personality(input, context = {}) {

  const usage = context.usage || 0;
  const need = context.inferredNeed || "general_support";
  const improvementMode = context.improvementMode;

  let tone = "neutral";

  if (need === "problem_solving") tone = "focused";
  if (need === "guided_support") tone = "gentle-assistant";
  if (need === "teacher_mode") tone = "educational";

  let improvement = null;

  if (improvementMode) {
    improvement = generateImprovementHint(input, need);
  }

  return {
    message: `I understand your goal: ${input}`,
    tone,
    improvement
  };
};

function generateImprovementHint(input, need) {
  if (need === "problem_solving") {
    return "Try breaking the problem into smaller steps before asking for a fix.";
  }
  if (need === "learning") {
    return "Try explaining what you already know so I can adapt better.";
  }
  return "Keep practicing — consistency improves results.";
}
