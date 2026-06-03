from __future__ import annotations

from typing import Any

from src.agents.ollama_client import OllamaJSONClient
from src.config import AppConfig
from src.schemas import Gap, Requirement, Solution


def verify_gaps(gaps: list[Gap], requirements: list[Requirement], solutions: list[Solution], config: AppConfig, warnings: list[str] | None = None) -> list[Gap]:
    if config.agents.gap_critic.provider == "ollama":
        return _verify_gaps_with_ollama(gaps, requirements, solutions, config, warnings)
    if config.agents.gap_critic.provider != "heuristic" and not config.run.allow_heuristic_fallback:
        raise ValueError(f"Unsupported gap critic provider: {config.agents.gap_critic.provider}")
    requirement_ids = {requirement.requirement_id for requirement in requirements}
    verified: list[Gap] = []
    for gap in gaps:
        if gap.requirement_id not in requirement_ids:
            continue
        gap.verified = True
        if not gap.critic_notes:
            gap.critic_notes.append("Verified by deterministic critic.")
        verified.append(gap)
    return _renumber_gaps(verified)


def _renumber_gaps(gaps: list[Gap]) -> list[Gap]:
    for index, gap in enumerate(gaps, start=1):
        gap.gap_id = f"GAP-{index:04d}"
    return gaps


def _verify_gaps_with_ollama(
    gaps: list[Gap],
    requirements: list[Requirement],
    solutions: list[Solution],
    config: AppConfig,
    warnings: list[str] | None,
) -> list[Gap]:
    if not gaps:
        return []
    client = OllamaJSONClient(
        config.run.ollama_base_url,
        config.run.temperature,
        config.run.ollama_timeout_seconds,
        think=config.run.ollama_think,
        num_predict=config.run.ollama_num_predict,
    )
    try:
        data = client.generate_json(
            model=config.agents.gap_critic.model,
            system=(
                "You are a strict requirements gap critic. Return only valid JSON. "
                "Do not include markdown, prose, or hidden reasoning."
            ),
            user=_critic_prompt(gaps, requirements, solutions),
        )
    except Exception as exc:
        if not config.run.allow_heuristic_fallback:
            raise RuntimeError(f"Ollama gap critic failed and heuristic fallback is disabled: {exc}") from exc
        if warnings is not None:
            warnings.append(f"Ollama gap critic failed, using deterministic critic fallback: {exc}")
        return _verify_gaps_heuristic(gaps, requirements)

    decisions = {
        str(item.get("gap_id")): item
        for item in data.get("verified_gaps", [])
        if isinstance(item, dict) and item.get("keep", True)
    }
    if gaps and not decisions:
        if warnings is not None:
            warnings.append("Ollama critic returned no kept gap decisions; preserving analyzer gaps instead of dropping all results.")
        for gap in gaps:
            gap.verified = True
            gap.critic_notes = ["Preserved because critic returned no kept decisions."]
        return _renumber_gaps(gaps)
    verified: list[Gap] = []
    for gap in gaps:
        decision = decisions.get(gap.gap_id)
        if decision is None:
            continue
        gap.verified = True
        notes = _string_list(decision.get("critic_notes"))
        gap.critic_notes = notes or ["Verified by Ollama gap critic."]
        verified.append(gap)
    return _renumber_gaps(verified)


def _verify_gaps_heuristic(gaps: list[Gap], requirements: list[Requirement]) -> list[Gap]:
    requirement_ids = {requirement.requirement_id for requirement in requirements}
    verified: list[Gap] = []
    for gap in gaps:
        if gap.requirement_id in requirement_ids:
            gap.verified = True
            gap.critic_notes.append("Verified by deterministic critic.")
            verified.append(gap)
    return _renumber_gaps(verified)


def _critic_prompt(gaps: list[Gap], requirements: list[Requirement], solutions: list[Solution]) -> str:
    requirement_block = "\n".join(f"- {item.requirement_id}: {item.statement}" for item in requirements)
    solution_block = "\n".join(f"- {item.solution_id}: {item.what}; deferred={item.deferred}; scope_limits={item.scope_limits}" for item in solutions)
    gap_block = "\n".join(
        f"- {gap.gap_id}: req={gap.requirement_id}; status={gap.status}; severity={gap.severity}; evidence={gap.evidence}; recommendation={gap.recommendation}"
        for gap in gaps
    )
    return (
        "Verify candidate gaps against the requirements and engineering solutions. "
        "Return JSON with key `verified_gaps`, an array of objects. "
        "Each object must have gap_id, keep, critic_notes. Set keep=false for false positives.\n\n"
        f"Requirements:\n{requirement_block}\n\n"
        f"Solutions:\n{solution_block}\n\n"
        f"Candidate gaps:\n{gap_block}"
    )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []
