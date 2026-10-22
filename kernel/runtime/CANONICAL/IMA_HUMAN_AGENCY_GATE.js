"use strict";

const ACTION_CLASSES = Object.freeze({
  INFORMATIONAL: "INFORMATIONAL",
  PREPARATORY: "PREPARATORY",
  AUTHORIZATION_REQUIRED: "AUTHORIZATION_REQUIRED",
  CANONICAL_CHANGE: "CANONICAL_CHANGE"
});

const AUTHORIZATION_REQUIRED_ACTIONS = new Set([
  "send_outreach",
  "update_product",
  "create_personal_outreach",
  "spend_money",
  "donate_money",
  "transfer_money",
  "subscribe",
  "purchase",
  "publish_consequential",
  "sign_contract",
  "create_sponsorship",
  "run_paid_ad",
  "change_legal_status",
  "change_inheritance",
  "convert_personal_ip_to_nonprofit_asset"
]);

function classify(action) {
  if (AUTHORIZATION_REQUIRED_ACTIONS.has(action)) {
    return ACTION_CLASSES.AUTHORIZATION_REQUIRED;
  }
  if (action === "canonical_change") {
    return ACTION_CLASSES.CANONICAL_CHANGE;
  }
  if (action === "prepare_public_impact_message" || action === "generate_outreach") {
    return ACTION_CLASSES.PREPARATORY;
  }
  return ACTION_CLASSES.INFORMATIONAL;
}

function decide(action, context = {}) {
  const className = classify(action);
  const authorized = context.authorization === true || context.authorized === true;
  if (className === ACTION_CLASSES.INFORMATIONAL || className === ACTION_CLASSES.PREPARATORY) {
    return { allowed: true, approval_required: false, class: className, reason: "NON_CONSEQUENTIAL" };
  }
  if (authorized) {
    return { allowed: true, approval_required: false, class: className, reason: "EXPLICIT_AUTHORIZATION_PRESENT" };
  }
  return {
    allowed: false,
    approval_required: true,
    class: className,
    reason: "EXPLICIT_HUMAN_AUTHORIZATION_REQUIRED"
  };
}

module.exports = { ACTION_CLASSES, classify, decide };
