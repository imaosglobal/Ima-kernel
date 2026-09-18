"use strict";

const agents = new Map();

function register(agent) {
  if (!agent || !agent.id || !agent.name) {
    throw new Error("Invalid agent");
  }

  agents.set(agent.id, {
    ...agent,
    registered_at: new Date().toISOString()
  });

  return agent.id;
}

function discover(capability = null) {
  return [...agents.values()]
    .filter(agent =>
      !capability ||
      (agent.capabilities || []).includes(capability)
    );
}

function agentCard(agent) {
  return {
    name: agent.name,
    description: agent.description || "",
    url: agent.url || null,
    protocolVersion: "1.0.0",
    capabilities: agent.capabilities || [],
    skills: agent.skills || []
  };
}

async function delegate(id, task) {
  const agent = agents.get(id);

  if (!agent) {
    throw new Error(`Unknown agent: ${id}`);
  }

  if (typeof agent.delegate !== "function") {
    throw new Error("AGENT_DELEGATION_UNAVAILABLE");
  }

  return agent.delegate(task);
}

module.exports = {
  register,
  discover,
  agentCard,
  delegate
};
