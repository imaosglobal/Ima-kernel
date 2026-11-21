from learning.accessibility_action_map import build_action_candidates

def test_maps_supported_roles_only():
    result = build_action_candidates([
        {"ref":"@e1","role":"button","name":"Report"},
        {"ref":"@e2","role":"textbox","name":"Message"},
        {"ref":"@e3","role":"image","name":"Logo"},
    ])
    assert result == [
        {"ref":"@e1","role":"button","name":"Report","action":"activate"},
        {"ref":"@e2","role":"textbox","name":"Message","action":"fill"},
    ]
