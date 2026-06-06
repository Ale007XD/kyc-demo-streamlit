from __future__ import annotations


def test_comparison_rows_count() -> None:
    from kyc_demo.components.comparison_panel import ROWS
    assert len(ROWS) == 6


def test_comparison_rows_content() -> None:
    from kyc_demo.components.comparison_panel import ROWS
    left_vals = [r[0] for r in ROWS]
    right_vals = [r[1] for r in ROWS]
    assert "Blocked before action" in right_vals
    assert "Logged after action" in left_vals
    assert "Capability-gated tools" in right_vals
    assert "Structural validation before execution" in right_vals


def test_governance_stream_importable() -> None:
    from kyc_demo.components.governance_stream import render_governance_stream
    assert callable(render_governance_stream)


def test_trunc_short() -> None:
    from kyc_demo.components.governance_stream import _trunc
    assert _trunc("sha256:ab", 12) == "sha256:ab"


def test_trunc_long() -> None:
    from kyc_demo.components.governance_stream import _trunc
    assert _trunc("sha256:abcdef1234567890", 12) == "sha256:abcde..."
    assert len(_trunc("sha256:abcdef1234567890", 12)) == 15


def test_policy_lock_importable() -> None:
    from kyc_demo.components.policy_lock import render_policy_lock
    assert callable(render_policy_lock)


def test_policy_lock_signature() -> None:
    import inspect
    from kyc_demo.components.policy_lock import render_policy_lock
    sig = inspect.signature(render_policy_lock)
    params = list(sig.parameters.keys())
    assert "policy_name" in params
    assert "hash_value" in params
    assert "locked" in params


def test_entropy_panel_importable() -> None:
    from kyc_demo.components.entropy_panel import render_entropy_panel
    assert callable(render_entropy_panel)


def test_entropy_threshold_constant() -> None:
    from kyc_demo.components.entropy_panel import ENTROPY_THRESHOLD
    assert ENTROPY_THRESHOLD == 2.5


def test_entropy_panel_signature() -> None:
    import inspect
    from kyc_demo.components.entropy_panel import render_entropy_panel
    sig = inspect.signature(render_entropy_panel)
    assert "entropy" in sig.parameters
    assert "threshold" in sig.parameters


def test_narrative_receipt_importable() -> None:
    from kyc_demo.components.narrative_receipt import render_narrative_receipt
    assert callable(render_narrative_receipt)


def test_narrative_receipt_signature() -> None:
    import inspect
    from kyc_demo.components.narrative_receipt import render_narrative_receipt
    sig = inspect.signature(render_narrative_receipt)
    assert "state" in sig.parameters
    assert "report" in sig.parameters


def test_audit_panel_importable() -> None:
    from kyc_demo.components.audit_panel import render_audit_panel
    assert callable(render_audit_panel)


def test_audit_panel_signature() -> None:
    import inspect
    from kyc_demo.components.audit_panel import render_audit_panel
    sig = inspect.signature(render_audit_panel)
    assert "state" in sig.parameters


def test_app_importable() -> None:
    import sys
    import unittest.mock as mock
    with mock.patch.dict(sys.modules, {"streamlit": mock.MagicMock()}):
        from kyc_demo.engine.program_validator import validate_program
        from kyc_demo.engine.mock_runtime import STEPS
        from kyc_demo.engine.trace_analyzer import analyze_trace, THRESHOLDS
        assert len(STEPS) == 6
        assert THRESHOLDS["transition_entropy"] == 2.5


def test_comparison_panel_importable() -> None:
    from kyc_demo.components.comparison_panel import render_comparison_panel
    assert callable(render_comparison_panel)


def test_comparison_panel_signature() -> None:
    import inspect
    from kyc_demo.components.comparison_panel import render_comparison_panel
    sig = inspect.signature(render_comparison_panel)
    assert len(sig.parameters) == 0
