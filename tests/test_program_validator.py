from __future__ import annotations


def test_valid_linear_program() -> None:
    from kyc_demo.engine.program_validator import validate_program
    steps = [
        {"id": "s1", "next_step": "s2"},
        {"id": "s2", "next_step": "s3"},
        {"id": "s3", "next_step": None},
    ]
    r = validate_program(steps)
    assert r.valid is True
    assert r.checks.missing_targets is True
    assert r.checks.unreachable_steps is True
    assert r.checks.cycle_detection is True
    assert r.errors == []


def test_missing_target() -> None:
    from kyc_demo.engine.program_validator import validate_program
    steps = [
        {"id": "s1", "next_step": "s2"},
        {"id": "s2", "next_step": "ghost"},
    ]
    r = validate_program(steps)
    assert r.valid is False
    assert r.checks.missing_targets is False
    assert len(r.errors) > 0


def test_unreachable_step() -> None:
    from kyc_demo.engine.program_validator import validate_program
    steps = [
        {"id": "s1", "next_step": "s2"},
        {"id": "s2", "next_step": None},
        {"id": "s3", "next_step": None},
    ]
    r = validate_program(steps)
    assert r.valid is False
    assert r.checks.unreachable_steps is False


def test_cycle() -> None:
    from kyc_demo.engine.program_validator import validate_program
    steps = [
        {"id": "s1", "next_step": "s2"},
        {"id": "s2", "next_step": "s3"},
        {"id": "s3", "next_step": "s1"},
    ]
    r = validate_program(steps)
    assert r.valid is False
    assert r.checks.cycle_detection is False


def test_empty_steps() -> None:
    from kyc_demo.engine.program_validator import validate_program
    r = validate_program([])
    assert r.valid is False


def test_pre_flight_panel_importable() -> None:
    from kyc_demo.components.pre_flight_panel import render_pre_flight_panel
    assert callable(render_pre_flight_panel)
