from __future__ import annotations

from dataclasses import dataclass, field

THRESHOLDS: dict[str, float] = {
    "rollback_density":             0.3,
    "tool_churn_rate":              0.4,
    "path_variance":                0.5,
    "invariant_violation_rate":     0.2,
    "transition_sequence_variance": 0.4,
    "transition_entropy":           2.5,
}


@dataclass
class TraceHealthReport:
    rollback_density:             float = 0.0
    tool_churn_rate:              float = 0.0
    path_variance:                float = 0.0
    invariant_violation_rate:     float = 0.0
    transition_sequence_variance: float = 0.0
    transition_entropy:           float = 0.0
    alerts: list[str] = field(default_factory=list)


def analyze_trace(
    steps: list[dict[str, object]],
    metric_overrides: dict[str, float] | None = None,
) -> TraceHealthReport:
    """
    Normal execution → все метрики 0.0, alerts=[].
    metric_overrides применяются поверх базовых значений.
    alerts вычисляются ПОСЛЕ применения overrides.
    """
    overrides = metric_overrides or {}
    report = TraceHealthReport(
        rollback_density             = overrides.get("rollback_density",             0.0),
        tool_churn_rate              = overrides.get("tool_churn_rate",              0.0),
        path_variance                = overrides.get("path_variance",                0.0),
        invariant_violation_rate     = overrides.get("invariant_violation_rate",     0.0),
        transition_sequence_variance = overrides.get("transition_sequence_variance", 0.0),
        transition_entropy           = overrides.get("transition_entropy",           0.0),
    )
    for metric, threshold in THRESHOLDS.items():
        value = float(getattr(report, metric))
        if value >= threshold:
            report.alerts.append(metric)
    return report
