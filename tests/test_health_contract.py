from deployment.health_contract import evaluate_runtime_contract, healthy


def test_healthy_contract():
    checks = evaluate_runtime_contract(
        app_entrypoint_present=True,
        requirements_present=True,
        deployment_pipeline_present=True,
    )
    assert healthy(checks) is True


def test_missing_requirement_fails_without_side_effects():
    checks = evaluate_runtime_contract(
        app_entrypoint_present=True,
        requirements_present=False,
        deployment_pipeline_present=True,
    )
    assert healthy(checks) is False
    assert checks[1].name == "requirements"
