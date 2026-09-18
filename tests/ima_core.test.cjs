"use strict";

const assert = require("assert");

const core =
  require("../kernel/runtime/CANONICAL/IMA_CORE_CONTRACT");

const memory =
  require("../kernel/runtime/CANONICAL/memory/IMA_MEMORY");

const models =
  require("../kernel/runtime/CANONICAL/gateway/IMA_MODEL_GATEWAY");

const tools =
  require("../kernel/runtime/CANONICAL/gateway/IMA_TOOL_GATEWAY");

const agents =
  require("../kernel/runtime/CANONICAL/gateway/IMA_AGENT_GATEWAY");

const derivation =
  require("../kernel/runtime/CANONICAL/IMA_DERIVATION_REGISTRY");

const action =
  require("../kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE");

const selfHosted =
  require("../kernel/runtime/CANONICAL/IMA_SELF_HOSTED");

(async () => {
  const contract = core.createContract({
    goal: "test"
  });

  assert.equal(core.validateContract(contract).valid, true);

  const mem = memory.append({
    type: "working",
    content: {
      test: true
    },
    provenance: {
      source: "ima_core_test"
    }
  });

  assert.ok(mem.id);
  assert.ok(memory.list("working").length >= 1);

  models.register({
    id: "test-model",
    capabilities: ["generate"],
    async generate(input) {
      return {
        ok: true,
        input
      };
    }
  });

  assert.equal(models.list().length >= 1, true);

  tools.register({
    id: "test-tool",
    description: "test",
    capabilities: ["test"],
    async invoke(input) {
      return {
        ok: true,
        input
      };
    }
  });

  const toolResult = await tools.invoke("test-tool", {
    hello: "world"
  });

  assert.equal(toolResult.ok, true);

  agents.register({
    id: "test-agent",
    name: "IMA Test Agent",
    capabilities: ["test"],
    async delegate(task) {
      return {
        ok: true,
        task
      };
    }
  });

  assert.equal(agents.discover("test").length >= 1, true);

  const derivative = derivation.registerDerivative({
    original_artifact_id: "original",
    derivative_artifact_id: "derivative-test",
    content: "IMA",
    source_language: "he",
    target_language: "en"
  });

  assert.equal(derivation.verify(derivative.derivative_artifact_id).valid, true);

  const execution = await action.execute({
    goal: "integration-test",
    execute: async () => ({ ok: true }),
    verify: async result => ({
      verified: result.ok
    })
  });

  assert.equal(execution.verification.verified, true);

  const selfHostedReport = selfHosted.capabilityReport();

  assert.equal(selfHostedReport.mode, "SELF_HOSTED");
  assert.equal(selfHostedReport.network_required, false);
  assert.equal(selfHostedReport.credentials_required, false);

  selfHosted.registerCommandModel({
    id: "local-test-model",
    command: process.execPath,
    args: [
      "-e",
      "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>process.stdout.write(JSON.stringify({ok:true,received:JSON.parse(s)})))"
    ]
  });

  const localExecution = await selfHosted.run({
    goal: "local-independence-test",
    provider_id: "local-test-model",
    action: "monitor"
  });

  assert.equal(localExecution.verification.verified, true);
  assert.equal(localExecution.result.output.ok, true);

  const deniedExecution = await selfHosted.run({
    goal: "policy-test",
    provider_id: "local-test-model",
    action: "unknown-action"
  });

  assert.equal(deniedExecution.verification.blocked, true);
  assert.equal(deniedExecution.verification.verified, false);

  console.log("IMA_CORE_TEST=PASS");
})().catch(error => {
  console.error(error);
  process.exit(1);
});
