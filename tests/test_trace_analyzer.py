from __future__ import annotations


def test_empty_steps_all_zero() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace
    r = analyze_trace([])
    assert r.rollback_density == 0.0
    assert r.tool_churn_rate == 0.0
    assert r.path_variance == 0.0
    assert r.invariant_violation_rate == 0.0
    assert r.transition_sequence_variance == 0.0
    assert r.transition_entropy == 0.0
    assert r.alerts == []


def test_no_overrides_normal_run() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace
    steps = [{"step_id": s} for s in ["s1", "s2", "s3"]]
    r = analyze_trace(steps)
    assert r.alerts == []


def test_override_triggers_alert() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace
    r = analyze_trace([], metric_overrides={"transition_entropy": 2.8})
    assert "transition_entropy" in r.alerts
    assert r.transition_entropy == 2.8


def test_override_below_threshold_no_alert() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace
    r = analyze_trace([], metric_overrides={"rollback_density": 0.1})
    assert "rollback_density" not in r.alerts


def test_multiple_overrides() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace
    r = analyze_trace([], metric_overrides={
        "path_variance": 0.6,
        "tool_churn_rate": 0.45,
    })
    assert "path_variance" in r.alerts
    assert "tool_churn_rate" in r.alerts
    assert "rollback_density" not in r.alerts


def test_threshold_entropy_is_2_5() -> None:
    from kyc_demo.engine.trace_analyzer import THRESHOLDS
    assert THRESHOLDS["transition_entropy"] == 2.5


def test_six_metrics_in_report() -> None:
    from kyc_demo.engine.trace_analyzer import analyze_trace, THRESHOLDS, TraceHealthReport
    r = analyze_trace([])
    metric_names = [
        f.name for f in TraceHealthReport.__dataclass_fields__.values()
        if f.name != "alerts"
    ]
    assert len(metric_names) == 6
    for name in THRESHOLDS:
        assert hasattr(r, name)


def test_trace_health_importable() -> None:
    from kyc_demo.components.trace_health import render_trace_health
    assert callable(render_trace_health)
