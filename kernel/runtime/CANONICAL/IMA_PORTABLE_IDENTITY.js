const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const CONTINUITY = path.join(ROOT, ".ima/runtime/continuity");
const SEEDS = path.join(CONTINUITY, "knowledge_seeds.jsonl");
const CONTENT_INDEX = path.join(CONTINUITY, "content_address_index.json");
const PORTABLE_INDEX = path.join(CONTINUITY, "portable_artifact_index.json");

function stableId(value) {
  return crypto
    .createHash("sha256")
    .update(String(value), "utf8")
    .digest("hex");
}

function ensureContinuityDirectory() {
  fs.mkdirSync(CONTINUITY, { recursive: true });
}

function writeEmptyContinuityState() {
  ensureContinuityDirectory();

  if (!fs.existsSync(SEEDS)) {
    fs.writeFileSync(SEEDS, "", "utf8");
  }

  if (!fs.existsSync(CONTENT_INDEX)) {
    fs.writeFileSync(
      CONTENT_INDEX,
      JSON.stringify({
        schema: "IMA-CONTENT-ADDRESS-INDEX-1.0",
        algorithm: "SHA-256",
        records: []
      }, null, 2),
      "utf8"
    );
  }
}

function build() {
  ensureContinuityDirectory();

  // CI, fresh clones and new installations legitimately start without
  // mutable continuity state. Bootstrap an empty, truthful state instead
  // of treating missing runtime state as a code failure.
  if (!fs.existsSync(SEEDS) && !fs.existsSync(CONTENT_INDEX)) {
    writeEmptyContinuityState();
  }

  if (!fs.existsSync(SEEDS)) {
    throw new Error("CONTINUITY_SEEDS_NOT_FOUND");
  }

  if (!fs.existsSync(CONTENT_INDEX)) {
    throw new Error("CONTENT_ADDRESS_INDEX_NOT_FOUND");
  }

  const seedLines = fs.readFileSync(SEEDS, "utf8")
    .split("\n")
    .map(line => line.trim())
    .filter(Boolean)
    .map(line => JSON.parse(line));

  const contentIndex = JSON.parse(
    fs.readFileSync(CONTENT_INDEX, "utf8")
  );

  const recordsIndex = Array.isArray(contentIndex.records)
    ? contentIndex.records
    : [];

  const byHash = new Map(
    recordsIndex.map(record => [record.sha256, record])
  );

  const records = seedLines.map(seed => {
    const content = byHash.get(seed.sha256);

    if (!content) {
      throw new Error(
        "CONTENT_OBJECT_NOT_FOUND:" + seed.artifact_id
      );
    }

    return {
      portable_artifact_id:
        "ima:" + stableId(seed.artifact_id),

      artifact_id: seed.artifact_id,

      sha256: seed.sha256,

      content_address:
        "sha256:" + seed.sha256,

      content_file:
        content.content_file,

      title: seed.title || null,
      creator: seed.creator || null,
      source_language: seed.source_language || null,
      creation_date: seed.creation_date || null,
      parent_artifact: seed.parent_artifact || null,
      derivation_type: seed.derivation_type || "original",
      license: seed.license || null,
      verification_status: seed.verification_status || null,

      identity_rule:
        "portable identity is independent of filename, filesystem encoding and platform"
    };
  });

  const output = {
    schema: "IMA-PORTABLE-ARTIFACT-IDENTITY-1.0",
    system: "IMA",
    algorithm: "SHA-256",
    filename_independent: true,
    unicode_filename_independent: true,
    platform_independent: true,
    originals_never_overwritten: true,
    records
  };

  fs.writeFileSync(
    PORTABLE_INDEX,
    JSON.stringify(output, null, 2),
    "utf8"
  );

  return {
    status: "PORTABLE_IDENTITY_BUILT",
    records: records.length,
    bootstrapped: seedLines.length === 0,
    path: PORTABLE_INDEX
  };
}

function verify() {
  if (!fs.existsSync(PORTABLE_INDEX)) {
    return { status: "PORTABLE_INDEX_NOT_FOUND" };
  }

  const index = JSON.parse(
    fs.readFileSync(PORTABLE_INDEX, "utf8")
  );

  let verified = 0;
  let missing = 0;
  let mismatched = 0;

  for (const record of index.records) {
    const file = path.join(ROOT, record.content_file);

    if (!fs.existsSync(file)) {
      missing++;
      continue;
    }

    const actual = crypto
      .createHash("sha256")
      .update(fs.readFileSync(file, "utf8"), "utf8")
      .digest("hex");

    if (actual === record.sha256) {
      verified++;
    } else {
      mismatched++;
    }
  }

  return {
    status:
      missing || mismatched
        ? "PORTABLE_IDENTITY_INTEGRITY_ERROR"
        : "PORTABLE_IDENTITY_INTEGRITY_OK",
    total: index.records.length,
    verified,
    missing,
    mismatched
  };
}

if (require.main === module) {
  console.log(JSON.stringify(build(), null, 2));
  console.log(JSON.stringify(verify(), null, 2));
}

module.exports = { build, verify };
