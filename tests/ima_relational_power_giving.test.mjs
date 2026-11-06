import assert from "node:assert/strict";
import fs from "node:fs";

const standard = fs.readFileSync("docs/IMA_HEALTHY_EMPOWERMENT_STANDARD.md", "utf8");
const runtime = fs.readFileSync("kernel/runtime/CANONICAL/IMA_HEALTHY_EMPOWERMENT.js", "utf8");

assert.match(standard, /Relational power-giving rule/);
assert.match(standard, /return power to the person/i);
assert.match(standard, /never extract power from vulnerability/i);
assert.match(standard, /less IMA and more human capability/i);

assert.match(runtime, /return_power_to_person:true/);
assert.match(runtime, /never_extract_power_from_vulnerability:true/);
assert.match(runtime, /support returns power to the person rather than extracting power from vulnerability/i);

const { plan } = await import("../kernel/runtime/CANONICAL/IMA_HEALTHY_EMPOWERMENT.js");
const result = plan({capacity:"LOW", overload:"HIGH", agency:"HIGH"});
assert.equal(result.guardrails.return_power_to_person, true);
assert.equal(result.guardrails.never_extract_power_from_vulnerability, true);
assert.ok(result.success.some(x => /returns power to the person/i.test(x)));

console.log("IMA_RELATIONAL_POWER_GIVING_CONTRACT=PASS");
