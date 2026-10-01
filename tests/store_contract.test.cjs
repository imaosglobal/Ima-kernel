import fs from "node:fs";
const app = fs.readFileSync("ima-ui/src/App.jsx", "utf8");
const catalog = JSON.parse(fs.readFileSync("integrations/IMA_STORE_CATALOG.json", "utf8"));
if (!app.includes('id="store"')) throw new Error("store section missing");
if (!app.includes('href="#store"')) throw new Error("store navigation missing");
if (catalog.status !== "CATALOG_ONLY") throw new Error("catalog-only status required");
if (catalog.payment_enabled !== false) throw new Error("payments must remain disabled");
console.log("IMA_STORE_CONTRACT=PASS");
