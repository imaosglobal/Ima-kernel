const fs = require("fs");

function buildReport() {
  const log = JSON.parse(fs.readFileSync("learning_log.json"));

  let md = `# IMA Learning Report\n\n`;

  md += `## Summary\n`;
  md += `Total repos analyzed: ${log.length}\n\n`;

  md += `## Insights\n`;

  log.forEach(l => {
    md += `- ${l.repo} → ${l.patterns} patterns\n`;
  });

  md += `\n---\nGenerated automatically by IMA system\n`;

  fs.writeFileSync("PUBLIC_REPORT.md", md);

  console.log("📄 PUBLIC REPORT GENERATED");
}

buildReport();
