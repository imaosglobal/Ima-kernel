const { execSync } = require("child_process");
const fs = require("fs");

function gitStatus() {
  try {
    return execSync("git status --porcelain").toString().trim();
  } catch {
    return null;
  }
}

function safeCommit(message = "auto-sync") {
  const status = gitStatus();
  if (!status) return { ok:false, error:"no git repo" };

  if (status.length === 0) {
    return { ok:true, message:"no changes" };
  }

  execSync("git add .");
  execSync(`git commit -m "${message}" || true`);
  return { ok:true, committed:true };
}

function safePush() {
  try {
    execSync("git push origin main || true");
    return { ok:true };
  } catch (e) {
    return { ok:false };
  }
}

function npmCheck() {
  try {
    const out = execSync("npm outdated || true").toString();
    return { ok:true, outdated: out };
  } catch {
    return { ok:false };
  }
}

module.exports = {
  safeCommit,
  safePush,
  npmCheck
};
