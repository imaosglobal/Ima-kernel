import assert from "node:assert/strict";
import { ImaPhysicalAdapter } from "../integrations/physical/ima-physical-adapter.js";

const adapter = new ImaPhysicalAdapter({
  class: "robot",
  vendor: "reference",
  model: "reference-device"
});

assert.equal(adapter.discover().standard, "0.1");
assert.equal(adapter.observe({ sensor: "ok" }).ok, true);
assert.equal(adapter.act({ type: "move" }).blocked, true);
adapter.authorize(3);
assert.equal(adapter.act({ type: "move" }, { explicitAuthorization: false }).blocked, true);
assert.equal(adapter.stop().ok, true);

console.log("IMA physical adapter tests: PASS");
