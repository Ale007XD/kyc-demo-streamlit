from __future__ import annotations


def test_steps_count() -> None:
    from kyc_demo.engine.mock_runtime import STEPS
    assert len(STEPS) == 6


def test_get_next_step_sequence() -> None:
    from kyc_demo.engine.mock_runtime import get_next_step
    assert get_next_step("collect_customer_data") == "screen_sanctions"
    assert get_next_step("human_approval") == "governance_seal"


def test_get_next_step_terminal() -> None:
    from kyc_demo.engine.mock_runtime import get_next_step
    assert get_next_step("governance_seal") is None


def test_get_next_step_unknown() -> None:
    from kyc_demo.engine.mock_runtime import get_next_step
    assert get_next_step("nonexistent") is None


def test_run_step_returns_success() -> None:
    from kyc_demo.engine.mock_runtime import run_step
    envelopes: list[dict[str, object]] = []
    result = run_step("screen_sanctions", "exec-test-001", envelopes.append)
    assert result["status"] == "SUCCESS"
    assert result["step_id"] == "screen_sanctions"


def test_run_step_emits_envelope() -> None:
    from kyc_demo.engine.mock_runtime import run_step
    envelopes: list[dict[str, object]] = []
    run_step("agent_review", "exec-test-002", envelopes.append)
    assert len(envelopes) == 1
    env = envelopes[0]
    assert env["execution_id"] == "exec-test-002"
    assert env["step_id"] == "agent_review"
    assert "policy_hash" in env
    assert "canonical_snapshot_hash" in env
