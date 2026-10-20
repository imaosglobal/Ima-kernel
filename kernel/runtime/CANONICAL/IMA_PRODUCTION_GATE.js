"use strict";
const fs=require("fs"),path=require("path"),relational=require("./IMA_RELATIONAL_CARE");
const ROOT=path.resolve(__dirname,"../../..");
function verify(){const required=["kernel/runtime/CANONICAL/IMA_RELATIONAL_CARE.js","tests/ima_relational_care.test.cjs","docs/IMA_UNIVERSAL_RELATIONAL_CARE_AND_AGENCY_CONTRACT.md"];const missing=required.filter(f=>!fs.existsSync(path.join(ROOT,f)));const policy=relational.verify();return {production_policy_gate:policy.valid&&missing.length===0,relational_policy_version:relational.POLICY_VERSION,missing,status:policy.valid&&missing.length===0?"READY_FOR_DEPLOYMENT_VERIFICATION":"BLOCKED"}}
module.exports={verify};
