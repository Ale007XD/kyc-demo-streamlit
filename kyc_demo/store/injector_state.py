from __future__ import annotations

import streamlit as st
from dataclasses import dataclass, field


@dataclass
class InjectorModal:
    title: str
    action: str
    reason: str
    outcome: str
    current_step: str | None = None
    required_capability: str | None = None
    granted_at: str | None = None


@dataclass
class InjectorState:
    active_injector: str | None = None
    modal: InjectorModal | None = None
    metric_overrides: dict[str, float] = field(default_factory=dict)


@dataclass
class InjectorDef:
    label: str
    modal: InjectorModal
    metric_overrides: dict[str, float]


INJECTORS: dict[str, InjectorDef] = {
    "invalid_program": InjectorDef(
        label="Invalid Program",
        modal=InjectorModal(
            title="PRE-FLIGHT VALIDATION FAILED",
            action="step 'agent_review' → 'final_check' not defined",
            reason="Structural governance gate: missing_targets check failed.",
            outcome="BLOCKED",
        ),
        metric_overrides={},
    ),
    "skip_step": InjectorDef(
        label="Skip Screening",
        modal=InjectorModal(
            title="BLOCKED ACTION: skip screen_sanctions",
            action="skip screen_sanctions",
            reason="FSM transition graph is compile-time fixed.",
            outcome="REJECTED",
        ),
        metric_overrides={"path_variance": 0.6, "transition_sequence_variance": 0.5},
    ),
    "reorder_steps": InjectorDef(
        label="Reorder Approvals",
        modal=InjectorModal(
            title="BLOCKED ACTION: reorder steps",
            action="move human_approval before agent_review",
            reason="Step ordering is immutable at runtime.",
            outcome="REJECTED",
        ),
        metric_overrides={"transition_sequence_variance": 0.55},
    ),
    "tool_injection": InjectorDef(
        label="Inject Unauthorized Tool",
        modal=InjectorModal(
            title="BLOCKED ACTION: approve_customer()",
            action="approve_customer()",
            reason="CapabilityRef not granted.",
            outcome="CapabilityDeniedError",
            current_step="adverse_media_search",
            required_capability="approval.write",
            granted_at="human_approval [step 5]",
        ),
        metric_overrides={"tool_churn_rate": 0.45, "invariant_violation_rate": 0.3},
    ),
    "policy_bypass": InjectorDef(
        label="Override Policy",
        modal=InjectorModal(
            title="BLOCKED ACTION: policy override",
            action="override_policy=True",
            reason="PolicySnapshot is frozen. Override produces hash mismatch.",
            outcome="REJECTED",
        ),
        metric_overrides={"invariant_violation_rate": 0.35},
    ),
    "corrupt_receipt": InjectorDef(
        label="Corrupt Receipt",
        modal=InjectorModal(
            title="INTEGRITY FAILURE",
            action="modify trace payload",
            reason="canonical_hash mismatch. Merkle chain: INVALID.",
            outcome="HASH_FAILURE",
        ),
        metric_overrides={"rollback_density": 0.4, "transition_entropy": 2.8},
    ),
    "gdpr_erase": InjectorDef(
        label="GDPR Erase",
        modal=InjectorModal(
            title="GdprEraseEvent executed",
            action="erase customer PII",
            reason="Customer PII: TOMBSTONED. Audit chain: PRESERVED. Governance integrity: MAINTAINED.",
            outcome="TOMBSTONED",
        ),
        metric_overrides={},
    ),
}


def get_injector_state() -> InjectorState:
    if "injector_state" not in st.session_state:
        st.session_state["injector_state"] = InjectorState()
    val = st.session_state["injector_state"]
    assert isinstance(val, InjectorState)
    return val


def trigger_injector(injector_id: str) -> None:
    inj = INJECTORS[injector_id]
    state = get_injector_state()
    state.active_injector = injector_id
    state.modal = inj.modal
    state.metric_overrides = dict(inj.metric_overrides)


def clear_modal() -> None:
    state = get_injector_state()
    state.active_injector = None
    state.modal = None
    state.metric_overrides = {}
