from __future__ import annotations

import streamlit as st

from kyc_demo.engine.program_validator import ValidationResult


def render_pre_flight_panel(result: ValidationResult) -> None:
    """Pure display. Receives ValidationResult, renders check rows + status badge."""
    st.subheader("PRE-FLIGHT VALIDATION")
    checks = [
        ("missing_targets",   result.checks.missing_targets),
        ("unreachable_steps", result.checks.unreachable_steps),
        ("cycle_detection",   result.checks.cycle_detection),
    ]
    for name, passed in checks:
        icon = "✅" if passed else "❌"
        st.markdown(f"{icon} `{name}`")

    if result.valid:
        st.success("✅ CLEARED FOR EXECUTION")
    else:
        st.error("🚫 EXECUTION BLOCKED")
        for err in result.errors:
            st.caption(err)
