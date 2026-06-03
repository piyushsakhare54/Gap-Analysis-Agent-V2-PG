from __future__ import annotations

import re

from src.schemas import Gap, Requirement, Solution


STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "for", "with", "by", "is", "are",
    "must", "shall", "should", "need", "needs", "require", "requires", "solution", "using",
}


def build_deterministic_gaps(requirements: list[Requirement], solutions: list[Solution]) -> list[Gap]:
    gaps: list[Gap] = []
    for requirement in requirements:
        best_solution, best_score = _best_solution(requirement, solutions)
        if best_solution and best_score >= 0.28 and not _has_delivery_blocker(best_solution):
            continue
        status = "partial" if best_score >= 0.20 else "unaddressed"
        severity = "medium" if status == "partial" else "high"
        evidence = []
        if best_solution:
            evidence.append(f"Closest solution {best_solution.solution_id} scored {best_score:.2f}: {best_solution.what}")
        else:
            evidence.append("No candidate solution was available for this requirement.")
        gaps.append(
            Gap(
                gap_id=f"GAP-{len(gaps) + 1:04d}",
                requirement_id=requirement.requirement_id,
                requirement_statement=requirement.statement,
                status=status,
                severity=severity,
                evidence=evidence,
                recommendation="Confirm ownership and add an engineering solution that explicitly covers this requirement.",
                confidence=0.78 if status == "unaddressed" else 0.66,
            )
        )
    return gaps


def _best_solution(requirement: Requirement, solutions: list[Solution]) -> tuple[Solution | None, float]:
    req_tokens = _tokens(" ".join([requirement.statement, *requirement.constraints, *requirement.notes]))
    best_solution = None
    best_score = 0.0
    for solution in solutions:
        sol_tokens = _tokens(" ".join([solution.what, *solution.tech_stack, *solution.scope_limits, *solution.deferred]))
        score = _jaccard(req_tokens, sol_tokens)
        if score > best_score:
            best_solution = solution
            best_score = score
    return best_solution, best_score


def _has_delivery_blocker(solution: Solution) -> bool:
    text = " ".join([solution.what, *solution.deferred, *solution.scope_limits]).lower()
    return any(marker in text for marker in ("deferred", "out of scope", "not included", "later", "read-only"))


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS and len(token) > 2}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))
