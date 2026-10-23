#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const required=["docs/IMA_HEALTHY_EMPOWERMENT_STANDARD.md","docs/IMA_EMOTIONAL_REGULATION_AND_ADAPTIVE_HUMAN_CARE.md","kernel/runtime/CANONICAL/IMA_HEALTHY_EMPOWERMENT.js","kernel/runtime/CANONICAL/IMA_RUNTIME.js","kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE.js"];
const missing=required.filter(f=>!fs.existsSync(path.join(root,f)));
const m=fs.readFileSync(path.join(root,"kernel/runtime/CANONICAL/IMA_HEALTHY_EMPOWERMENT.js"),"utf8");
const r=fs.readFileSync(path.join(root,"kernel/runtime/CANONICAL/IMA_RUNTIME.js"),"utf8");
const a=fs.readFileSync(path.join(root,"kernel/runtime/CANONICAL/orchestration/IMA_ACTION_ENGINE.js"),"utf8");
const checks={required_files:missing.length===0,runtime_wired:r.includes("IMA_HEALTHY_EMPOWERMENT"),action_engine_wired:a.includes("IMA_HEALTHY_EMPOWERMENT"),unknown_preserved:m.includes("UNKNOWN stays UNKNOWN"),agency_preserved:m.includes("preserve_agency:true"),no_harm_gate:m.includes("no_harm_to_self_or_others:true"),no_dependency_design:m.includes("no_dependency_design:true"),tone_modes:m.includes("GENTLE_HUMOR")&&m.includes("NEUTRAL")&&m.includes("POSITIVE")};
const result={tool:"IMA Healthy Empowerment Audit",status:Object.values(checks).every(Boolean)?"VERIFIED":"GAPS_RECORDED",checks,missing,rule:"No claim of live capability without reproducible deployment evidence."};
console.log(JSON.stringify(result,null,2)); if(result.status!=="VERIFIED")process.exitCode=2;
