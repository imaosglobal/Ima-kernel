"use strict";

const tools = new Map();

function register(tool) {
  if (!tool || !tool.id || typeof tool.invoke !== "function") {
    throw new Error("Invalid tool");
  }

  tools.set(tool.id, tool);
  return tool.id;
}

function discover(capability = null) {
  return [...tools.values()]
    .filter(tool =>
      !capability ||
      (tool.capabilities || []).includes(capability)
    )
    .map(tool => ({
      id: tool.id,
      description: tool.description || "",
      capabilities: tool.capabilities || []
    }));
}

async function invoke(id, input, policy = null) {
  const tool = tools.get(id);

  if (!tool) {
    throw new Error(`Unknown tool: ${id}`);
  }

  if (policy && typeof policy.allow === "function") {
    const decision = policy.allow({
      action: id,
      input
    });

    if (decision === false || decision?.allowed === false) {
      throw new Error("POLICY_DENIED");
    }
  }

  return tool.invoke(input);
}

module.exports = {
  register,
  discover,
  invoke
};
