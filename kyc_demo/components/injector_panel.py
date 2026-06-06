from __future__ import annotations

import streamlit as st

from kyc_demo.store.injector_state import (
    INJECTORS,
    InjectorModal,
    InjectorState,
    clear_modal,
    trigger_injector,
)

OUTCOME_COLORS: dict[str, str] = {
    "REJECTED":              "🔴",
    "CapabilityDeniedError": "🟠",
    "HASH_FAILURE":          "🔴",
    "TOMBSTONED":            "🟡",
    "BLOCKED":               "🔴",
}


def render_injector_panel(state: InjectorState) -> None:
    """Renders 7 injector buttons. If modal set — renders blocked action details."""
    st.subheader("SABOTAGE INJECTORS")
    if state.modal is not None:
        render_blocked_modal(state.modal)
        return
    for injector_id, cfg in INJECTORS.items():
        if st.button(cfg.label, key=f"inj_{injector_id}"):
            trigger_injector(injector_id)
            st.rerun()


def render_blocked_modal(modal: InjectorModal) -> None:
    """Renders blocked action modal inline."""
    st.error(f"**{modal.title}**")
    st.markdown(f"**Action attempted:** `{modal.action}`")
    st.markdown(f"**Reason:** {modal.reason}")
    color = OUTCOME_COLORS.get(modal.outcome, "⚪")
    st.markdown(f"**Outcome:** {color} `{modal.outcome}`")
    if modal.current_step is not None:
        st.markdown(f"**Current step:** `{modal.current_step}`")
        st.markdown(f"**Required capability:** `{modal.required_capability}`")
        st.markdown(f"**Granted at:** {modal.granted_at}")
    if modal.outcome == "TOMBSTONED":
        st.info("Audit chain: PRESERVED. Governance integrity: MAINTAINED.")
    if st.button("Dismiss", key="dismiss_modal"):
        clear_modal()
        st.rerun()
