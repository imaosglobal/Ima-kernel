const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const DIR = path.join(ROOT, ".ima/runtime/continuity");
const REGISTRY = path.join(DIR, "preservation_registry.json");

function ensure() {
  fs.mkdirSync(DIR, { recursive: true });
}

function sha256(content) {
  return crypto.createHash("sha256")
    .update(String(content), "utf8")
    .digest("hex");
}

function load() {
  ensure();

  if (!fs.existsSync(REGISTRY)) {
    const initial = {
      schema: "IMA-PRESERVATION-REGISTRY-1.0",
      system: "IMA",
      originals_never_overwritten: true,
      translations_are_derivatives: true,
      provenance_required: true,
      sha256_required: true,
      records: []
    };

    fs.writeFileSync(
      REGISTRY,
      JSON.stringify(initial, null, 2),
      "utf8"
    );

    return initial;
  }

  return JSON.parse(fs.readFileSync(REGISTRY, "utf8"));
}

function verifyRecord(record) {
  if (!record || !record.artifact_id || !record.sha256) {
    return {
      valid: false,
      reason: "MISSING_REQUIRED_ID_OR_HASH"
    };
  }

  return {
    valid: true,
    artifact_id: record.artifact_id,
    sha256: record.sha256
  };
}

function importContinuitySeeds() {
  const seeds = path.join(DIR, "knowledge_seeds.jsonl");
  const registry = load();

  if (!fs.existsSync(seeds)) {
    return {
      imported: 0,
      skipped: 0,
      reason: "SEED_FILE_NOT_FOUND"
    };
  }

  const existing = new Set(
    registry.records.map(r => String(r.artifact_id))
  );

  let imported = 0;
  let skipped = 0;

  for (const line of fs.readFileSync(seeds, "utf8").split("\n")) {
    if (!line.trim()) continue;

    let seed;
    try {
      seed = JSON.parse(line);
    } catch (_) {
      skipped++;
      continue;
    }

    if (!seed.artifact_id || existing.has(String(seed.artifact_id))) {
      skipped++;
      continue;
    }

    const record = {
      artifact_id: String(seed.artifact_id),
      title: seed.title || null,
      creator: seed.creator || null,

      creation_date:
        seed.original_creation_date ||
        seed.creation_date ||
        null,

      source_language: seed.source_language || null,
      file_format: seed.file_format || null,
      sha256: seed.sha256 || null,

      parent_artifact:
        seed.parent_artifact ||
        null,

      derivation_type:
        seed.derivation_type ||
        "original",

      license:
        seed.license ||
        null,

      verification_status:
        seed.verification_status ||
        "unverified",

      source:
        seed.source ||
        null,

      preserved_at:
        seed.preserved_at ||
        Date.now(),

      imported_at:
        Date.now()
    };

    const verification = verifyRecord(record);

    if (!verification.valid) {
      skipped++;
      continue;
    }

    registry.records.push(record);
    existing.add(record.artifact_id);
    imported++;
  }

  fs.writeFileSync(
    REGISTRY,
    JSON.stringify(registry, null, 2),
    "utf8"
  );

  return {
    imported,
    skipped,
    total_records: registry.records.length,
    registry: REGISTRY
  };
}

function status() {
  const registry = load();

  return {
    enabled: true,
    schema: registry.schema,
    records: registry.records.length,
    originals_never_overwritten:
      registry.originals_never_overwritten,
    translations_are_derivatives:
      registry.translations_are_derivatives,
    provenance_required:
      registry.provenance_required,
    sha256_required:
      registry.sha256_required,
    registry_path: REGISTRY
  };
}

module.exports = {
  load,
  importContinuitySeeds,
  verifyRecord,
  status,
  sha256
};

if (require.main === module) {
  console.log(
    JSON.stringify(importContinuitySeeds(), null, 2)
  );

  console.log(
    JSON.stringify(status(), null, 2)
  );
}
