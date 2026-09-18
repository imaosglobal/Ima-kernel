const fs = require("fs");
const path = require("path");
const vault = require("./IMA_ARTIFACT_VAULT");

const ROOT = path.resolve(__dirname, "../../..");

const SEEDS = path.join(
  ROOT,
  ".ima/runtime/continuity/knowledge_seeds.jsonl"
);

const PROVENANCE = path.join(
  ROOT,
  "learning/provenance_memory.json"
);

function migrate() {
  if (!fs.existsSync(SEEDS)) {
    return {
      status: "UNAVAILABLE",
      reason: "SEEDS_NOT_FOUND"
    };
  }

  const provenance = fs.existsSync(PROVENANCE)
    ? JSON.parse(fs.readFileSync(PROVENANCE, "utf8"))
    : {};

  let preserved = 0;
  let already = 0;
  let unavailable = 0;
  const results = [];

  for (const line of fs.readFileSync(SEEDS, "utf8").split("\n")) {
    if (!line.trim()) continue;

    let seed;
    try {
      seed = JSON.parse(line);
    } catch (_) {
      continue;
    }

    let content = null;

    if (
      String(seed.artifact_id).startsWith("provenance:")
    ) {
      const knowledgeId = String(seed.artifact_id).slice(
        "provenance:".length
      );

      if (
        provenance[knowledgeId] &&
        provenance[knowledgeId].content !== undefined
      ) {
        content = provenance[knowledgeId].content;
      }
    }

    /*
     * The canonical continuity seed was originally registered
     * with a hash but its source text was not persisted.
     * Restore the exact canonical text used to create that hash.
     */
    if (
      seed.artifact_id ===
      "ima-intergenerational-continuity-001"
    ) {
      content =
`Knowledge should remain recoverable across generations.
Original works must never be overwritten by translations or derivatives.
Every derivative must retain provenance and its parent artifact.
Human agency remains with humans.
IMA should preserve knowledge while remaining portable across changing models, platforms and formats.`;
    }

    if (content === null) {
      unavailable++;
      results.push({
        artifact_id: seed.artifact_id,
        status: "CONTENT_UNAVAILABLE"
      });
      continue;
    }

    const result = vault.preserve({
      artifact_id: seed.artifact_id,
      title: seed.title,
      creator: seed.creator,
      source_language: seed.source_language,
      content,
      creation_date: seed.creation_date,
      parent_artifact: seed.parent_artifact,
      derivation_type: seed.derivation_type,
      license: seed.license,
      verification_status: seed.verification_status
    });

    if (result.status === "ALREADY_PRESERVED") {
      already++;
    } else {
      preserved++;
    }

    const verification = vault.verify(
      seed.artifact_id,
      seed.sha256
    );

    results.push({
      artifact_id: seed.artifact_id,
      preservation: result.status,
      verification
    });
  }

  return {
    status: "MIGRATION_COMPLETE",
    preserved,
    already,
    unavailable,
    total: preserved + already + unavailable,
    results
  };
}

if (require.main === module) {
  console.log(JSON.stringify(migrate(), null, 2));
  console.log(JSON.stringify(vault.status(), null, 2));
}

module.exports = { migrate };
