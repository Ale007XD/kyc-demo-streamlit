from __future__ import annotations

import streamlit as st

from kyc_demo.engine.trace_analyzer import THRESHOLDS, TraceHealthReport


def render_trace_health(report: TraceHealthReport) -> None:
    """Renders 6 metric rows with threshold indicators."""
    st.subheader("TRACE HEALTH")
    for metric, threshold in THRESHOLDS.items():
        value = float(getattr(report, metric))
        alerted = metric in report.alerts
        icon = "⚠️" if alerted else "✅"
        st.markdown(f"{icon} `{metric}` = **{value:.2f}** (threshold: {threshold})")
    if report.alerts:
        st.error(f"⚠ GOVERNANCE ALERT: {', '.join(report.alerts)}")
    else:
        st.success("NOMINAL")
