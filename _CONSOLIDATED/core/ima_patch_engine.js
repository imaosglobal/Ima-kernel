const fs = require("fs");
const { execSync } = require("child_process");

function backup(file) {
  fs.copyFileSync(file, file + ".bak");
}

function isValid() {
  try {
    execSync("node -c server.js");
    return true;
  } catch {
    return false;
  }
}

function patch() {
  console.log("🧠 IMA PATCH ENGINE START");

  const target = "server.js";

  let content = fs.readFileSync(target, "utf-8");

  // דוגמה: שיפור לוגים (לא מסוכן)
  const improved = content.replace(
    "console.log(\"🧠 IMA KERNEL RUNNING\");",
    "console.log(\"🧠 IMA KERNEL RUNNING | optimized \" + Date.now());"
  );

  if (content === improved) {
    console.log("⏳ NO CHANGE");
    return;
  }

  backup(target);
  fs.writeFileSync(target, improved);

  if (!isValid()) {
    console.log("🛑 PATCH BROKE SYSTEM → ROLLBACK");
    fs.copyFileSync(target + ".bak", target);
    return;
  }

  console.log("✔ PATCH APPLIED");

  try {
    execSync("git add server.js");
    execSync(`git commit -m "auto patch ${Date.now()}"`);
    execSync("git push");
    console.log("🚀 PATCH PUSHED");
  } catch (e) {
    console.log("⚠️ GIT:", e.message);
  }

  console.log("✅ PATCH DONE");
}

patch();
