const fs = require("fs");
const cp = require("child_process");

function sh(cmd, ok = false) {
  try {
    return cp.execSync(cmd, { stdio: "pipe" }).toString().trim();
  } catch (e) {
    if (!ok) throw new Error(cmd);
    return null;
  }
}

function run(cmd) {
  console.log(">>", cmd);
  cp.execSync(cmd, { stdio: "inherit" });
}

// CONFIG
const BASE_NAME = "ima-core";
const SCOPE = "@mom-os1";
const NAME = `${SCOPE}/${BASE_NAME}`;
const VERSION = "1.0." + Date.now();

console.log("=== IMA RELEASE PIPELINE ===");
console.log("PACKAGE:", NAME);
console.log("VERSION:", VERSION);

// AUTH
const user = sh("npm whoami", true);
if (!user) {
  console.log("RUN: npm login");
  process.exit(1);
}
console.log("[AUTH OK]", user);

// PACKAGE
fs.writeFileSync("package.json", JSON.stringify({
  name: NAME,
  version: VERSION,
  main: "server.js",
  files: ["server.js","runtime/ENTRYPOINT.js","cli.js"],
  bin: { ima: "cli.js" }
}, null, 2));

// CLI
fs.writeFileSync("cli.js", `#!/usr/bin/env node
const http = require('http');
const cmd = process.argv[2] || 'run';
const host = process.env.IMA_HOST || 'localhost';

http.get('http://' + host + ':4000/' + cmd, res => {
  res.pipe(process.stdout);
}).on('error', () => {
  console.log('server not reachable');
});
`);

run("chmod +x cli.js");

// GIT
run("git add .");
run(`git commit -m "release ${VERSION}" || true`);
run(`git tag ${VERSION} || true`);
run("git push || true");
run("git push --tags || true");

// PUBLISH
try {
  run("npm publish --access public");
} catch (e) {
  console.log("PUBLISH FAILED");
  process.exit(1);
}

// VERIFY
const v = sh(`npm view ${NAME} version`, true);
if (v.includes(VERSION)) {
  console.log("SUCCESS:", NAME, VERSION);
} else {
  console.log("VERIFY FAILED");
}
