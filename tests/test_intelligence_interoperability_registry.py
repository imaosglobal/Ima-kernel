from learning.intelligence_interoperability_registry import validate_candidate, promote


def test_discovered_needs_no_connection_evidence():
    assert validate_candidate({"status": "DISCOVERED"}) == []


def test_connected_requires_authorization_and_connection_evidence():
    gaps = validate_candidate({
        "status": "CONNECTED",
        "authorization": "authorized",
        "evidence_tags": ["authorized_credentials_or_explicit_host_permission"],
    })
    assert "missing:successful_connection_evidence" in gaps


def test_runtime_verified_requires_live_result():
    gaps = validate_candidate({
        "status": "RUNTIME-VERIFIED",
        "authorization": "authorized",
        "evidence_tags": [
            "authorized_credentials_or_explicit_host_permission",
            "successful_connection_evidence",
            "successful_live_request_or_interaction",
            "captured_result_evidence",
            "boundary_check",
        ],
    })
    assert "missing:live_result_evidence" in gaps


def test_monitoring_cannot_be_claimed_without_health_evidence():
    candidate = {
        "status": "RUNTIME-VERIFIED",
        "authorization": "authorized",
        "live_result_evidence": "evidence",
        "evidence_tags": [
            "authorized_credentials_or_explicit_host_permission",
            "successful_connection_evidence",
            "successful_live_request_or_interaction",
            "captured_result_evidence",
            "boundary_check",
        ],
    }
    promoted = promote(candidate, "RUNTIME-VERIFIED")
    assert promoted["status"] == "RUNTIME-VERIFIED"
