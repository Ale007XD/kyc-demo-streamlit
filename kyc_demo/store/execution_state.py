from __future__ import annotations

import streamlit as st
from dataclasses import dataclass, field

from kyc_demo.engine.mock_runtime import STEPS


@dataclass
class ExecutionState:
    execution_id: str | None = None
    current_step_index: int = -1
    steps: list[str] = field(default_factory=lambda: list(STEPS))
    step_statuses: dict[str, str] = field(default_factory=dict)
    envelopes: list[dict[str, object]] = field(default_factory=list)
    blocked_actions_total: int = 0
    running: bool = False


def get_execution_state() -> ExecutionState:
    if "execution_state" not in st.session_state:
        st.session_state["execution_state"] = ExecutionState()
    val = st.session_state["execution_state"]
    assert isinstance(val, ExecutionState)
    return val


def reset_execution_state() -> None:
    st.session_state["execution_state"] = ExecutionState()
