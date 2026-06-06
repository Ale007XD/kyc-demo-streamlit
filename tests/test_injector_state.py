from __future__ import annotations


def test_injectors_count() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    assert len(INJECTORS) == 7


def test_injector_keys() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    expected = {
        "invalid_program", "skip_step", "reorder_steps",
        "tool_injection", "policy_bypass", "corrupt_receipt", "gdpr_erase",
    }
    assert set(INJECTORS.keys()) == expected


def test_tool_injection_outcome() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    modal = INJECTORS["tool_injection"].modal
    assert modal.outcome == "CapabilityDeniedError"
    assert modal.current_step == "adverse_media_search"
    assert modal.required_capability == "approval.write"


def test_gdpr_erase_outcome() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    modal = INJECTORS["gdpr_erase"].modal
    assert modal.outcome == "TOMBSTONED"
    assert "PRESERVED" in modal.reason


def test_metric_overrides_corrupt_receipt() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    overrides = INJECTORS["corrupt_receipt"].metric_overrides
    assert overrides["transition_entropy"] == 2.8
    assert overrides["rollback_density"] == 0.4


def test_metric_overrides_skip_step() -> None:
    from kyc_demo.store.injector_state import INJECTORS
    overrides = INJECTORS["skip_step"].metric_overrides
    assert overrides["path_variance"] == 0.6


def test_injector_panel_importable() -> None:
    from kyc_demo.components.injector_panel import render_injector_panel
    assert callable(render_injector_panel)


def test_blocked_modal_importable() -> None:
    from kyc_demo.components.injector_panel import render_blocked_modal
    assert callable(render_blocked_modal)
