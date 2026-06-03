from __future__ import annotations

import json
from typing import Any

from src.agents.ollama_client import OllamaJSONClient
from src.config import AppConfig
from src.rules import build_deterministic_gaps
from src.schemas import Gap, Requirement, RequirementMatchSet, Solution


def analyze_gaps(requirements: list[Requirement], solutions: list[Solution], config: AppConfig, warnings: list[str] | None = None) -> list[Gap]:
    if config.agents.gap_analyzer.provider == "ollama":
        return _analyze_gaps_with_ollama(requirements, solutions, config, warnings)
    if config.agents.gap_analyzer.provider != "heuristic" and not config.run.allow_heuristic_fallback:
        raise ValueError(f"Unsupported gap analyzer provider: {config.agents.gap_analyzer.provider}")
    return build_deterministic_gaps(requirements, solutions)


def analyze_match_sets_gaps(
    match_sets: list[RequirementMatchSet],
    config: AppConfig,
    warnings: list[str] | None = None,
) -> list[Gap]:
    if config.agents.gap_analyzer.provider != "ollama":
        gaps: list[Gap] = []
        for match_set in match_sets:
            gaps.extend(build_deterministic_gaps([match_set.requirement], match_set.candidate_solutions))
        return _renumber_gaps(gaps)

    batch_size = max(1, config.retrieval.gap_analysis_batch_size)
    gaps: list[Gap] = []
    for start in range(0, len(match_sets), batch_size):
        batch = match_sets[start : start + batch_size]
        gaps.extend(_analyze_match_set_batch_with_ollama(batch, config, warnings, len(gaps)))
    return _renumber_gaps(gaps)


def _analyze_gaps_with_ollama(
    requirements: list[Requirement],
    solutions: list[Solution],
    config: AppConfig,
    warnings: list[str] | None,
) -> list[Gap]:
    client = OllamaJSONClient(
        config.run.ollama_base_url,
        config.run.temperature,
        config.run.ollama_timeout_seconds,
        think=config.run.ollama_think,
        num_predict=config.run.ollama_num_predict,
    )
    gaps: list[Gap] = []
    for requirement in requirements:
        try:
            data = client.generate_json(
                model=config.agents.gap_analyzer.model,
                system=(
                    "You are a senior software requirements gap analyst. Return only valid JSON. "
                    "Do not include markdown, prose, or hidden reasoning."
                ),
                user=_gap_prompt(requirement, solutions),
            )
        except Exception as exc:
            if not config.run.allow_heuristic_fallback:
                raise RuntimeError(f"Ollama gap analysis failed and heuristic fallback is disabled: {exc}") from exc
            if warnings is not None:
                warnings.append(f"Ollama gap analysis failed, using heuristic fallback: {exc}")
            return build_deterministic_gaps(requirements, solutions)
        for item in data.get("gaps", []):
            if isinstance(item, dict):
                gap = _gap_from_llm_item(item, requirement, len(gaps) + 1)
                if gap.status != "covered":
                    gaps.append(gap)
    return _renumber_gaps(gaps)


def _analyze_match_set_batch_with_ollama(
    match_sets: list[RequirementMatchSet],
    config: AppConfig,
    warnings: list[str] | None,
    offset: int,
) -> list[Gap]:
    client = OllamaJSONClient(config.run.ollama_base_url, config.run.temperature, config.run.ollama_timeout_seconds)
    try:
        data = client.generate_json(
            model=config.agents.gap_analyzer.model,
            system=(
                "You are a senior software requirements gap analyst. Return only valid JSON. "
                "Do not include markdown, prose, or hidden reasoning."
            ),
            user=_gap_batch_prompt(match_sets),
        )
    except Exception as exc:
        if not config.run.allow_heuristic_fallback:
            raise RuntimeError(f"Ollama batched gap analysis failed and heuristic fallback is disabled: {exc}") from exc
        if warnings is not None:
            warnings.append(f"Ollama batched gap analysis failed, using heuristic fallback: {exc}")
        fallback: list[Gap] = []
        for match_set in match_sets:
            fallback.extend(build_deterministic_gaps([match_set.requirement], match_set.candidate_solutions))
        return fallback

    gaps: list[Gap] = []
    requirements_by_id = {match_set.requirement.requirement_id: match_set.requirement for match_set in match_sets}
    for item in data.get("gaps", []):
        if not isinstance(item, dict):
            continue
        requirement_id = str(item.get("requirement_id") or "").strip()
        requirement = requirements_by_id.get(requirement_id)
        if requirement is None:
            continue
        gap = _gap_from_llm_item(item, requirement, offset + len(gaps) + 1)
        if gap.status != "covered":
            gaps.append(gap)
    return gaps


def _gap_prompt(requirement: Requirement, solutions: list[Solution]) -> str:
    solution_block = "\n".join(
        f"- {solution.solution_id}: {solution.what}\n"
        f"  deferred={solution.deferred}; scope_limits={solution.scope_limits}; tech_stack={solution.tech_stack}"
        for solution in solutions
    ) or "No candidate engineering solutions were retrieved."
    return (
        "Compare one requirement against the retrieved candidate engineering solutions. "
        "Return JSON with key `gaps`, an array. Return an empty array if the requirement is fully covered. "
        "If not fully covered, create one object with: requirement_id, status, severity, evidence, recommendation, confidence. "
        "Allowed status values: unaddressed, partial, covered. Allowed severity values: low, medium, high. "
        "Use partial when a solution exists but is deferred, out of scope, incomplete, or missing required constraints.\n\n"
        f"Requirement id: {requirement.requirement_id}\n"
        f"Requirement: {requirement.statement}\n"
        f"Constraints: {requirement.constraints}\n\n"
        f"Candidate solutions:\n{solution_block}"
    )


def _gap_batch_prompt(match_sets: list[RequirementMatchSet]) -> str:
    cases = []
    for match_set in match_sets:
        candidates = [
            {
                "solution_id": solution.solution_id,
                "what": solution.what,
                "deferred": solution.deferred,
                "scope_limits": solution.scope_limits,
                "tech_stack": solution.tech_stack,
                "retrieval_score": next(
                    (round(match.score, 4) for match in match_set.matches if match.solution_id == solution.solution_id),
                    None,
                ),
            }
            for solution in match_set.candidate_solutions
        ]
        cases.append(
            {
                "requirement_id": match_set.requirement.requirement_id,
                "requirement": match_set.requirement.statement,
                "constraints": match_set.requirement.constraints,
                "candidate_solutions": candidates,
            }
        )
    return (
        "Analyze these requirement coverage cases strictly. Return JSON with key `gaps`, an array. "
        "For each case, decide whether the candidate solutions fully satisfy the exact requirement. "
        "For fully covered requirements, do not include a gap. For missing or incomplete coverage, include one gap object. "
        "Each gap object must have: requirement_id, status, severity, evidence, recommendation, confidence. "
        "Allowed status values: unaddressed, partial, covered. Allowed severity values: low, medium, high. "
        "Use partial when a candidate solution exists but is deferred, out of scope, incomplete, or missing required constraints. "
        "Use unaddressed when no candidate solution covers the requirement. "
        "Important: a semantically similar solution is not coverage unless it explicitly satisfies the requirement. "
        "If a solution says planned, deferred, not implemented, not included, unavailable, or future work, that is a gap.\n\n"
        f"Cases JSON:\n{json.dumps(cases, indent=2)}"
    )


def _gap_from_llm_item(item: dict[str, Any], requirement: Requirement, index: int) -> Gap:
    status = str(item.get("status") or "unaddressed").strip().lower()
    if status not in {"unaddressed", "partial", "covered"}:
        status = "unaddressed"
    severity = str(item.get("severity") or "medium").strip().lower()
    if severity not in {"low", "medium", "high"}:
        severity = "medium"
    return Gap(
        gap_id=f"GAP-{index:04d}",
        requirement_id=requirement.requirement_id,
        requirement_statement=requirement.statement,
        status=status,
        severity=severity,
        evidence=_string_list(item.get("evidence")),
        recommendation=str(item.get("recommendation") or "Confirm the implementation plan for this requirement.").strip(),
        confidence=_confidence_value(item.get("confidence")),
    )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _confidence_value(value: Any) -> float:
    if value is None:
        return 0.75
    if isinstance(value, (int, float)):
        return _clamp_confidence(float(value))
    text = str(value).strip().lower()
    label_map = {
        "very high": 0.95,
        "high": 0.85,
        "medium": 0.65,
        "moderate": 0.65,
        "low": 0.4,
        "very low": 0.2,
    }
    if text in label_map:
        return label_map[text]
    try:
        return _clamp_confidence(float(text))
    except ValueError:
        return 0.75


def _clamp_confidence(value: float) -> float:
    if value > 10 and value <= 100:
        value = value / 100
    return max(0.0, min(1.0, value))


def _renumber_gaps(gaps: list[Gap]) -> list[Gap]:
    for index, gap in enumerate(gaps, start=1):
        gap.gap_id = f"GAP-{index:04d}"
    return gaps
