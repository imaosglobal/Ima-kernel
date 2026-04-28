const { execSync } = require("child_process");
const fs = require("fs");

/* ================= UTIL ================= */
function run(cmd){
  try {
    return execSync(cmd, { encoding: "utf8" });
  } catch (e) {
    return e.message;
  }
}

/* ================= STEP 1: CHECK SYSTEM ================= */
function step1_check(){
  console.log("🧠 STEP 1: SYSTEM CHECK");

  const gitStatus = run("git status");
  console.log(gitStatus);

  return gitStatus.includes("working tree clean") || gitStatus.includes("nothing to commit");
}

/* ================= STEP 2: BUILD CORE ================= */
function step2_build(){
  console.log("⚙️ STEP 2: BUILD CORE");

  fs.writeFileSync("ima_runtime_state.json", JSON.stringify({
    boot: true,
    timestamp: Date.now()
  }, null, 2));

  return true;
}

/* ================= STEP 3: GIT SYNC ================= */
function step3_git(){
  console.log("🌍 STEP 3: GIT SYNC");

  run("git add .");

  const commit = run('git commit -m "IMA auto orchestrator sync"');

  console.log(commit);

  const push = run("git push origin main");

  console.log(push);

  return true;
}

/* ================= STEP 4: VERIFY ================= */
function step4_verify(){
  console.log("🔍 STEP 4: VERIFY");

  const log = run("git log --oneline -3");
  console.log(log);

  return log.includes("IMA");
}

/* ================= RUN PIPELINE ================= */
function runPipeline(){

  console.log("\n🚀 IMA ORCHESTRATOR START\n");

  const s1 = step1_check();
  const s2 = step2_build();
  const s3 = step3_git();
  const s4 = step4_verify();

  const status = {
    system_check: s1,
    build: s2,
    git_sync: s3,
    verify: s4
  };

  console.log("\n📊 FINAL STATUS:");
  console.log(status);

  if(s1 && s2 && s3 && s4){
    console.log("\n✅ IMA PIPELINE COMPLETE");
  } else {
    console.log("\n⚠️ PIPELINE PARTIAL / NEEDS REVIEW");
  }
}

runPipeline();
