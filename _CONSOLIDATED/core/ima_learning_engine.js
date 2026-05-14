const fs = require("fs");
const { execSync } = require("child_process");

const { search } = require("./repo_discovery");
const { clone } = require("./repo_clone");
const { scan } = require("./repo_learn");

async function run() {
  console.log("🧠 IMA LEARNING START");

  const repos = await search();
  let report = [];

  for (const repo of repos) {
    console.log("🔎", repo.name);

    const dir = clone(repo);
    const insights = scan(dir);

    report.push({
      repo: repo.name,
      patterns: insights.length
    });

    console.log("📚 learned:", insights.length);
  }

  // שמירת למידה
  fs.writeFileSync("learning_log.json", JSON.stringify(report, null, 2));

  console.log("💾 LEARNING SAVED");

  // sync לגיט
  try {
    execSync("git add learning_log.json");
    execSync(`git commit -m "learning update ${Date.now()}"`);
    execSync("git push");
    console.log("🚀 LEARNING PUSHED");
  } catch (e) {
    console.log("⚠️ GIT:", e.message);
  }

  console.log("✅ LEARNING DONE");
}

run();
