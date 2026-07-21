const IMM = require("./IMMUTABLE_GATE");
const POLICY = require("./POLICY_ENGINE");

function write(file, content) {
  if (!POLICY.allowWrite(file, content)) {
    return { status: "blocked_by_policy", file };
  }

  return IMM.write(file, content);
}

module.exports = { write };
