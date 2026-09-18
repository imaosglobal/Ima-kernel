"use strict";

const { createContract, validateContract } =
  require("../IMA_CORE_CONTRACT");

async function execute(input = {}) {
  const contract = createContract({
    goal: input.goal || null,
    context: input.context || {},
    identity: input.identity || null,
    memory: input.memory || null,
    policy: input.policy || null,
    plan: input.plan || null,
    capability: input.capability || null,
    action: input.action || null,
    result: null,
    verification: null,
    learning: null,
    provenance: input.provenance || null
  });

  const validation = validateContract(contract);

  if (!validation.valid) {
    throw new Error(
      "INVALID_CONTRACT:" + validation.missing.join(",")
    );
  }

  let result = null;

  if (contract.policy && typeof contract.policy.allow === "function") {
    const decision = contract.policy.allow(
      contract.action,
      contract.context
    );

    if (!decision || decision.allowed !== true) {
      return {
        contract,
        result: null,
        verification: {
          verified: false,
          blocked: true,
          reason: decision?.reason || "POLICY_DENIED",
          approval_required: decision?.approval_required === true
        },
        executed_at: new Date().toISOString()
      };
    }
  }

  if (typeof input.execute === "function") {
    result = await input.execute(contract);
  }

  const verification =
    typeof input.verify === "function"
      ? await input.verify(result, contract)
      : {
          verified: false,
          reason: "NO_VERIFIER"
        };

  return {
    contract,
    result,
    verification,
    executed_at: new Date().toISOString()
  };
}

module.exports = {
  execute
};
