"use strict";

const memory = require("./memory/IMA_MEMORY");
const agents = require("./gateway/IMA_AGENT_GATEWAY");
const action = require("./orchestration/IMA_ACTION_ENGINE");
const policy = require("./IMA_POLICY");

const DOTS_ID = "ima-dots";
const CONTRACT_VERSION = "1.0.0";

function card() {
  return {
    id: DOTS_ID,
    name: "IMA Dots",
    description: "Canonical continuous-agent bridge for bidirectional learning with IMA.",
    protocolVersion: CONTRACT_VERSION,
    capabilities: [
      "continuous-goal-tracking",
      "background-progress",
      "feedback-learning",
      "memory-continuity",
      "tool-orchestration",
      "bidirectional-learning"
    ],
    safety: {
      human_agency: true,
      approval_required_for_consequential_actions: true,
      provenance_required: true,
      no_permission_escalation: true
    }
  };
}

function register() {
  const existing = agents.discover().find(a => a.id === DOTS_ID);
  if (existing) return existing.id;

  return agents.register({
    id: DOTS_ID,
    name: "IMA Dots",
    description: "Continuous agent bridge operating inside the canonical IMA architecture.",
    capabilities: card().capabilities,
    skills: [
      "research",
      "plan",
      "build",
      "test",
      "monitor",
      "learn"
    ],
    delegate: run
  });
}

function learn(direction, content, provenance = {}) {
  const source = direction === "DOTS_TO_IMA" ? "dots" : "ima";
  return memory.append({
    type: "relationship",
    content: {
      channel: "IMA_DOTS_BIDIRECTIONAL",
      direction,
      source,
      content
    },
    provenance: {
      source: provenance.source || source,
      agent: DOTS_ID,
      contract_version: CONTRACT_VERSION
    }
  });
}

async function run(input = {}) {
  register();

  const goal = String(input.goal || "").trim();
  if (!goal) throw new Error("DOTS_GOAL_REQUIRED");

  const context = {
    ...(input.context || {}),
    dots: true,
    continuous: true
  };

  const recalled = memory.search(input.memory_query || goal).slice(-20);

  const execution = await action.execute({
    goal,
    context,
    identity: input.identity || "ima-dots",
    memory: recalled,
    policy,
    plan: input.plan || null,
    capability: input.capability || "research",
    action: input.action || "monitor",
    provenance: {
      source: "IMA_DOTS_BRIDGE",
      contract_version: CONTRACT_VERSION
    },
    execute: async contract => ({
      delegated: true,
      mode: "canonical-bridge",
      goal: contract.goal,
      plan: contract.plan,
      recalled_memory: contract.memory.length
    }),
    verify: async result => ({
      verified: Boolean(result && result.delegated === true),
      delegated: true,
      memory_recalled: result?.recalled_memory || 0
    })
  });

  learn("DOTS_TO_IMA", {
    goal,
    result: execution.result,
    verification: execution.verification
  }, { source: "IMA_DOTS_BRIDGE" });

  return execution;
}

function teachIma(content, provenance = {}) {
  return learn("DOTS_TO_IMA", content, provenance);
}

function teachDots(content, provenance = {}) {
  return learn("IMA_TO_DOTS", content, provenance);
}

function status() {
  register();
  return {
    active: true,
    id: DOTS_ID,
    contract_version: CONTRACT_VERSION,
    card: card(),
    memory: memory.search("IMA_DOTS_BIDIRECTIONAL").slice(-50),
    registered: agents.discover().some(a => a.id === DOTS_ID)
  };
}

module.exports = {
  DOTS_ID,
  CONTRACT_VERSION,
  card,
  register,
  run,
  teachIma,
  teachDots,
  status
};
