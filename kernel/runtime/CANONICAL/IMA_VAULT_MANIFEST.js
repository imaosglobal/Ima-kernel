const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const VAULT = path.join(ROOT, ".ima/runtime/continuity/artifacts");
const MANIFEST = path.join(
  ROOT,
  ".ima/runtime/continuity/artifact_manifest.json"
);

function sha256(value) {
  return crypto
    .createHash("sha256")
    .update(String(value), "utf8")
    .digest("hex");
}

function build() {
  fs.mkdirSync(VAULT, { recursive: true });

  const files = fs
    .readdirSync(VAULT)
    .filter(name => name.endsWith(".txt"))
    .sort();

  const artifacts = files.map(file => {
    const full = path.join(VAULT, file);
    const content = fs.readFileSync(full, "utf8");

    return {
      file,
      sha256: sha256(content),
      bytes: Buffer.byteLength(content, "utf8")
    };
  });

  const manifest = {
    schema: "IMA-ARTIFACT-MANIFEST-1.0",
    system: "IMA",
    purpose:
      "portable integrity manifest for preserved intergenerational artifacts",
    originals_never_overwritten: true,
    artifact_count: artifacts.length,
    artifacts,
    generated_at: new Date().toISOString()
  };

  fs.writeFileSync(
    MANIFEST,
    JSON.stringify(manifest, null, 2),
    "utf8"
  );

  return {
    status: "MANIFEST_BUILT",
    path: MANIFEST,
    artifact_count: artifacts.length,
    manifest_sha256: sha256(
      JSON.stringify(manifest, null, 2)
    )
  };
}

function verify() {
  if (!fs.existsSync(MANIFEST)) {
    return {
      status: "MANIFEST_NOT_FOUND"
    };
  }

  const manifest = JSON.parse(
    fs.readFileSync(MANIFEST, "utf8")
  );

  const results = [];
  let verified = 0;
  let mismatched = 0;
  let missing = 0;

  for (const artifact of manifest.artifacts || []) {
    const file = path.join(VAULT, artifact.file);

    if (!fs.existsSync(file)) {
      missing++;
      results.push({
        file: artifact.file,
        status: "MISSING"
      });
      continue;
    }

    const actual = sha256(
      fs.readFileSync(file, "utf8")
    );

    if (actual === artifact.sha256) {
      verified++;
      results.push({
        file: artifact.file,
        status: "VERIFIED"
      });
    } else {
      mismatched++;
      results.push({
        file: artifact.file,
        status: "HASH_MISMATCH"
      });
    }
  }

  return {
    status:
      mismatched || missing
        ? "MANIFEST_INTEGRITY_ERROR"
        : "MANIFEST_INTEGRITY_OK",
    total: manifest.artifact_count,
    verified,
    mismatched,
    missing,
    results
  };
}

if (require.main === module) {
  console.log(JSON.stringify(build(), null, 2));
  console.log(JSON.stringify(verify(), null, 2));
}

module.exports = {
  build,
  verify
};
