#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CANON="$ROOT/kernel/runtime/CANONICAL"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP="$ROOT/.ima/backup_before_report_$TS"

echo "=== IMA REPORT IMPLEMENTATION ==="
echo "[IMA] root: $ROOT"

mkdir -p "$CANON" "$BACKUP"

backup_file() {
  local f="$1"
  if [ -f "$f" ]; then
    mkdir -p "$BACKUP/$(dirname "${f#$ROOT/}")"
    cp -p "$f" "$BACKUP/${f#$ROOT/}"
  fi
}

echo "[IMA] creating backup..."
backup_file "$CANON/IMA_POLICY.js"
backup_file "$CANON/IMA_RUNTIME.js"
backup_file "$CANON/IMA_PRESERVATION_VERIFY.js"
backup_file "$CANON/IMA_DERIVATION_REGISTRY.js"
backup_file "$ROOT/package.json"
backup_file "$ROOT/README.md"

mkdir -p \
  "$CANON/memory" \
  "$CANON/gateway" \
  "$CANON/orchestration" \
  "$ROOT/tests"

cat > "$CANON/package.json" <<'EOF'
{
  "name": "ima-canonical-runtime",
  "private": true,
  "type": "commonjs"
}
EOF

cat > "$CANON/IMA_CORE_CONTRACT.js" <<'EOF'
"use strict";

const REQUIRED_FIELDS = Object.freeze([
  "goal",
  "context",
  "identity",
  "memory",
  "policy",
  "plan",
  "capability",
  "action",
  "result",
  "verification",
  "learning",
  "provenance"
]);

function createContract(input = {}) {
  const contract = {};

  for (const field of REQUIRED_FIELDS) {
    contract[field] = Object.prototype.hasOwnProperty.call(input, field)
      ? input[field]
      : null;
  }

  contract.created_at = new Date().toISOString();
  return Object.freeze(contract);
}

function validateContract(contract) {
  const missing = REQUIRED_FIELDS.filter(
    field => !Object.prototype.hasOwnProperty.call(contract || {}, field)
  );

  return {
    valid: missing.length === 0,
    missing
  };
}

module.exports = {
  REQUIRED_FIELDS,
  createContract,
  validateContract
};
EOF

cat > "$CANON/memory/IMA_MEMORY.js" <<'EOF'
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const DIR = path.join(ROOT, ".ima", "runtime", "memory");
const FILE = path.join(DIR, "memory.jsonl");

const TYPES = Object.freeze([
  "working",
  "episodic",
  "semantic",
  "personal",
  "artifact",
  "relationship"
]);

function ensure() {
  fs.mkdirSync(DIR, { recursive: true });
  if (!fs.existsSync(FILE)) fs.writeFileSync(FILE, "", "utf8");
}

function idFor(record) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(record))
    .digest("hex");
}

function append(input) {
  if (!input || !TYPES.includes(input.type)) {
    throw new Error("Invalid memory type");
  }

  ensure();

  const record = {
    id: idFor({
      type: input.type,
      content: input.content,
      provenance: input.provenance || null
    }),
    type: input.type,
    content: input.content,
    provenance: input.provenance || null,
    status: input.status || "active",
    created_at: new Date().toISOString()
  };

  fs.appendFileSync(FILE, JSON.stringify(record) + "\n", "utf8");
  return record;
}

function list(type = null) {
  ensure();

  return fs.readFileSync(FILE, "utf8")
    .split("\n")
    .filter(Boolean)
    .map(line => JSON.parse(line))
    .filter(record => !type || record.type === type);
}

function search(query) {
  const q = String(query || "").toLowerCase();

  return list().filter(record =>
    JSON.stringify(record).toLowerCase().includes(q)
  );
}

function status() {
  return {
    file: FILE,
    types: TYPES.slice(),
    records: list().length
  };
}

module.exports = {
  TYPES,
  append,
  list,
  search,
  status
};
EOF

cat > "$CANON/gateway/IMA_MODEL_GATEWAY.js" <<'EOF'
"use strict";

const providers = new Map();

function register(provider) {
  if (!provider || !provider.id || typeof provider.generate !== "function") {
    throw new Error("Invalid model provider");
  }

  providers.set(provider.id, provider);
  return provider.id;
}

function list() {
  return [...providers.values()].map(provider => ({
    id: provider.id,
    capabilities: provider.capabilities || []
  }));
}

async function generate(providerId, request) {
  const provider = providers.get(providerId);

  if (!provider) {
    throw new Error(`Unknown model provider: ${providerId}`);
  }

  return provider.generate(request);
}

module.exports = {
  register,
  list,
  generate
};
EOF

cat > "$CANON/gateway/IMA_TOOL_GATEWAY.js" <<'EOF'
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
EOF

cat > "$CANON/gateway/IMA_AGENT_GATEWAY.js" <<'EOF'
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
EOF

cat > "$CANON/orchestration/IMA_ACTION_ENGINE.js" <<'EOF'
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
EOF

cat > "$CANON/IMA_SYSTEM_INTEGRITY.js" <<'EOF'
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../..");

const required = [
  "IMA_CORE_CONTRACT.js",
  "IMA_POLICY.js",
  "IMA_RUNTIME.js",
  "IMA_CONTINUITY.js",
  "IMA_PRESERVATION_VERIFY.js",
  "IMA_DERIVATION_REGISTRY.js",
  "memory/IMA_MEMORY.js",
  "gateway/IMA_MODEL_GATEWAY.js",
  "gateway/IMA_TOOL_GATEWAY.js",
  "gateway/IMA_AGENT_GATEWAY.js",
  "orchestration/IMA_ACTION_ENGINE.js"
];

const missing = required.filter(file =>
  !fs.existsSync(path.join(__dirname, file))
);

const result = {
  valid: missing.length === 0,
  canonical_root: __dirname,
  missing
};

console.log(JSON.stringify(result, null, 2));

if (!result.valid) process.exit(1);
EOF

cat > "$CANON/IMA_PRESERVATION_VERIFY.js" <<'EOF'
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function sha256File(file) {
  return crypto
    .createHash("sha256")
    .update(fs.readFileSync(file))
    .digest("hex");
}

function verifyArtifact(record, root) {
  if (!record || !record.content_file) {
    return {
      status: "UNAVAILABLE",
      reason: "content_file_missing"
    };
  }

  const file = path.resolve(root, record.content_file);

  if (!fs.existsSync(file)) {
    return {
      status: "UNAVAILABLE",
      reason: "content_not_found",
      file
    };
  }

  const actual = sha256File(file);
  const expected = record.sha256 || record.hash || null;

  if (!expected) {
    return {
      status: "NO_EXPECTED_HASH",
      actual
    };
  }

  return {
    status: actual === expected ? "VERIFIED" : "MISMATCH",
    expected,
    actual,
    file
  };
}

function verifyRegistry(registry, root) {
  const records = Array.isArray(registry)
    ? registry
    : registry?.artifacts || [];

  return records.map(record => ({
    artifact_id: record.artifact_id || record.id || null,
    ...verifyArtifact(record, root)
  }));
}

module.exports = {
  sha256File,
  verifyArtifact,
  verifyRegistry
};
EOF

cat > "$CANON/IMA_DERIVATION_REGISTRY.js" <<'EOF'
"use strict";

const crypto = require("crypto");

const records = new Map();

function hashContent(content) {
  return crypto
    .createHash("sha256")
    .update(String(content), "utf8")
    .digest("hex");
}

function validate(record) {
  return Boolean(
    record &&
    record.original_artifact_id &&
    record.derivative_artifact_id &&
    record.content !== undefined
  );
}

function registerDerivative(input) {
  if (!validate(input)) {
    throw new Error("INVALID_DERIVATION_RECORD");
  }

  const contentHash = hashContent(input.content);

  const record = {
    original_artifact_id: input.original_artifact_id,
    derivative_artifact_id: input.derivative_artifact_id,
    source_language: input.source_language || null,
    target_language: input.target_language || null,
    derivation_type: input.derivation_type || "translation",
    content_hash: contentHash,
    content: String(input.content),
    created_at: new Date().toISOString()
  };

  records.set(record.derivative_artifact_id, record);
  return { ...record };
}

function verify(id) {
  const record = records.get(id);

  if (!record) {
    return {
      valid: false,
      reason: "NOT_FOUND"
    };
  }

  const actual = hashContent(record.content);

  return {
    valid: actual === record.content_hash,
    expected: record.content_hash,
    actual
  };
}

function list() {
  return [...records.values()].map(record => ({
    ...record,
    content: undefined
  }));
}

module.exports = {
  hashContent,
  validate,
  registerDerivative,
  verify,
  list
};
EOF

cat > "$ROOT/tests/ima_core.test.js" <<'EOF'
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

  console.log("IMA_CORE_TEST=PASS");
})().catch(error => {
  console.error(error);
  process.exit(1);
});
EOF

echo "[IMA] adding safe npm scripts..."

if [ -f "$ROOT/package.json" ]; then
  node <<'NODE'
const fs = require("fs");
const file = "package.json";
const pkg = JSON.parse(fs.readFileSync(file, "utf8"));
pkg.scripts = pkg.scripts || {};
pkg.scripts.test = "node tests/ima_core.test.js";
pkg.scripts["ima:integrity"] =
  "node kernel/runtime/CANONICAL/IMA_SYSTEM_INTEGRITY.js";
pkg.scripts["ima:runtime"] =
  "node kernel/runtime/CANONICAL/IMA_RUNTIME.js";
fs.writeFileSync(file, JSON.stringify(pkg, null, 2) + "\n");
NODE
else
  cat > "$ROOT/package.json" <<'EOF'
{
  "private": true,
  "scripts": {
    "test": "node tests/ima_core.test.js",
    "ima:integrity": "node kernel/runtime/CANONICAL/IMA_SYSTEM_INTEGRITY.js",
    "ima:runtime": "node kernel/runtime/CANONICAL/IMA_RUNTIME.js"
  }
}
EOF
fi

echo "[IMA] checking syntax..."

node --check "$CANON/IMA_CORE_CONTRACT.js"
node --check "$CANON/memory/IMA_MEMORY.js"
node --check "$CANON/gateway/IMA_MODEL_GATEWAY.js"
node --check "$CANON/gateway/IMA_TOOL_GATEWAY.js"
node --check "$CANON/gateway/IMA_AGENT_GATEWAY.js"
node --check "$CANON/orchestration/IMA_ACTION_ENGINE.js"
node --check "$CANON/IMA_SYSTEM_INTEGRITY.js"
node --check "$CANON/IMA_PRESERVATION_VERIFY.js"
node --check "$CANON/IMA_DERIVATION_REGISTRY.js"

echo "[IMA] running system integrity..."
node "$CANON/IMA_SYSTEM_INTEGRITY.js"

echo "[IMA] running core tests..."
node "$ROOT/tests/ima_core.test.js"

echo "[IMA] git diff summary..."
git -C "$ROOT" status --short

echo "=== IMA REPORT IMPLEMENTATION COMPLETE LOCALLY ==="
echo "BACKUP=$BACKUP"
echo "NEXT=review git diff, then commit/push"
