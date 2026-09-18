const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const DIR = path.join(ROOT, ".ima/runtime/continuity");
const SEEDS = path.join(DIR, "knowledge_seeds.jsonl");
const MANIFEST = path.join(DIR, "manifest.json");

function ensureDir() {
  fs.mkdirSync(DIR, { recursive: true });
}

function sha256(value) {
  return crypto
    .createHash("sha256")
    .update(String(value), "utf8")
    .digest("hex");
}

function loadManifest() {
  ensureDir();

  if (!fs.existsSync(MANIFEST)) {
    const manifest = {
      schema: "IMA-INTERGENERATIONAL-CONTINUITY-1.0",
      system: "IMA",
      purpose: "preserve knowledge, provenance, identity and derivations across generations",
      originals_never_overwritten: true,
      content_addressed: true,
      human_agency_preserved: true,
      created_at: Date.now()
    };

    fs.writeFileSync(
      MANIFEST,
      JSON.stringify(manifest, null, 2),
      "utf8"
    );

    return manifest;
  }

  try {
    return JSON.parse(fs.readFileSync(MANIFEST, "utf8"));
  } catch (_) {
    return null;
  }
}

function registerSeed({
  artifact_id,
  title,
  creator,
  source_language,
  content,
  source = null,
  parent_artifact = null,
  derivation_type = "original",
  license = null,
  verification_status = "unverified"
}) {
  ensureDir();

  if (!artifact_id || !title || content === undefined) {
    throw new Error("CONTINUITY_SEED_INVALID");
  }

  const record = {
    artifact_id: String(artifact_id),
    title: String(title),
    creator: creator || null,
    creation_date: new Date().toISOString(),
    source_language: source_language || null,
    file_format: "text",
    sha256: sha256(content),
    parent_artifact: parent_artifact || null,
    derivation_type,
    license: license || null,
    verification_status,
    source: source || null,
    preserved_at: Date.now()
  };

  fs.appendFileSync(
    SEEDS,
    JSON.stringify(record) + "\n",
    "utf8"
  );

  return record;
}

function status() {
  const manifest = loadManifest();

  return {
    enabled: true,
    schema: manifest ? manifest.schema : null,
    manifest_exists: fs.existsSync(MANIFEST),
    seeds_exists: fs.existsSync(SEEDS),
    seeds_path: SEEDS,
    originals_never_overwritten: true,
    content_addressed: true,
    human_agency_preserved: true
  };
}

module.exports = {
  loadManifest,
  registerSeed,
  status
};
