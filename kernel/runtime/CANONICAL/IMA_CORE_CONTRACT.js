"use strict";

const REQUIRED_FIELDS = Object.freeze([
  "goal",
  "context",
  "identity",
  "memory",
  "policy",
  "plan",
  "capability",
  "action",
  "result",
  "verification",
  "learning",
  "provenance"
]);

function createContract(input = {}) {
  const contract = {};

  for (const field of REQUIRED_FIELDS) {
    contract[field] = Object.prototype.hasOwnProperty.call(input, field)
      ? input[field]
      : null;
  }

  contract.created_at = new Date().toISOString();
  return Object.freeze(contract);
}

function validateContract(contract) {
  const missing = REQUIRED_FIELDS.filter(
    field => !Object.prototype.hasOwnProperty.call(contract || {}, field)
  );

  return {
    valid: missing.length === 0,
    missing
  };
}

module.exports = {
  REQUIRED_FIELDS,
  createContract,
  validateContract
};
