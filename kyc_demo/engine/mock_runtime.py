from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime, timezone

STEPS: tuple[str, ...] = (
    "collect_customer_data",
    "screen_sanctions",
    "adverse_media_search",
    "agent_review",
    "human_approval",
    "governance_seal",
)

STEP_LABELS: dict[str, str] = {
    "collect_customer_data": "Collect Customer Data",
    "screen_sanctions":      "Screen Sanctions",
    "adverse_media_search":  "Adverse Media Search",
    "agent_review":          "Agent Review",
    "human_approval":        "Human Approval",
    "governance_seal":       "Governance Seal",
}


def run_step(
    step_id: str,
    execution_id: str,
    on_envelope: Callable[[dict[str, object]], None],
) -> dict[str, object]:
    envelope: dict[str, object] = {
        "execution_id": execution_id,
        "step_id": step_id,
        "policy_hash": "sha256:a3f1b2c3",
        "canonical_snapshot_hash": "sha256:b2e4c5d6",
        "timestamp": _now_iso(),
        "payload": {"step_id": step_id, "result": "success"},
    }
    on_envelope(envelope)
    return {"step_id": step_id, "status": "SUCCESS", "blocked_actions": 0}


def get_next_step(current_step_id: str) -> str | None:
    idx = STEPS.index(current_step_id) if current_step_id in STEPS else -1
    if idx == -1 or idx == len(STEPS) - 1:
        return None
    return STEPS[idx + 1]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
