from __future__ import annotations

import re
from copy import deepcopy
from typing import TypeVar

from src.schemas import Requirement, Solution


T = TypeVar("T", Requirement, Solution)
STOPWORDS = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "with", "by", "is", "are", "must", "shall", "should"}


def dedupe_requirements(requirements: list[Requirement]) -> list[Requirement]:
    merged: list[Requirement] = []
    for requirement in requirements:
        match = _find_requirement_match(merged, requirement)
        if match is None:
            merged.append(deepcopy(requirement))
        else:
            _merge_requirement(match, requirement)
    for index, requirement in enumerate(merged, start=1):
        requirement.requirement_id = f"REQ-{index:04d}"
    return merged


def dedupe_solutions(solutions: list[Solution]) -> list[Solution]:
    merged: list[Solution] = []
    for solution in solutions:
        match = _find_solution_match(merged, solution)
        if match is None:
            merged.append(deepcopy(solution))
        else:
            _merge_solution(match, solution)
    for index, solution in enumerate(merged, start=1):
        solution.solution_id = f"SOL-{index:04d}"
    return merged


def _find_requirement_match(existing: list[Requirement], candidate: Requirement) -> Requirement | None:
    for item in existing:
        if _is_duplicate(item.statement, candidate.statement, item.source_transcript, candidate.source_transcript):
            return item
    return None


def _find_solution_match(existing: list[Solution], candidate: Solution) -> Solution | None:
    for item in existing:
        if _is_duplicate(item.what, candidate.what, item.source_transcript, candidate.source_transcript):
            return item
        if item.source_transcript == candidate.source_transcript and _token_overlap(item.what, candidate.what) >= 0.5:
            return item
    return None


def _is_duplicate(left_text: str, right_text: str, left_source: str, right_source: str) -> bool:
    left = _normalize(left_text)
    right = _normalize(right_text)
    if not left or not right:
        return False
    if left == right or left in right or right in left:
        return True
    overlap = _token_overlap(left, right)
    return overlap >= 0.72 if left_source == right_source else overlap >= 0.86


def _merge_requirement(primary: Requirement, incoming: Requirement) -> None:
    if incoming.confidence > primary.confidence:
        primary.statement = incoming.statement
        primary.source_quote = incoming.source_quote
        primary.source_line_range = incoming.source_line_range
        primary.confidence = incoming.confidence
    primary.constraints = _unique([*primary.constraints, *incoming.constraints])
    primary.notes = _unique([*primary.notes, *incoming.notes, f"Merged duplicate from {incoming.source_transcript}:{incoming.source_line_range}"])


def _merge_solution(primary: Solution, incoming: Solution) -> None:
    if incoming.confidence > primary.confidence:
        primary.what = incoming.what
        primary.source_quote = incoming.source_quote
        primary.source_line_range = incoming.source_line_range
        primary.confidence = incoming.confidence
    primary.tech_stack = _unique([*primary.tech_stack, *incoming.tech_stack])
    primary.deferred = _unique([*primary.deferred, *incoming.deferred])
    primary.scope_limits = _unique([*primary.scope_limits, *incoming.scope_limits])
    primary.notes = _unique([*primary.notes, *incoming.notes, f"Merged duplicate from {incoming.source_transcript}:{incoming.source_line_range}"])


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _tokens(text: str) -> set[str]:
    return {token for token in _normalize(text).split() if token not in STOPWORDS and len(token) > 2}


def _token_overlap(left: str, right: str) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens))


def _unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        normalized = _normalize(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(value)
    return result
