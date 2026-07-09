const { execSync } = require("child_process");
const fs = require("fs");

let lastHash = "";

function hashRepo() {
  try {
    return execSync("git status --porcelain").toString();
  } catch {
    return "";
  }
}

function commitAuto() {
  try {
    execSync("git add -A");

    const msg = `auto-sync ${Date.now()}`;
    execSync(`git commit -m "${msg}" || true`);
  } catch (e) {}
}

function startAutoGit() {
  setInterval(() => {
    const current = hashRepo();

    if (current !== lastHash) {
      console.log("[AUTO-GIT] change detected → committing");
      commitAuto();
      lastHash = current;
    }
  }, 5000);
}

module.exports = { startAutoGit };
