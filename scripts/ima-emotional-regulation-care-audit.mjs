import fs from "node:fs";

const path = "docs/IMA_EMOTIONAL_REGULATION_AND_ADAPTIVE_HUMAN_CARE.md";
if (!fs.existsSync(path)) throw new Error("Missing canonical emotional-regulation care standard");

const text = fs.readFileSync(path, "utf8");
const requiredSections = [
  "## Core regulation loop",
  "## Universal adaptation",
  "## Medical boundary",
  "## Future technology research",
  "## Trauma and procedure mode",
  "## Safety escalation",
  "## Personalization without surveillance",
  "## Human-agency rule",
  "## Evidence rule",
  "## Humor rule",
  "## Governance"
];

for (const section of requiredSections) {
  if (!text.includes(section)) throw new Error("Missing required care-governance section: " + section);
}

const forbiddenClaims = [
  "diagnose from conversation alone",
  "prescribe or change medication",
  "recommend an individualized drug dose",
  "replace emergency services or qualified clinicians"
];

for (const phrase of forbiddenClaims) {
  if (!text.includes(phrase)) throw new Error("Medical safety boundary missing: " + phrase);
}

console.log(JSON.stringify({
  ok: true,
  standard: path,
  regulation_loop: "notice-orient-name-reduce-load-choose-connect-review-learn",
  medical_boundary: true,
  human_agency: true,
  privacy: true,
  safety_escalation: true,
  future_technology_gate: true,
  humor_is_optional: true
}, null, 2));
