from __future__ import annotations

import streamlit as st


def _trunc(h: str, n: int = 12) -> str:
    return h[:n] + "..." if len(h) > n else h


def render_governance_stream(envelopes: list[dict[str, object]]) -> None:
    """Renders governance envelopes, newest-first."""
    st.subheader("GOVERNANCE STREAM")
    if not envelopes:
        st.caption("Awaiting execution...")
        return
    for env in reversed(envelopes):
        with st.expander(f"📋 {env['step_id']}", expanded=False):
            st.caption(f"policy_hash: `{_trunc(str(env['policy_hash']))}`")
            st.caption(f"canonical_hash: `{_trunc(str(env['canonical_snapshot_hash']))}`")
            st.caption(f"timestamp: {env['timestamp']}")
            st.json(env["payload"])
            st.info("Per-step envelope. trace_hash / merkle_root → Trace-level (AuditPanel).")
