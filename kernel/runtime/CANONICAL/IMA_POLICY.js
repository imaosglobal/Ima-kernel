const SAFE_ACTIONS = new Set([
    "monitor",
    "collect_feedback",
    "analyze_feedback",
    "rank_leads",
    "find_leads",
    "generate_outreach",
    "prepare_public_impact_message"
]);

const APPROVAL_REQUIRED = new Set([
    "send_outreach",
    "update_product",
    "create_personal_outreach"
]);

function allow(action, context = {}) {
    if (SAFE_ACTIONS.has(action)) {
        return {
            allowed: true,
            approval_required: false,
            action
        };
    }

    if (APPROVAL_REQUIRED.has(action)) {
        return {
            allowed: false,
            approval_required: true,
            action,
            reason: "impactful or external action requires explicit approval"
        };
    }

    return {
        allowed: false,
        approval_required: true,
        action,
        reason: "unknown action is denied by default"
    };
}

module.exports = {
    allow,
    SAFE_ACTIONS: [...SAFE_ACTIONS],
    APPROVAL_REQUIRED: [...APPROVAL_REQUIRED]
};
