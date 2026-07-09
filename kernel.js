const { execSync } = require("child_process");
const fs = require("fs");

const PATH = process.cwd();

// ---------- boot ----------
function boot() {
  console.log("🧠 IMA KERNEL v2 STARTING...");

  ensureMemory();
  ensureDeps();

  startServer();
}

// ---------- memory ----------
function ensureMemory() {
  if (!fs.existsSync("./memory.json")) {
    fs.writeFileSync("./memory.json", JSON.stringify({
      profile: { name: "אורי", mood: "calm", personality: "neutral" },
      memory: []
    }, null, 2));
  }
}

// ---------- deps ----------
function ensureDeps() {
  try {
    require.resolve("express");
    require.resolve("cors");
  } catch {
    console.log("📦 Installing dependencies...");
    execSync("npm install express cors", { stdio: "inherit" });
  }
}

// ---------- git sync ----------
function syncGit(message = "auto sync") {
  try {
    execSync("git add .");
    execSync(`git commit -m "${message}" || true`);
    execSync("git push origin main");
    console.log("🔄 Git synced");
  } catch (e) {
    console.log("⚠️ Git sync skipped");
  }
}

// ---------- self-heal ----------
function monitorProcess() {
  setInterval(() => {
    try {
      execSync("curl -s http://localhost:3000/health");
    } catch {
      console.log("💥 Kernel down → restarting...");
      restartServer();
    }
  }, 10000);
}

// ---------- server ----------
function startServer() {
  const server = require("./server.js");

  monitorProcess();

  process.on("SIGINT", () => {
    syncGit("shutdown snapshot");
    process.exit();
  });
}

// ---------- restart ----------
function restartServer() {
  execSync("pkill -f node || true");
  execSync("node kernel.js &");
}

// BOOT
boot();
