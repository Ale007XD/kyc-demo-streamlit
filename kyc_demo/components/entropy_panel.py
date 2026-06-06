from __future__ import annotations

import streamlit as st

ENTROPY_THRESHOLD: float = 2.5


def render_entropy_panel(entropy: float, threshold: float = ENTROPY_THRESHOLD) -> None:
    """Renders transition entropy metric with framing and alert badge."""
    st.subheader("TRANSITION ENTROPY")
    st.metric(label="Transition Entropy", value=f"{entropy:.1f} bits")
    st.caption("Low entropy = stable governed execution paths")
    st.caption("High entropy = execution instability / policy drift signal")
    if entropy >= threshold:
        st.error("⚠ GOVERNANCE ALERT: Execution instability detected.")
        st.caption("Transition paths diverging from baseline.")
    else:
        st.success("DETERMINISTIC")
