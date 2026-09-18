const fs = require("fs");
const path = require("path");
const continuity = require("./IMA_CONTINUITY");

const ROOT = path.resolve(__dirname, "../../..");
const PROVENANCE = path.join(ROOT, "learning/provenance_memory.json");

function ingestExistingProvenance() {
  if (!fs.existsSync(PROVENANCE)) {
    return {
      available: false,
      imported: 0,
      skipped: 0,
      reason: "PROVENANCE_FILE_NOT_FOUND"
    };
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(PROVENANCE, "utf8"));
  } catch (error) {
    return {
      available: false,
      imported: 0,
      skipped: 0,
      reason: "PROVENANCE_JSON_INVALID"
    };
  }

  if (!data || typeof data !== "object") {
    return {
      available: false,
      imported: 0,
      skipped: 0,
      reason: "PROVENANCE_DATA_INVALID"
    };
  }

  const seedFile = path.join(
    ROOT,
    ".ima/runtime/continuity/knowledge_seeds.jsonl"
  );

  const existing = new Set();

  if (fs.existsSync(seedFile)) {
    for (const line of fs.readFileSync(seedFile, "utf8").split("\n")) {
      if (!line.trim()) continue;
      try {
        const record = JSON.parse(line);
        if (record.artifact_id) existing.add(String(record.artifact_id));
      } catch (_) {}
    }
  }

  let imported = 0;
  let skipped = 0;

  for (const [knowledgeId, entry] of Object.entries(data)) {
    const artifactId = `provenance:${knowledgeId}`;

    if (existing.has(artifactId)) {
      skipped++;
      continue;
    }

    if (!entry || typeof entry !== "object") {
      skipped++;
      continue;
    }

    if (entry.content === undefined || entry.content === null) {
      skipped++;
      continue;
    }

    continuity.registerSeed({
      artifact_id: artifactId,
      title: `Provenance ${knowledgeId}`,
      creator: null,
      source_language: null,
      content: String(entry.content),
      source: entry.source || "IMA provenance store",
      parent_artifact: null,
      derivation_type: "provenance_record",
      license: null,
      verification_status: entry.validation ? "provenance_recorded" : "unverified"
    });

    imported++;
  }

  return {
    available: true,
    imported,
    skipped,
    source: "learning/provenance_memory.json",
    originals_unchanged: true
  };
}

if (require.main === module) {
  console.log(JSON.stringify(ingestExistingProvenance(), null, 2));
}

module.exports = { ingestExistingProvenance };
