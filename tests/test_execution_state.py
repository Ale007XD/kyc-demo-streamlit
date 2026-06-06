from __future__ import annotations


def test_execution_state_defaults() -> None:
    from kyc_demo.store.execution_state import ExecutionState
    s = ExecutionState()
    assert s.current_step_index == -1
    assert s.running is False
    assert s.envelopes == []
    assert len(s.steps) == 6


def test_pipeline_panel_importable() -> None:
    from kyc_demo.components.pipeline_panel import render_pipeline_panel
    assert callable(render_pipeline_panel)


def test_execution_state_step_statuses_empty() -> None:
    from kyc_demo.store.execution_state import ExecutionState
    s = ExecutionState()
    assert s.step_statuses == {}
    assert s.blocked_actions_total == 0
