const { execSync } = require("child_process");
const fs = require("fs");
const { saveSnapshot } = require("./snapshot");

function run(cmd){
  try {
    return execSync(cmd).toString().trim();
  } catch {
    return "";
  }
}

function gitDiff(){
  return run("git status --porcelain");
}

function commitIfNeeded(){
  const diff = gitDiff();

  if (!diff) {
    return { ok:true, message:"no changes" };
  }

  saveSnapshot();

  run("git add .");
  run('git commit -m "auto-sync: autonomous engine" || true');

  return { ok:true, committed:true };
}

function push(){
  run("git push origin main || true");
  return { ok:true, pushed:true };
}

function npmCheck(){
  const out = run("npm outdated || true");
  return {
    ok:true,
    outdated: out || "clean"
  };
}

function cycle(){
  const result = {
    git: commitIfNeeded(),
    push: push(),
    npm: npmCheck(),
    ts: Date.now()
  };

  return result;
}

module.exports = { cycle };
