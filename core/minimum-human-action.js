/**
 * IMA system-wide minimum-human-action planner.
 * It plans and gates actions; it never fabricates authority.
 */
export const HUMAN_ACTION_CLASSES = Object.freeze([
  "NONE","REVIEW","APPROVAL","IDENTITY","SIGNATURE",
  "BANKING","LIVE_INTERACTION","ACCOUNTABLE_DECISION","BLOCKED"
]);

const HARD_BOUNDARIES = new Set([
  "IDENTITY","SIGNATURE","BANKING","LIVE_INTERACTION","ACCOUNTABLE_DECISION"
]);

export function classifyHumanBoundary({ requiresHuman = false, irreversible = false,
  requiresIdentity = false, requiresSignature = false, requiresBanking = false,
  requiresLiveInteraction = false, requiresAccountableDecision = false,
  authorized = false, technicallyAvailable = true } = {}) {
  if (!technicallyAvailable) return "BLOCKED";
  if (requiresAccountableDecision) return "ACCOUNTABLE_DECISION";
  if (requiresSignature) return "SIGNATURE";
  if (requiresBanking) return "BANKING";
  if (requiresIdentity) return "IDENTITY";
  if (requiresLiveInteraction) return "LIVE_INTERACTION";
  if (requiresHuman) return irreversible && !authorized ? "APPROVAL" : "REVIEW";
  return "NONE";
}

export function buildMinimumHumanPlan(task = {}) {
  const steps = Array.isArray(task.steps) ? task.steps : [];
  const normalized = steps.map((step, index) => ({
    id: step.id || `step-${index + 1}`,
    title: step.title || step.id || `Step ${index + 1}`,
    boundary: classifyHumanBoundary(step),
    reversible: step.reversible !== false,
    prepared: step.prepared !== false,
    provider: step.provider || null
  }));

  const mandatory = normalized.filter(s => s.boundary !== "NONE");
  const hard = mandatory.filter(s => HARD_BOUNDARIES.has(s.boundary));
  const review = mandatory.filter(s => s.boundary === "REVIEW" || s.boundary === "APPROVAL");

  // One grouped human interaction where the legal/provider workflow permits it.
  const grouped = [...new Map(
    mandatory.map(s => [s.boundary, s])
  ).values()].map(s => s.boundary);

  return {
    task_id: task.task_id || null,
    automated_steps: normalized.filter(s => s.boundary === "NONE").map(s => s.id),
    human_steps: mandatory.map(s => s.id),
    hard_boundaries: hard.map(s => ({ id: s.id, boundary: s.boundary })),
    grouped_human_actions: grouped,
    minimum_interactions: mandatory.length === 0 ? 0 : 1,
    stop_before: hard.length ? hard[0].id : (review[0]?.id || null),
    resume_after_human: mandatory.length > 0,
    rule: "MINIMUM_HUMAN_ACTION"
  };
}

export function canDelegateToProvider({ capability, providerAuthorized = false, userAuthorized = false } = {}) {
  return Boolean(capability && providerAuthorized && userAuthorized);
}
