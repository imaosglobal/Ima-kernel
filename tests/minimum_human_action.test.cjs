import assert from "node:assert/strict";
import { buildMinimumHumanPlan, classifyHumanBoundary, canDelegateToProvider } from "../core/minimum-human-action.js";

assert.equal(classifyHumanBoundary({}), "NONE");
assert.equal(classifyHumanBoundary({requiresIdentity:true}), "IDENTITY");
assert.equal(classifyHumanBoundary({requiresSignature:true}), "SIGNATURE");
assert.equal(classifyHumanBoundary({requiresBanking:true}), "BANKING");
assert.equal(classifyHumanBoundary({requiresAccountableDecision:true}), "ACCOUNTABLE_DECISION");
assert.equal(classifyHumanBoundary({irreversible:true, authorized:false}), "APPROVAL");

const plan = buildMinimumHumanPlan({
  task_id: "funding-demo",
  steps: [
    {id:"prepare", prepared:true},
    {id:"kyc", requiresIdentity:true, provider:"idv"},
    {id:"sign", requiresSignature:true, provider:"esign"},
    {id:"submit", irreversible:true, authorized:true}
  ]
});
assert.deepEqual(plan.automated_steps, ["prepare","submit"]);
assert.deepEqual(plan.human_steps, ["kyc","sign"]);
assert.equal(plan.minimum_interactions, 1);
assert.equal(plan.stop_before, "kyc");
assert.equal(plan.resume_after_human, true);
assert.equal(canDelegateToProvider({capability:"idv",providerAuthorized:true,userAuthorized:true}), true);
assert.equal(canDelegateToProvider({capability:"idv",providerAuthorized:true,userAuthorized:false}), false);

console.log("minimum-human-action: PASS");
