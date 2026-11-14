"use strict";

/**
 * IMA Continuous Learning & World Pattern Engine
 *
 * Purpose:
 * - turn external evidence into durable, provenance-aware learning
 * - compare IMA against successful and failed projects without copying them
 * - translate findings into testable product hypotheses
 * - preserve human agency: learning does not silently authorize consequential action
 *
 * The engine is intentionally model-agnostic. A web/research adapter can feed
 * evidence through ingest(). IMA then normalizes, deduplicates, scores, and
 * turns evidence into candidate improvements.
 */

const crypto = require("crypto");
const memory = require("./memory/IMA_MEMORY");
const truthGate = require("./IMA_TRUTH_GATE");
const agencyGate = require("./IMA_HUMAN_AGENCY_GATE");

const DOMAINS = Object.freeze([
  "TRUST",
  "AGENCY",
  "USEFULNESS",
  "ACCESSIBILITY",
  "LEARNING",
  "ADOPTION",
  "COMMUNITY",
  "SAFETY",
  "PRIVACY",
  "GOVERNANCE",
  "EVALUATION",
  "DISTRIBUTION",
  "ECONOMIC_SUSTAINABILITY",
  "INTEROPERABILITY",
  "PRESERVATION"
]);

const DEFAULT_LESSONS = Object.freeze([
  {
    id: "lesson-agency-not-dependency",
    domain: "AGENCY",
    pattern: "A successful human-centered system should increase the person's capability and freedom to act, not make itself permanently necessary.",
    action: "Measure whether IMA returns capability to the user, including whether the user can become less dependent on IMA.",
    evidence: "IMA canonical product principle",
    source: "https://github.com/imaosglobal/Ima-kernel"
  },
  {
    id: "lesson-truth-before-claim",
    domain: "TRUST",
    pattern: "Claims about capability, success, verification, or deployment must follow evidence rather than precede it.",
    action: "Make every important IMA claim traceable to a source, timestamp, reproducible check, or explicit unknown.",
    evidence: "IMA Truth Gate",
    source: "https://github.com/imaosglobal/Ima-kernel"
  },
  {
    id: "lesson-wonder-as-action",
    domain: "USEFULNESS",
    pattern: "Wonder is valuable when it produces better questions, learning, experiments, and human possibility rather than passive spectacle.",
    action: "Treat curiosity and awe as inputs to exploration, not as substitutes for evidence or action.",
    evidence: "IMA canonical product direction",
    source: "https://github.com/imaosglobal/Ima-kernel"
  },
  {
    id: "lesson-human-agency",
    domain: "AGENCY",
    pattern: "AI systems scale more sustainably when people retain purpose, control, collaboration, and meaningful choice.",
    action: "Measure whether IMA increases the user's capability and control rather than merely increasing dependency.",
    evidence: "Springer Human Agency Framework, 2026",
    source: "https://link.springer.com/article/10.1007/s44217-026-02173-7"
  },
  {
    id: "lesson-proof-over-promise",
    domain: "EVALUATION",
    pattern: "Successful AI deployment increasingly depends on measurable value, redesigned human-AI workflows, strong data foundations, and calibrated oversight.",
    action: "Every major IMA capability must have an observable outcome, evaluation method, and human-oversight boundary.",
    evidence: "World Economic Forum MINDS / Accenture, 2026",
    source: "https://www.weforum.org/publications/proof-over-promise-insights-on-real-world-ai-adoption-from-2025-minds-organizations"
  },
  {
    id: "lesson-adopt-sustain-optimise",
    domain: "ADOPTION",
    pattern: "Adoption is a lifecycle: adopt, sustain, optimise; onboarding, confidence, recurring use, and risk mitigation matter.",
    action: "IMA must measure first-use success, repeat use, user confidence, failure recovery, and safe expansion.",
    evidence: "UK Government Assist scaling lessons",
    source: "https://www.gov.uk/government/publications/a-human-centred-approach-to-scaling-and-de-risking-ai-tools/the-people-factor-a-human-centred-approach-to-scaling-ai-tools-html"
  },
  {
    id: "lesson-global-learning",
    domain: "DISTRIBUTION",
    pattern: "Global educational products can scale when they are accessible across countries and languages while preserving a simple core value proposition.",
    action: "Design IMA as a language-, age-, culture-, and ability-adaptive system without fragmenting the canonical core.",
    evidence: "Khan Academy annual impact data",
    source: "https://annualreport.khanacademy.org/"
  },
  {
    id: "lesson-community-contribution",
    domain: "COMMUNITY",
    pattern: "Community contribution can become a growth and quality mechanism when participation is genuinely useful and identity is clear.",
    action: "Give IMA users safe ways to teach, test, contribute, correct, and improve the system without surrendering personal data.",
    evidence: "Duolingo community growth analysis",
    source: "https://community.inc/deep-dives/contribution-duolingo"
  },
  {
    id: "lesson-trust-is-conditional",
    domain: "TRUST",
    pattern: "People accept AI more readily for low-risk assistance than for opaque autonomous or high-stakes decisions; transparency and human oversight remain central.",
    action: "Prefer visible evidence, uncertainty, reversible actions, and explicit human control over impressive but opaque autonomy.",
    evidence: "UK AI Adoption Research 2026",
    source: "https://assets.publishing.service.gov.uk/media/6ae202189bca21f1c5036e99/artificial-intelligence-adoption-research-report-2026.pdf"
  },
  {
    id: "lesson-failure-data-and-integration",
    domain: "INTEROPERABILITY",
    pattern: "Ambitious AI projects can fail because data integration, infrastructure, workflow fit, or organizational context is harder than the demo suggests.",
    action: "Before scaling an IMA capability, test real data boundaries, integration points, user workflow fit, operational cost, and failure recovery in small reversible experiments.",
    evidence: "2026 case studies of failed AI deployments and education chatbots",
    source: "https://www.jmir.org/2026/1/e87534/"
  },
  {
    id: "lesson-every-project-is-eval",
    domain: "EVALUATION",
    pattern: "AI systems become evaluation projects as soon as they operate in dynamic real-world settings.",
    action: "IMA's loop must continuously test real behavior, not rely only on static demonstrations or claims.",
    evidence: "Google Cloud 2025 lessons on agents and trust",
    source: "https://cloud.google.com/transform/ai-grew-up-and-got-a-job-lessons-from-2025-on-agents-and-trust"
  }
]);

function stableId(value) {
  return crypto.createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

function normalizeDomain(domain) {
  const d = String(domain || "").trim().toUpperCase();
  return DOMAINS.includes(d) ? d : "LEARNING";
}

function normalizeEvidence(item = {}) {
  const source = String(item.source || item.url || "").trim();
  const timestamp = item.timestamp || item.checked_at || new Date().toISOString();
  const status = item.status || (source ? "VERIFIED" : "GAPS_RECORDED");
  const gate = truthGate.assess({
    source,
    timestamp,
    reproducible: Boolean(item.reproducible || item.test || item.reproduction),
    status
  });

  return {
    id: item.id || stableId({
      title: item.title || "",
      source,
      claim: item.claim || item.pattern || "",
      timestamp
    }),
    title: String(item.title || "").trim(),
    source,
    timestamp,
    status: gate.status,
    truth_gate: gate,
    domain: normalizeDomain(item.domain),
    pattern: String(item.pattern || item.claim || "").trim(),
    action: String(item.action || "").trim(),
    counterexample: String(item.counterexample || "").trim(),
    context: item.context || {},
    confidence: Number.isFinite(item.confidence) ? item.confidence : (gate.verified ? 0.8 : 0.3)
  };
}

function seed() {
  const existing = memory.search("IMA_LEARNING_SEED");
  if (existing.length) return { seeded: false, count: existing.length };

  DEFAULT_LESSONS.forEach(lesson => {
    memory.append({
      type: "semantic",
      content: {
        type: "IMA_LEARNING_SEED",
        ...lesson
      },
      provenance: {
        source: "IMA_CONTINUOUS_LEARNING",
        verified: true
      }
    });
  });

  return { seeded: true, count: DEFAULT_LESSONS.length };
}

function ingest(items = []) {
  const list = Array.isArray(items) ? items : [items];
  const accepted = [];
  const rejected = [];

  for (const raw of list) {
    const item = normalizeEvidence(raw);
    if (!item.pattern) {
      rejected.push({ id: item.id, reason: "EMPTY_PATTERN" });
      continue;
    }

    const duplicate = memory.search(item.id).some(record =>
      record.content && record.content.type === "IMA_WORLD_EVIDENCE"
    );

    if (duplicate) continue;

    memory.append({
      type: "semantic",
      content: {
        type: "IMA_WORLD_EVIDENCE",
        ...item
      },
      provenance: {
        source: "IMA_CONTINUOUS_LEARNING",
        external_source: item.source || null,
        truth_gate: item.truth_gate
      }
    });

    accepted.push(item);
  }

  return { accepted, rejected };
}

function evidence() {
  return memory.list("semantic")
    .filter(record =>
      record.content &&
      ["IMA_LEARNING_SEED", "IMA_WORLD_EVIDENCE"].includes(record.content.type)
    )
    .map(record => record.content);
}

function synthesize() {
  const rows = evidence();
  const byDomain = {};

  for (const row of rows) {
    const domain = normalizeDomain(row.domain);
    byDomain[domain] ||= [];
    byDomain[domain].push(row);
  }

  const priorities = Object.entries(byDomain).map(([domain, items]) => {
    const verified = items.filter(x => x.truth_gate?.verified || x.evidence).length;
    const confidence = items.reduce((sum, x) => sum + (x.confidence || 0), 0) / items.length;
    return {
      domain,
      evidence_count: items.length,
      verified_or_sourced: verified,
      mean_confidence: Number(confidence.toFixed(3)),
      next: items
        .map(x => x.action)
        .filter(Boolean)
        .slice(0, 5)
    };
  }).sort((a, b) => (b.mean_confidence * b.evidence_count) - (a.mean_confidence * a.evidence_count));

  return {
    total_evidence: rows.length,
    domains: priorities,
    rule: "Learn broadly; change narrowly; verify before claiming success."
  };
}

function nextActions() {
  const synthesis = synthesize();
  return synthesis.domains
    .flatMap(d => d.next.map(action => ({
      domain: d.domain,
      action,
      action_class: agencyGate.classify("update_product"),
      approval_required: true,
      reason: "Learning can propose; canonical consequential change requires human authorization."
    })))
    .slice(0, 20);
}

function status() {
  return {
    domains: DOMAINS.slice(),
    evidence_count: evidence().length,
    seeded: evidence().some(x => x.id === "lesson-human-agency"),
    synthesis: synthesize()
  };
}

module.exports = {
  DOMAINS,
  DEFAULT_LESSONS,
  seed,
  ingest,
  evidence,
  synthesize,
  nextActions,
  status
};
