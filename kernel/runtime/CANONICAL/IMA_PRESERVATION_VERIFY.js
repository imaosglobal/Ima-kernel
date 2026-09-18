const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const REGISTRY = path.join(
  ROOT,
  ".ima/runtime/continuity/preservation_registry.json"
);
const SEEDS = path.join(
  ROOT,
  ".ima/runtime/continuity/knowledge_seeds.jsonl"
);

function hash(value) {
  return crypto
    .createHash("sha256")
    .update(String(value), "utf8")
    .digest("hex");
}

function verify() {
  if (!fs.existsSync(REGISTRY)) {
    return {
      status: "UNAVAILABLE",
      reason: "REGISTRY_NOT_FOUND"
    };
  }

  const registry = JSON.parse(
    fs.readFileSync(REGISTRY, "utf8")
  );

  const seeds = new Map();

  if (fs.existsSync(SEEDS)) {
    for (const line of fs.readFileSync(SEEDS, "utf8").split("\n")) {
      if (!line.trim()) continue;

      try {
        const record = JSON.parse(line);
        if (record.artifact_id) {
          seeds.set(String(record.artifact_id), record);
        }
      } catch (_) {}
    }
  }

  const results = [];
  let verified = 0;
  let unavailable = 0;
  let mismatched = 0;

  for (const record of registry.records || []) {
    const seed = seeds.get(String(record.artifact_id));

    if (!seed) {
      unavailable++;
      results.push({
        artifact_id: record.artifact_id,
        status: "CONTENT_UNAVAILABLE"
      });
      continue;
    }

    /*
     * The seed registry stores the hash but deliberately does not
     * duplicate all source content. Therefore we can confirm that
     * the registered hash exists, but cannot recompute it unless
     * the original content is available.
     */
    if (!record.sha256) {
      mismatched++;
      results.push({
        artifact_id: record.artifact_id,
        status: "HASH_MISSING"
      });
      continue;
    }

    if (record.sha256 === seed.sha256) {
      verified++;
      results.push({
        artifact_id: record.artifact_id,
        status: "HASH_RECORD_MATCH"
      });
    } else {
      mismatched++;
      results.push({
        artifact_id: record.artifact_id,
        status: "HASH_RECORD_MISMATCH"
      });
    }
  }

  return {
    status: mismatched > 0 ? "INTEGRITY_ERROR" : "INTEGRITY_OK",
    total: (registry.records || []).length,
    verified,
    unavailable,
    mismatched,
    results
  };
}

if (require.main === module) {
  console.log(JSON.stringify(verify(), null, 2));
}

module.exports = { verify };
