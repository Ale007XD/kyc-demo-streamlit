from __future__ import annotations

import time
import uuid

import streamlit as st

from kyc_demo.components.audit_panel import render_audit_panel
from kyc_demo.components.comparison_panel import render_comparison_panel
from kyc_demo.components.entropy_panel import render_entropy_panel
from kyc_demo.components.governance_stream import render_governance_stream
from kyc_demo.components.injector_panel import render_injector_panel
from kyc_demo.components.narrative_receipt import render_narrative_receipt
from kyc_demo.components.pipeline_panel import render_pipeline_panel
from kyc_demo.components.policy_lock import render_policy_lock
from kyc_demo.components.pre_flight_panel import render_pre_flight_panel
from kyc_demo.components.trace_health import render_trace_health
from kyc_demo.engine.mock_runtime import STEPS, get_next_step, run_step
from kyc_demo.engine.program_validator import validate_program
from kyc_demo.engine.trace_analyzer import analyze_trace
from kyc_demo.store.execution_state import get_execution_state, reset_execution_state
from kyc_demo.store.injector_state import get_injector_state

st.set_page_config(
    page_title="nano-vm Governed KYC Demo",
    layout="wide",
)

DEMO_PROGRAM = [{"id": s, "next_step": get_next_step(s)} for s in STEPS]

# --- state ---
exec_state = get_execution_state()
inj_state = get_injector_state()
validation_result = validate_program(DEMO_PROGRAM)
health_report = analyze_trace(
    [{"step_id": s} for s in exec_state.steps],
    metric_overrides=inj_state.metric_overrides or None,
)

# --- header ---
st.header("🔒 [GOVERNED EXECUTION MODE] — nano-vm v0.8.4")

# --- execution loop ---
if exec_state.running and exec_state.current_step_index >= 0:
    current_step = exec_state.steps[exec_state.current_step_index]
    result = run_step(current_step, exec_state.execution_id or "", exec_state.envelopes.append)
    exec_state.step_statuses[current_step] = str(result["status"])
    next_s = get_next_step(current_step)
    if next_s:
        exec_state.current_step_index += 1
        exec_state.step_statuses[next_s] = "RUNNING"
        time.sleep(0.8)
        st.rerun()
    else:
        exec_state.running = False
        st.rerun()

# --- row 1 ---
col1, col2, col3 = st.columns(3)
with col1:
    render_pre_flight_panel(validation_result)
    st.divider()
    render_comparison_panel()
with col2:
    if st.button("▶ Start Execution", disabled=exec_state.running):
        exec_state.execution_id = str(uuid.uuid4())
        exec_state.running = True
        exec_state.current_step_index = 0
        exec_state.step_statuses[exec_state.steps[0]] = "RUNNING"
        st.rerun()
    if st.button("↺ Reset"):
        reset_execution_state()
        st.rerun()
    render_pipeline_panel(exec_state)
    st.divider()
    render_governance_stream(exec_state.envelopes)
with col3:
    render_policy_lock(
        policy_name="KYC_AML_POLICY_v2",
        hash_value="sha256:a3f1b2c3d4e5f6",
        locked=exec_state.running or exec_state.current_step_index >= 0,
    )
    st.divider()
    render_trace_health(health_report)

# --- row 2 ---
col4, col5 = st.columns(2)
with col4:
    render_entropy_panel(health_report.transition_entropy)
with col5:
    render_injector_panel(inj_state)

# --- row 3 ---
col6, col7 = st.columns(2)
with col6:
    render_narrative_receipt(exec_state, health_report)
with col7:
    render_audit_panel(exec_state)
