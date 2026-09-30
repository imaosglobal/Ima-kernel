import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const root=process.cwd();
const registry=JSON.parse(fs.readFileSync(path.join(root,"integrations/IMA_SKILL_REGISTRY.json"),"utf8"));
assert.equal(registry.schema,"IMA-APPLIED-SKILL-REGISTRY-1.0");
assert.ok(registry.lifecycle.includes("VERIFIED"));
assert.equal(registry.safety.learning_never_executes_external_actions,true);
assert.equal(registry.safety.consequential_actions_require_explicit_authorization,true);

const compiler=fs.readFileSync(path.join(root,"learning/skill_compiler.py"),"utf8");
for (const marker of ["compile_skill","persist_skill","SPECIFY","IMPLEMENT","TEST","VERIFY","rollback","provenance"]) {
  assert.ok(compiler.includes(marker),marker);
}

const loop=fs.readFileSync(path.join(root,"learning/learning_loop.py"),"utf8");
assert.ok(loop.includes("compile_and_record"));
assert.ok(loop.includes("applied_skill"));

console.log("IMA_APPLIED_SKILL_CONTRACT=PASS");
