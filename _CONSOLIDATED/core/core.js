const fs = require("fs");

console.log("🧠 IMA BRAIN V2");

const report = JSON.parse(fs.readFileSync("./unify_report.json"));

let brain = {
  stable_modules: [],
  unstable_modules: [],
  recommendations: []
};

// ניתוח בסיסי
if (report.failed.length > 0) {
  report.failed.forEach(f => {
    brain.unstable_modules.push(f.repo);
    brain.recommendations.push("Fix repo: " + f.repo);
  });
}

if (report.cloned.length > 0) {
  report.cloned.forEach(c => {
    if (c.files < 3) {
      brain.recommendations.push("Weak repo structure: " + c.repo);
    } else {
      brain.stable_modules.push(c.repo);
    }
  });
}

fs.writeFileSync(
  "./ima_brain_v2/brain.json",
  JSON.stringify(brain, null, 2)
);

console.log("✔ Brain analysis complete");
