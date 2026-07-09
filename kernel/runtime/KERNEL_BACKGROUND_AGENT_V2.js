const { execSync } = require("child_process");
const fs = require("fs");
const GOV = require("./KERNEL_GOVERNOR");

function sh(cmd) {
  try { return execSync(cmd).toString(); }
  catch { return null; }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function loop() {
  console.log("KERNEL GOVERNED AGENT STARTED");

  while (true) {
    try {
      const decision = GOV.decide();

      if (decision.action === "ignore") {
        await sleep(5000);
        continue;
      }

      if (decision.action === "hold") {
        console.log("[GOV] HOLD:", decision.reason);
        await sleep(8000);
        continue;
      }

      if (decision.action === "release") {
        console.log("[GOV] RELEASE:", decision.reason);

        sh("git add .");
        sh(`git commit -m "governed sync ${Date.now()}" || true`);

        const pkg = JSON.parse(fs.readFileSync("package.json","utf8"));
        const parts = pkg.version.split(".").map(Number);
        parts[2] += 1;
        pkg.version = parts.join(".");
        fs.writeFileSync("package.json", JSON.stringify(pkg,null,2));

        sh(`git tag -f v${pkg.version}`);
        sh("git push origin main || true");
        sh(`git push origin -f v${pkg.version} || true`);

        // שמירת snapshot
        const state = {
          snapshot: GOV.diffCheck(),
          version: pkg.version,
          ts: Date.now()
        };

        fs.writeFileSync("./runtime/kernel_state.json", JSON.stringify(state,null,2));
      }

    } catch (e) {}

    await sleep(5000);
  }
}

loop();
