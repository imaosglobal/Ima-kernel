const fs = require("fs");
const { execSync } = require("child_process");
const { analyze } = require("./ima_analyzer");

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

function improve() {
  console.log("🧠 SMART IMPROVE START");

  const targets = analyze();

  if (targets.length === 0) {
    console.log("⏳ NO TARGETS");
    return;
  }

  let content = fs.readFileSync("server.js", "utf-8");

  // שיפור: הוספת לוג חכם לכל route
  let improved = content.replace(
    /app\.(get|post)\(([^)]+)\)\s*=>\s*{/g,
    (match) => {
      return match + ` console.log("⚡ route hit", Date.now()); `;
    }
  );

  if (content === improved) {
    console.log("⏳ NO CHANGE");
    return;
  }

  backup("server.js");
  fs.writeFileSync("server.js", improved);

  if (!isValid()) {
    console.log("🛑 BROKEN → ROLLBACK");
    fs.copyFileSync("server.js.bak", "server.js");
    return;
  }

  console.log("✔ SMART PATCH APPLIED");

  try {
    execSync("git add server.js");
    execSync(`git commit -m "smart improve ${Date.now()}"`);
    execSync("git push");
    console.log("🚀 PUSHED");
  } catch (e) {
    console.log("⚠️ GIT:", e.message);
  }

  console.log("✅ DONE");
}

improve();
