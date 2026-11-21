/**
 * IMA canonical resilience runtime.
 * Policy engine only: detects/classifies/plans; it does not publish or take
 * accountable human/legal/medical/banking actions by itself.
 */
import protocol from "./GLOBAL_RESILIENCE_AND_CRISIS_PROTOCOL.json" with { type: "json" };

export const CRISIS_CLASSES = Object.freeze([
  "PERSONAL","HEALTH","REPUTATION","LEADERSHIP","LEGAL_REGULATORY",
  "CYBER_DATA","FINANCIAL","PRODUCT_SAFETY","RELATIONSHIP_FAMILY",
  "MEDIA_SOCIAL","CONTINUITY","MISINFORMATION"
]);

export const SEVERITIES = Object.freeze(["LOW","MODERATE","HIGH","CRITICAL"]);

const HARD_ACTIONS = new Set([
  "IDENTITY","SIGNATURE","BANKING","LIVE_INTERACTION","ACCOUNTABLE_DECISION"
]);

export function classifyIncident(input = {}) {
  const category = CRISIS_CLASSES.includes(input.category) ? input.category : "CONTINUITY";
  const severity = SEVERITIES.includes(input.severity) ? input.severity : "MODERATE";
  const confidence = ["LOW","MEDIUM","HIGH"].includes(input.confidence) ? input.confidence : "LOW";
  const affected = Array.isArray(input.affected) ? input.affected : [];
  return {
    category, severity, confidence, affected,
    verified: Boolean(input.verified),
    source: input.source || null,
    unknowns: Array.isArray(input.unknowns) ? input.unknowns : [],
    timestamp: input.timestamp || new Date().toISOString()
  };
}

export function buildResiliencePlan(incident = {}) {
  const i = classifyIncident(incident);
  const urgent = i.severity === "HIGH" || i.severity === "CRITICAL";
  const actions = [
    "PRESERVE_EVIDENCE",
    "PROTECT_AFFECTED_PEOPLE",
    "SEPARATE_FACTS_HYPOTHESES_UNKNOWNS",
    "CONTAIN_HARM",
    "ESTABLISH_SINGLE_SOURCE_OF_TRUTH",
    "ASSIGN_QUALIFIED_RESPONSE_OWNER",
    "PREPARE_STAKEHOLDER_UPDATE",
    "VERIFY_OUTCOME",
    "RECORD_LESSONS"
  ];
  if (urgent) actions.splice(1, 0, "ESCALATE_TO_HUMAN_REVIEW");

  return {
    protocol: protocol.name,
    incident: i,
    lifecycle: urgent ? ["DETECT","CONTAIN","RESPOND","RECOVER","REBUILD","LEARN"] :
      ["DETECT","RESPOND","RECOVER","LEARN"],
    actions,
    communication: {
      verified_only: true,
      include_unknowns: true,
      next_update_required: true,
      evidence_required: true
    },
    human_boundary: urgent ? "REVIEW" : "NONE",
    stop_before: urgent ? "PUBLIC_OR_IRREVERSIBLE_ACTION" : null
  };
}

export function gateAction(action = {}) {
  if (!action.technicallyAvailable) return { allowed:false, boundary:"BLOCKED" };
  const boundary =
    action.requiresIdentity ? "IDENTITY" :
    action.requiresSignature ? "SIGNATURE" :
    action.requiresBanking ? "BANKING" :
    action.requiresLiveInteraction ? "LIVE_INTERACTION" :
    action.requiresAccountableDecision ? "ACCOUNTABLE_DECISION" :
    action.requiresHuman && action.irreversible && !action.authorized ? "APPROVAL" :
    action.requiresHuman ? "REVIEW" : "NONE";
  return {
    allowed: boundary === "NONE" || Boolean(action.authorized && !HARD_ACTIONS.has(boundary)),
    boundary,
    must_stop: HARD_ACTIONS.has(boundary) || boundary === "APPROVAL"
  };
}

export function buildEvidenceRecord({ incident, action, result, actor = "IMA" } = {}) {
  const i = classifyIncident(incident);
  return {
    schema_version: "1.0",
    timestamp: new Date().toISOString(),
    incident: i,
    action: action || null,
    result: result || null,
    actor,
    unresolved_unknowns: i.unknowns,
    provenance_required: true
  };
}
