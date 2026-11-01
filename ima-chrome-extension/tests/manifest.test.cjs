const fs = require("fs");
const assert = require("assert");

const manifest = JSON.parse(fs.readFileSync(require("path").join(__dirname, "..", "manifest.json"), "utf8"));

assert.equal(manifest.manifest_version, 3);
assert.equal(manifest.background.service_worker, "background.js");
assert.deepEqual(manifest.permissions.sort(), ["activeTab", "scripting", "storage", "tabs"].sort());
assert.equal(manifest.permissions.includes("cookies"), false);
assert.equal(manifest.permissions.includes("<all_urls>"), false);

console.log("IMA Browser Bridge manifest checks passed.");
