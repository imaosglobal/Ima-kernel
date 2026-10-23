#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const files=[
"docs/IMA_CONTINUOUS_BETTERMENT_STANDARD.md",
"kernel/runtime/CANONICAL/IMA_CONTINUOUS_BETTERMENT.js",
"kernel/runtime/CANONICAL/IMA_RUNTIME.js"
];
const missing=files.filter(f=>!fs.existsSync(path.join(root,f)));
const m=fs.readFileSync(path.join(root,files[1]),"utf8");
const r=fs.readFileSync(path.join(root,files[2]),"utf8");
const checks={
files:missing.length===0,
dimensions:m.includes("TRUTH")&&m.includes("ACCESSIBILITY")&&m.includes("COMMUNITY_BENEFIT"),
risk_gate:m.includes("HUMAN_AUTHORIZATION_REQUIRED_FOR_HIGH_IMPACT_RISK"),
runtime_wired:r.includes("IMA_CONTINUOUS_BETTERMENT")
};
const result={status:Object.values(checks).every(Boolean)?"VERIFIED":"GAPS_RECORDED",checks,missing};
console.log(JSON.stringify(result,null,2));
if(result.status!=="VERIFIED")process.exitCode=2;
