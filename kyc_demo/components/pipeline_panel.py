from __future__ import annotations

import streamlit as st

from kyc_demo.engine.mock_runtime import STEP_LABELS
from kyc_demo.store.execution_state import ExecutionState

ICONS: dict[str, str] = {
    "PENDING": "·",
    "RUNNING": "→",
    "SUCCESS": "✅",
    "FAILED":  "❌",
}


def render_pipeline_panel(state: ExecutionState) -> None:
    """Reads ExecutionState (passed as arg). Renders 6 step rows."""
    st.subheader("KYC Pipeline")
    for step_id in state.steps:
        status = state.step_statuses.get(step_id, "PENDING")
        icon = ICONS.get(status, "·")
        label = STEP_LABELS.get(step_id, step_id)
        st.markdown(f"{icon} `{step_id}` — {label}")
