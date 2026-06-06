from __future__ import annotations

import streamlit as st

ROWS: list[tuple[str, str]] = [
    ("AI decides execution order",   "Runtime decides execution order"),
    ("Dynamic tool access",          "Capability-gated tools"),
    ("Prompt-level controls",        "Runtime-level controls"),
    ("Logged after action",          "Blocked before action"),
    ("Best-effort audit trail",      "Integrity-verifiable execution trace"),
    ("No pre-flight validation",     "Structural validation before execution"),
]


def render_comparison_panel() -> None:
    """Renders two-column comparison table. No state, pure display."""
    st.subheader("Governance Comparison")
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### :red[Traditional Agent]")
        for left, _ in ROWS:
            st.markdown(f"- {left}")
    with col_right:
        st.markdown("### :green[nano-vm]")
        for _, right in ROWS:
            st.markdown(f"- {right}")
