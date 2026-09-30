import { spawnSync } from "node:child_process";

const steps = [
  ["core", ["npm", "test"]],
  ["integrity", ["npm", "run", "ima:integrity"]],
  ["runtime", ["npm", "run", "ima:runtime"]],
  ["public-runtime", ["python", "tests/public_runtime.test.py"]],
  ["contract-harness", ["node", "tests/test_harness.test.cjs"]],
  ["accessibility-contract", ["node", "tests/accessibility_contract.test.cjs"]],
  ["preservation-contract", ["node", "tests/preservation_contract.test.cjs"]],
  ["applied-skill-contract", ["node", "tests/applied_skill_contract.test.cjs"]],
  ["learning-gap-contract", ["node", "tests/learning_gap_contract.test.cjs"]],
  ["learning-conclusion-import", ["python", "-c", "from learning.conclusion_engine import conclude; from learning.teaching_artifact import create_teaching_artifact; print(\"IMA_LEARNING_MODULES=PASS\")"]]
];

for (const [name, command] of steps) {
  console.log("\n=== IMA VERIFY: " + name + " ===");
  const result = spawnSync(command[0], command.slice(1), {
    stdio: "inherit",
    shell: false
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    console.error("IMA_VERIFY=FAIL:" + name);
    process.exit(result.status || 1);
  }
}

console.log("\nIMA_VERIFY=PASS");
