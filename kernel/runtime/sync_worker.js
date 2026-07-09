const { execSync } = require("child_process");

function run(cmd){
  try { return execSync(cmd).toString().trim(); }
  catch { return ""; }
}

function cycle(){
  const diff = run("git status --porcelain");

  if (diff) {
    run("git add .");
    run('git commit -m "auto-sync worker commit" || true');
    run("git push origin main || true");
    console.log("[SYNC WORKER] committed + pushed");
  } else {
    console.log("[SYNC WORKER] clean");
  }

  run("npm outdated || true");
}

console.log("[SYNC WORKER STARTED]");

setInterval(cycle, 15000);
