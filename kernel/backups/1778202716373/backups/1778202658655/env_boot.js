const fs = require("fs");
const envPath = process.env.HOME + "/.ima_env";

if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, "utf8").split("\n");
  for (const line of lines) {
    const [k, ...v] = line.split("=");
    if (k && v.length) {
      process.env[k.trim()] = v.join("=").trim();
    }
  }
  console.log("ENV LOADED FROM:", envPath);
}
