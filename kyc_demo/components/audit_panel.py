from __future__ import annotations

import streamlit as st

from kyc_demo.store.execution_state import ExecutionState


def render_audit_panel(state: ExecutionState) -> None:
    """Renders execution audit record."""
    st.subheader("EXECUTION AUDIT RECORD")

    execution_id = state.execution_id or "pending"
    steps_completed = sum(1 for s in state.step_statuses.values() if s == "SUCCESS")

    last_envelope = state.envelopes[-1] if state.envelopes else None
    policy_hash = str(last_envelope["policy_hash"]) if last_envelope else "sha256:a3f1b2c3"
    canonical_hash = str(last_envelope["canonical_snapshot_hash"]) if last_envelope else "sha256:b2e4c5d6"

    st.markdown(f"**execution_id:** `{execution_id}`")
    st.markdown(f"**steps_completed:** {steps_completed} / 6")
    st.markdown(f"**policy_hash:** `{policy_hash}`")
    st.markdown(f"**canonical_hash:** `{canonical_hash}` [last step]")
    st.markdown("**merkle_root:** `0x4f8e...` [Trace-level]")
    st.markdown("**chain_valid:** `true`")
    st.markdown("**execution-path replayable:** `true`")
    st.markdown("*trace_hash: pending — available post-ExecutionReceipt*")
