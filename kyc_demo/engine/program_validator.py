from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationChecks:
    missing_targets: bool = True
    unreachable_steps: bool = True
    cycle_detection: bool = True


@dataclass
class ValidationResult:
    valid: bool
    checks: ValidationChecks
    errors: list[str] = field(default_factory=list)


def validate_program(steps: list[dict[str, object]]) -> ValidationResult:
    """
    steps: list of {"id": str, "next_step": str | None}
    Checks:
      missing_targets:   every next_step exists as step id
      unreachable_steps: BFS from steps[0]; all ids reachable
      cycle_detection:   DFS WHITE/GRAY/BLACK; no cycle
    """
    errors: list[str] = []
    checks = ValidationChecks()

    if not steps:
        return ValidationResult(valid=False, checks=ValidationChecks(False, False, False),
                                errors=["empty steps"])

    ids: set[str] = {str(s["id"]) for s in steps}
    adj: dict[str, list[str]] = {str(s["id"]): [] for s in steps}
    for s in steps:
        nxt = s.get("next_step")
        if nxt is not None:
            adj[str(s["id"])].append(str(nxt))

    # missing_targets
    for s in steps:
        nxt = s.get("next_step")
        if nxt is not None and str(nxt) not in ids:
            checks.missing_targets = False
            errors.append(f"missing target: {nxt!r} (from {s['id']!r})")

    # unreachable_steps — BFS from steps[0]
    start = str(steps[0]["id"])
    visited: set[str] = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for nb in adj.get(node, []):
            if nb not in visited:
                queue.append(nb)
    unreachable = ids - visited
    if unreachable:
        checks.unreachable_steps = False
        errors.append(f"unreachable steps: {sorted(unreachable)}")

    # cycle_detection — DFS WHITE/GRAY/BLACK
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in ids}
    has_cycle = False

    def dfs(node: str) -> None:
        nonlocal has_cycle
        color[node] = GRAY
        for nb in adj.get(node, []):
            if nb not in color:
                continue
            if color[nb] == GRAY:
                has_cycle = True
                return
            if color[nb] == WHITE:
                dfs(nb)
        color[node] = BLACK

    for node in ids:
        if color[node] == WHITE:
            dfs(node)

    if has_cycle:
        checks.cycle_detection = False
        errors.append("cycle detected")

    valid = checks.missing_targets and checks.unreachable_steps and checks.cycle_detection
    return ValidationResult(valid=valid, checks=checks, errors=errors)
