"use strict";

const { spawn } = require("child_process");

const models = require("./gateway/IMA_MODEL_GATEWAY");
const memory = require("./memory/IMA_MEMORY");
const policy = require("./IMA_POLICY");
const action = require("./orchestration/IMA_ACTION_ENGINE");

function runCommand(command, args, input, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args || [], {
      cwd: options.cwd || process.cwd(),
      env: options.env || process.env,
      stdio: ["pipe", "pipe", "pipe"],
      shell: false
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", chunk => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", chunk => {
      stderr += chunk.toString();
    });

    child.on("error", reject);

    child.on("close", code => {
      if (code !== 0) {
        const error = new Error(
          "LOCAL_MODEL_COMMAND_FAILED:" + code
        );
        error.stderr = stderr;
        reject(error);
        return;
      }

      resolve(stdout.trim());
    });

    child.stdin.end(JSON.stringify(input || {}));
  });
}

function registerCommandModel(config = {}) {
  if (!config.id || !config.command) {
    throw new Error("INVALID_LOCAL_MODEL_CONFIG");
  }

  const provider = {
    id: config.id,
    capabilities: config.capabilities || ["generate"],

    async generate(request) {
      const output = await runCommand(
        config.command,
        config.args || [],
        request,
        config
      );

      let parsed = output;

      try {
        parsed = JSON.parse(output);
      } catch (_) {}

      return {
        provider: config.id,
        mode: "local-command",
        output: parsed
      };
    }
  };

  models.register(provider);
  return config.id;
}

function capabilityReport() {
  return {
    mode: "SELF_HOSTED",
    network_required: false,
    credentials_required: false,
    model_providers: models.list(),
    memory: memory.status(),
    policy: {
      safe_actions: policy.SAFE_ACTIONS,
      approval_required: policy.APPROVAL_REQUIRED
    }
  };
}

async function run(input = {}) {
  const goal = input.goal || "";
  const providerId = input.provider_id || null;

  const remembered = memory
    .search(input.memory_query || goal)
    .slice(-20);

  const execution = await action.execute({
    goal,
    context: input.context || {},
    identity: input.identity || "local-user",
    memory: remembered,
    policy,
    plan: input.plan || null,
    capability: input.capability || "generate",
    action: input.action || "monitor",

    provenance: {
      source: "IMA_SELF_HOSTED",
      provider: providerId
    },

    execute: async contract => {
      if (!providerId) {
        return {
          executed: false,
          reason: "NO_LOCAL_MODEL_PROVIDER",
          contract_goal: contract.goal
        };
      }

      return models.generate(providerId, {
        goal: contract.goal,
        context: contract.context,
        memory: contract.memory,
        plan: contract.plan
      });
    },

    verify: async result => ({
      verified: Boolean(result),
      local: true
    })
  });

  memory.append({
    type: "episodic",
    content: {
      goal,
      provider: providerId,
      verified: execution.verification?.verified === true
    },
    provenance: {
      source: "IMA_SELF_HOSTED"
    }
  });

  return execution;
}

module.exports = {
  registerCommandModel,
  capabilityReport,
  run
};
