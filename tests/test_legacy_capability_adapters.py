from learning.legacy_capability_adapters import action_requires_confirmation, classify_legacy_intent

def test_commerce_is_only_classified():
    result = classify_legacy_intent("אני רוצה לקנות מוצר")
    assert result.intent == "commerce"
    assert result.requested_actions == ("open_store",)

def test_learning_is_only_classified():
    result = classify_legacy_intent("אני רוצה ללמוד")
    assert result.intent == "learning"
    assert result.requested_actions == ("activate_learning",)

def test_memory_request_is_only_classified():
    result = classify_legacy_intent("זכור את זה")
    assert result.intent == "memory_request"
    assert result.requested_actions == ("store_memory",)

def test_legacy_actions_require_confirmation():
    assert action_requires_confirmation("open_store")
    assert action_requires_confirmation("activate_learning")
    assert action_requires_confirmation("store_memory")

def test_unknown_text_remains_chat():
    result = classify_legacy_intent("שלום")
    assert result.intent == "chat"
    assert result.requested_actions == ()
