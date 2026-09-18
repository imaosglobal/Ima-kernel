const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const DIR = path.join(ROOT, ".ima/runtime/continuity");
const INDEX = path.join(DIR, "portable_artifact_index.json");
const DERIVATIONS = path.join(DIR, "derivation_registry.json");
const ARTIFACTS = path.join(DIR, "artifacts/derivatives");

function sha256(value) {
  return crypto.createHash("sha256").update(String(value), "utf8").digest("hex");
}

function load() {
  if (!fs.existsSync(DERIVATIONS)) {
    return {
      schema: "IMA-DERIVATION-REGISTRY-1.0",
      originals_never_overwritten: true,
      translations_are_derivatives: true,
      records: []
    };
  }
  return JSON.parse(fs.readFileSync(DERIVATIONS, "utf8"));
}

function save(registry) {
  fs.mkdirSync(DIR, { recursive: true });
  registry.records.sort((a, b) =>
    a.derivation_id.localeCompare(b.derivation_id)
  );
  fs.writeFileSync(
    DERIVATIONS,
    JSON.stringify(registry, null, 2),
    "utf8"
  );
}

function build() {
  if (!fs.existsSync(INDEX)) {
    throw new Error("PORTABLE_ARTIFACT_INDEX_NOT_FOUND");
  }

  const index = JSON.parse(fs.readFileSync(INDEX, "utf8"));
  const registry = load();
  const known = new Set(registry.records.map(r => r.derivation_id));

  for (const parent of index.records) {
    if (parent.derivation_type !== "original") continue;

    const derivation_id =
      "ima:derivation:" +
      sha256(parent.portable_artifact_id + ":derivation-policy-1");

    if (!known.has(derivation_id)) {
      registry.records.push({
        derivation_id,
        parent_artifact: parent.portable_artifact_id,
        parent_sha256: parent.sha256,
        source_language: parent.source_language,
        derivation_type: "translation_or_derivative",
        target_language: null,
        translator: null,
        translation_date: null,
        methodology: null,
        model: null,
        model_version: null,
        sha256: null,
        content_file: null,
        verification_status: "awaiting_derivative",
        original_preserved: true
      });
    }
  }

  save(registry);

  return {
    status: "DERIVATION_REGISTRY_BUILT",
    records: registry.records.length,
    path: DERIVATIONS
  };
}

function registerDerivative({
  parent_artifact,
  target_language,
  content,
  translator = null,
  translation_date = new Date().toISOString(),
  methodology = null,
  model = null,
  model_version = null,
  derivation_type = "translation"
}) {
  if (!parent_artifact || !target_language || content == null) {
    throw new Error("DERIVATIVE_PARENT_LANGUAGE_CONTENT_REQUIRED");
  }

  const registry = load();

  const parent = registry.records.find(
    r => r.parent_artifact === parent_artifact
  );

  if (!parent) {
    throw new Error("PARENT_ARTIFACT_NOT_REGISTERED");
  }

  if (!parent.original_preserved) {
    throw new Error("ORIGINAL_PRESERVATION_REQUIRED");
  }

  const contentHash = sha256(content);
  const derivation_id =
    "ima:derivative:" +
    sha256(
      parent_artifact +
      ":" +
      target_language +
      ":" +
      contentHash
    );

  fs.mkdirSync(ARTIFACTS, { recursive: true });

  const contentFile = path.join(
    ARTIFACTS,
    `${contentHash}.txt`
  );

  if (!fs.existsSync(contentFile)) {
    fs.writeFileSync(
      contentFile,
      String(content),
      { encoding: "utf8", flag: "wx" }
    );
  }

  const existing = registry.records.find(
    r => r.derivation_id === derivation_id
  );

  if (!existing) {
    registry.records.push({
      derivation_id,
      parent_artifact,
      parent_sha256: parent.parent_sha256,
      source_language: parent.source_language,
      derivation_type,
      target_language,
      translator,
      translation_date,
      methodology,
      model,
      model_version,
      sha256: contentHash,
      content_file: path.relative(ROOT, contentFile),
      verification_status: "verified",
      original_preserved: true
    });

    save(registry);
  }

  return {
    status: "DERIVATIVE_REGISTERED",
    derivation_id,
    parent_artifact,
    target_language,
    sha256: contentHash,
    content_file: path.relative(ROOT, contentFile),
    original_preserved: true
  };
}

function verify() {
  if (!fs.existsSync(DERIVATIONS)) {
    return { status: "DERIVATION_REGISTRY_NOT_FOUND" };
  }

  const registry = JSON.parse(
    fs.readFileSync(DERIVATIONS, "utf8")
  );

  let valid = 0;
  let invalid = 0;
  const results = [];

  for (const record of registry.records) {
    const structural =
      record.parent_artifact &&
      record.original_preserved === true &&
      record.derivation_type === "translation_or_derivative" ||
      record.derivation_type === "translation";

    if (!structural) {
      invalid++;
      results.push({
        derivation_id: record.derivation_id,
        status: "INVALID_STRUCTURE"
      });
      continue;
    }

    if (record.verification_status === "awaiting_derivative") {
      valid++;
      results.push({
        derivation_id: record.derivation_id,
        status: "AWAITING_DERIVATIVE"
      });
      continue;
    }

    if (!record.content_file || !record.sha256) {
      invalid++;
      results.push({
        derivation_id: record.derivation_id,
        status: "MISSING_CONTENT_HASH"
      });
      continue;
    }

    const file = path.join(ROOT, record.content_file);

    if (!fs.existsSync(file)) {
      invalid++;
      results.push({
        derivation_id: record.derivation_id,
        status: "CONTENT_MISSING"
      });
      continue;
    }

    const actual = sha256(
      fs.readFileSync(file, "utf8")
    );

    if (actual !== record.sha256) {
      invalid++;
      results.push({
        derivation_id: record.derivation_id,
        status: "CONTENT_HASH_MISMATCH"
      });
      continue;
    }

    valid++;
    results.push({
      derivation_id: record.derivation_id,
      status: "VERIFIED"
    });
  }

  return {
    status: invalid
      ? "DERIVATION_REGISTRY_INTEGRITY_ERROR"
      : "DERIVATION_REGISTRY_INTEGRITY_OK",
    total: registry.records.length,
    valid,
    invalid,
    results
  };
}

if (require.main === module) {
  console.log(JSON.stringify(build(), null, 2));
  console.log(JSON.stringify(verify(), null, 2));
}

module.exports = {
  build,
  registerDerivative,
  verify
};
