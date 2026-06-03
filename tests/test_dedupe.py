from src.merge import dedupe_requirements, dedupe_solutions
from src.schemas import Requirement, Solution


def req(identifier: str, statement: str) -> Requirement:
    return Requirement(
        requirement_id=identifier,
        statement=statement,
        source_transcript="biz",
        source_quote=statement,
        source_line_range=(1, 1),
        constraints=["seven years"] if "seven" in statement else [],
    )


def sol(identifier: str, what: str) -> Solution:
    return Solution(
        solution_id=identifier,
        what=what,
        source_transcript="eng",
        source_quote=what,
        source_line_range=(1, 1),
        tech_stack=["postgres"] if "Postgres" in what else [],
        scope_limits=["read only"] if "read-only" in what else [],
    )


def test_duplicate_requirements_merge_and_renumber() -> None:
    merged = dedupe_requirements(
        [
            req("REQ-1", "We need audit logs retained for seven years"),
            req("REQ-2", "Audit logs must be retained for seven years"),
        ]
    )
    assert len(merged) == 1
    assert merged[0].requirement_id == "REQ-0001"
    assert merged[0].constraints


def test_distinct_requirements_remain_separate() -> None:
    merged = dedupe_requirements(
        [
            req("REQ-1", "Portal must support passwordless login"),
            req("REQ-2", "Dashboard should load under two seconds"),
        ]
    )
    assert len(merged) == 2


def test_solution_scope_fields_combine() -> None:
    merged = dedupe_solutions(
        [
            sol("SOL-1", "Role management uses Postgres"),
            sol("SOL-2", "Role management is read-only in this release"),
        ]
    )
    assert len(merged) == 1
    assert "postgres" in merged[0].tech_stack
    assert merged[0].scope_limits
    assert merged[0].solution_id == "SOL-0001"

