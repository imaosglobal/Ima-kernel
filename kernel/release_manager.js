const { execSync } = require("child_process");
const { analyzeChanges } = require("./decision_engine");

function run() {
  const d = analyzeChanges();

  if (d.shouldRestart) {
    console.log("[AUTO] restart");
    execSync("ima restart", { stdio: "inherit" });
  }

  if (d.shouldPush) {
    console.log("[AUTO] git push");
    execSync("git add . && git commit -m 'auto sync' && git push", {
      stdio: "inherit"
    });
  }

  if (d.shouldRelease) {
    console.log("[AUTO] version bump");
    execSync("npm version patch --no-git-tag-version", { stdio: "inherit" });
  }

  return d;
}

module.exports = { run };
