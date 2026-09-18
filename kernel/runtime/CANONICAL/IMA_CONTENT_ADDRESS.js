const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../..");
const VAULT = path.join(ROOT, ".ima/runtime/continuity/artifacts");
const INDEX = path.join(
  ROOT,
  ".ima/runtime/continuity/content_address_index.json"
);

function sha256(content) {
  return crypto.createHash("sha256")
    .update(String(content), "utf8")
    .digest("hex");
}

function build() {
  fs.mkdirSync(VAULT, { recursive: true });

  const index = {
    schema: "IMA-CONTENT-ADDRESS-1.0",
    algorithm: "SHA-256",
    immutable: true,
    records: []
  };

  for (const file of fs.readdirSync(VAULT).filter(f => f.endsWith(".txt")).sort()) {
    const content = fs.readFileSync(path.join(VAULT, file), "utf8");
    const digest = sha256(content);

    const addressDir = path.join(VAULT, "sha256");
    fs.mkdirSync(addressDir, { recursive: true });

    const addressFile = path.join(addressDir, digest + ".txt");

    if (!fs.existsSync(addressFile)) {
      fs.writeFileSync(addressFile, content, {
        encoding: "utf8",
        flag: "wx"
      });
    }

    index.records.push({
      legacy_file: file,
      sha256: digest,
      content_address: "sha256:" + digest,
      content_file: path.relative(ROOT, addressFile)
    });
  }

  fs.writeFileSync(
    INDEX,
    JSON.stringify(index, null, 2),
    "utf8"
  );

  return {
    status: "CONTENT_ADDRESSING_BUILT",
    algorithm: "SHA-256",
    records: index.records.length,
    index: INDEX
  };
}

function verify() {
  if (!fs.existsSync(INDEX)) {
    return { status: "INDEX_NOT_FOUND" };
  }

  const index = JSON.parse(fs.readFileSync(INDEX, "utf8"));
  let verified = 0;
  let missing = 0;
  let mismatched = 0;

  const results = [];

  for (const record of index.records) {
    const file = path.join(ROOT, record.content_file);

    if (!fs.existsSync(file)) {
      missing++;
      results.push({
        content_address: record.content_address,
        status: "MISSING"
      });
      continue;
    }

    const actual = sha256(fs.readFileSync(file, "utf8"));

    if (actual === record.sha256) {
      verified++;
      results.push({
        content_address: record.content_address,
        status: "VERIFIED"
      });
    } else {
      mismatched++;
      results.push({
        content_address: record.content_address,
        status: "HASH_MISMATCH"
      });
    }
  }

  return {
    status: missing || mismatched
      ? "CONTENT_ADDRESS_INTEGRITY_ERROR"
      : "CONTENT_ADDRESS_INTEGRITY_OK",
    total: index.records.length,
    verified,
    missing,
    mismatched,
    results
  };
}

if (require.main === module) {
  console.log(JSON.stringify(build(), null, 2));
  console.log(JSON.stringify(verify(), null, 2));
}

module.exports = { build, verify };
