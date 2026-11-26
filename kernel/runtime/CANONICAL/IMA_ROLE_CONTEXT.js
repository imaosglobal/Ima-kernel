const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../../docs");
const SOURCES = [
  "IMA_HUMAN_INTELLIGENCE_CHARTER.md",
  "IMA_UNIVERSAL_VOCATION_AND_LIFE_DIRECTION.md",
  "IMA_CREATOR_QUESTIONS_AND_HUMAN_PATH_CHARTER.md",
  "IMA_MULTI_PERSPECTIVE_REVIEW_PROTOCOL.md",
  "IMA_SELF_MARKETING_AND_GROWTH_ENGINE.md",
  "IMA_UNIVERSAL_ROLE_AND_HUMAN_AI_FUNCTION_MAP.md",
  "IMA_PERMANENT_VERIFICATION_AND_SELF_REPAIR_CONTRACT.md",
  "IMA_LONGEVITY_AGING_RESEARCH_AND_COLLABORATION_MAP.md",
  "IMA_MASTER_REQUIREMENTS_LEDGER.md"
];

function read(name) {
  try {
    return fs.readFileSync(path.join(ROOT, name), "utf8");
  } catch {
    return "";
  }
}

function buildContext() {
  const documents = SOURCES.map(name => ({ name, content: read(name) }))
    .filter(x => x.content);

  return {
    identity: "IMA — אמא",
    mode: "canonical-human-centered-intelligence",
    instruction:
      "Use the canonical IMA knowledge and role framework in every conversation when relevant. Answer naturally in the user's language and context. Distinguish verified fact, source-reported claim, interpretation, forecast, hypothesis and unknown. Preserve human agency. Do not claim a capability is active unless runtime evidence supports it.",
    role_rule:
      "Identify the relevant human role or combination of roles, what the person is responsible for, what authority exists, what IMA can safely do, what must remain human, and what evidence would show that the support helped.",
    role_map: "docs/IMA_UNIVERSAL_ROLE_AND_HUMAN_AI_FUNCTION_MAP.md",
    sources: documents
  };
}

function contextForPrompt(message, options = {}) {
  const base = buildContext();
  const maxChars = Number(options.maxChars || 50000);
  let out = JSON.stringify(base);
  if (out.length > maxChars) out = out.slice(0, maxChars);
  return {
    system_context: out,
    user_message: String(message || "")
  };
}

function status() {
  const context = buildContext();
  return {
    ready: context.sources.length === SOURCES.length,
    loaded_documents: context.sources.map(x => x.name),
    role_map: context.role_map,
    canonical: true
  };
}

module.exports = { buildContext, contextForPrompt, status };
