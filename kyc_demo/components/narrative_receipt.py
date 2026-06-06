from __future__ import annotations

import streamlit as st

from kyc_demo.engine.trace_analyzer import TraceHealthReport
from kyc_demo.store.execution_state import ExecutionState


def render_narrative_receipt(
    state: ExecutionState,
    report: TraceHealthReport,
) -> None:
    """
    Header: NARRATIVE RECEIPT
    Warning badge: UI ARTIFACT
    Subtitle: Derived from execution trace. Not authoritative runtime state.
    """
    st.subheader("NARRATIVE RECEIPT")
    st.warning("⚠ UI ARTIFACT")
    st.caption("Derived from execution trace. Not authoritative runtime state.")

    st.markdown(f"**Execution ID:** `{state.execution_id or 'N/A'}`")
    st.markdown(f"**Steps completed:** {max(state.current_step_index + 1, 0)} / {len(state.steps)}")
    st.markdown(f"**Blocked actions total:** {state.blocked_actions_total}")

    status = "COMPLETE" if state.current_step_index >= len(state.steps) - 1 else "IN PROGRESS"
    st.markdown(f"**Status:** `{status}`")

    st.markdown("---")
    st.markdown("**Trace Health Summary**")
    if report.alerts:
        st.error(f"⚠ Alerts: {', '.join(report.alerts)}")
    else:
        st.success("NOMINAL — no governance alerts")

    st.caption("merkle_root: [Trace-level] — see AuditPanel for integrity verification.")
