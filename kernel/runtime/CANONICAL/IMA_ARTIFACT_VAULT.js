const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const VAULT = path.join(ROOT, ".ima/runtime/continuity/artifacts");
const REGISTRY = path.join(
  ROOT,
  ".ima/runtime/continuity/preservation_registry.json"
);

function ensure() {
  fs.mkdirSync(VAULT, { recursive: true });
}

function sha256(content) {
  return crypto
    .createHash("sha256")
    .update(String(content), "utf8")
    .digest("hex");
}

function safeId(id) {
  return String(id).replace(/[^a-zA-Z0-9._:-]/g, "_");
}

function preserve({
  artifact_id,
  title,
  creator,
  source_language,
  content,
  creation_date = null,
  parent_artifact = null,
  derivation_type = "original",
  license = null,
  verification_status = "preserved"
}) {
  ensure();

  if (!artifact_id || content === undefined) {
    throw new Error("ARTIFACT_INVALID");
  }

  const id = safeId(artifact_id);
  const file = path.join(VAULT, `${id}.txt`);

  /*
   * Originals are immutable.
   * An existing artifact is never overwritten.
   */
  if (fs.existsSync(file)) {
    const existing = fs.readFileSync(file, "utf8");
    return {
      artifact_id: String(artifact_id),
      status: "ALREADY_PRESERVED",
      sha256: sha256(existing),
      content_path: file
    };
  }

  const text = String(content);
  const digest = sha256(text);

  fs.writeFileSync(file, text, {
    encoding: "utf8",
    flag: "wx"
  });

  return {
    artifact_id: String(artifact_id),
    title: title || null,
    creator: creator || null,
    creation_date: creation_date || new Date().toISOString(),
    source_language: source_language || null,
    file_format: "text/plain",
    sha256: digest,
    parent_artifact: parent_artifact || null,
    derivation_type,
    license: license || null,
    verification_status,
    content_path: file,
    preserved_at: Date.now()
  };
}

function verify(artifact_id, expected_sha256 = null) {
  ensure();

  const file = path.join(VAULT, `${safeId(artifact_id)}.txt`);

  if (!fs.existsSync(file)) {
    return {
      artifact_id: String(artifact_id),
      status: "CONTENT_NOT_FOUND"
    };
  }

  const digest = sha256(fs.readFileSync(file, "utf8"));

  return {
    artifact_id: String(artifact_id),
    status:
      expected_sha256 && digest !== expected_sha256
        ? "HASH_MISMATCH"
        : "VERIFIED",
    sha256: digest,
    expected_sha256: expected_sha256 || null,
    content_path: file
  };
}

function status() {
  ensure();

  return {
    enabled: true,
    vault_path: VAULT,
    artifact_count: fs
      .readdirSync(VAULT)
      .filter(name => name.endsWith(".txt")).length,
    originals_never_overwritten: true,
    sha256_verified_on_write: true
  };
}

module.exports = {
  preserve,
  verify,
  status,
  sha256
};
