from __future__ import annotations

import streamlit as st


def render_policy_lock(
    policy_name: str,
    hash_value: str,
    locked: bool,
) -> None:
    """
    locked=True:  amber badge 'LOCKED FOR EXECUTION' + hash + immutability note
    locked=False: gray badge 'UNLOCKED'
    """
    st.subheader("POLICY SNAPSHOT")
    st.markdown(f"**Policy:** `{policy_name}`")
    if locked:
        st.warning("🔒 LOCKED FOR EXECUTION")
        st.caption(f"hash: `{hash_value}`")
        st.caption("Policy snapshot is immutable for this execution.")
    else:
        st.markdown("🔓 UNLOCKED")
