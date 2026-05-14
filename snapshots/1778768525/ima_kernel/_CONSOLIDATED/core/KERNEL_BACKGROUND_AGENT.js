const { execSync } = require("child_process");
const fs = require("fs");
const SYNC = require("./KERNEL_SYNC_ENGINE");

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function sh(cmd) {
  try {
    return execSync(cmd).toString().trim();
  } catch {
    return null;
  }
}

async function loop() {
  console.log("KERNEL BACKGROUND AGENT STARTED");

  let lastVersion = null;

  while (true) {
    try {
      const plan = SYNC.syncPlan();

      const local = plan.local;

      // רק אם יש שינוי אמיתי
      if (local !== lastVersion) {
        console.log("[AGENT] drift detected");

        // commit אוטומטי
        sh("git add .");
        sh(`git commit -m "auto sync ${Date.now()}" || true`);

        // tag sync
        sh(`git tag -f v${local}`);

        // push (שקט)
        sh("git push origin main || true");
        sh(`git push origin -f v${local} || true`);

        lastVersion = local;
      }

    } catch (e) {
      // שקט לחלוטין כדי לא להפריע לריצה
    }

    await sleep(5000); // בדיקה כל 5 שניות
  }
}

loop();
