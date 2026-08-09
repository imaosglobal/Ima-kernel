POLICY = {

    "public_allowed": [
        "submit_lessons",
        "submit_plugins",
        "submit_connectors",
        "submit_feedback"
    ],

    "private_core": [
        "founder_identity",
        "private_memory",
        "core_reasoning",
        "internal_weights",
        "security_keys"
    ],

    "validation_required": True
}


def get_policy():
    return POLICY
