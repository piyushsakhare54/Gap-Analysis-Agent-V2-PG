from __future__ import annotations

import re
from typing import Any

from src.config import AppConfig
from src.agents.ollama_client import OllamaJSONClient
from src.schemas import Requirement, Solution, Transcript


REQUIREMENT_HINTS = (
    "must",
    "shall",
    "need",
    "needs",
    "require",
    "requires",
    "requirement",
    "should",
    "compliance",
    "sla",
)
SOLUTION_HINTS = (
    "implemented",
    "built",
    "supports",
    "solution",
    "using",
    "service",
    "api",
    "database",
    "queue",
    "cache",
    "deferred",
    "out of scope",
)
TECH_TERMS = ("python", "fastapi", "postgres", "redis", "kafka", "s3", "aws", "azure", "gcp", "react", "api")


def extract_requirements(transcripts: list[Transcript], config: AppConfig, warnings: list[str] | None = None) -> list[Requirement]:
    if config.agents.requirements_extractor.provider == "ollama":
        return _extract_requirements_with_ollama(transcripts, config, warnings)
    if config.agents.requirements_extractor.provider != "heuristic" and not config.run.allow_heuristic_fallback:
        raise ValueError(f"Unsupported requirements extractor provider: {config.agents.requirements_extractor.provider}")
    requirements: list[Requirement] = []
    for transcript in transcripts:
        for line in transcript.lines:
            normalized = line.text.lower()
            if _has_hint(normalized, REQUIREMENT_HINTS):
                requirements.append(
                    Requirement(
                        requirement_id=f"REQ-{len(requirements) + 1:04d}",
                        statement=_clean_statement(line.text),
                        source_transcript=transcript.transcript_id,
                        source_quote=line.text,
                        source_line_range=(line.line_number, line.line_number),
                        confidence=0.72,
                        constraints=_extract_constraints(line.text),
                    )
                )
    return requirements


def extract_solutions(transcripts: list[Transcript], config: AppConfig, warnings: list[str] | None = None) -> list[Solution]:
    if config.agents.solution_extractor.provider == "ollama":
        return _extract_solutions_with_ollama(transcripts, config, warnings)
    if config.agents.solution_extractor.provider != "heuristic" and not config.run.allow_heuristic_fallback:
        raise ValueError(f"Unsupported solution extractor provider: {config.agents.solution_extractor.provider}")
    solutions: list[Solution] = []
    for transcript in transcripts:
        for line in transcript.lines:
            normalized = line.text.lower()
            if _has_hint(normalized, SOLUTION_HINTS):
                solutions.append(
                    Solution(
                        solution_id=f"SOL-{len(solutions) + 1:04d}",
                        what=_clean_statement(line.text),
                        source_transcript=transcript.transcript_id,
                        source_quote=line.text,
                        source_line_range=(line.line_number, line.line_number),
                        confidence=0.72,
                        tech_stack=_extract_tech(line.text),
                        deferred=_extract_deferred(line.text),
                        scope_limits=_extract_scope_limits(line.text),
                    )
                )
    return solutions


def _has_hint(text: str, hints: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(hint)}\b", text) for hint in hints)


def _clean_statement(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_constraints(text: str) -> list[str]:
    constraints = []
    lowered = text.lower()
    for marker in ("within", "under", "at least", "no more than", "sla", "compliance"):
        if marker in lowered:
            constraints.append(text.strip())
            break
    return constraints


def _extract_tech(text: str) -> list[str]:
    lowered = text.lower()
    return sorted({term for term in TECH_TERMS if term in lowered})


def _extract_deferred(text: str) -> list[str]:
    return [text.strip()] if "deferred" in text.lower() or "later" in text.lower() else []


def _extract_scope_limits(text: str) -> list[str]:
    lowered = text.lower()
    if "not included" in lowered or "out of scope" in lowered or "only" in lowered:
        return [text.strip()]
    return []


def _extract_requirements_with_ollama(transcripts: list[Transcript], config: AppConfig, warnings: list[str] | None) -> list[Requirement]:
    client = _ollama_client(config)
    requirements: list[Requirement] = []
    for transcript in transcripts:
        try:
            data = client.generate_json(
                model=config.agents.requirements_extractor.model,
                system=_json_system_prompt(),
                user=_requirements_prompt(transcript),
            )
        except Exception as exc:
            return _handle_llm_extraction_failure(exc, transcripts, config, warnings, "requirements")
        for item in data.get("requirements", []):
            if not isinstance(item, dict):
                continue
            requirement = _requirement_from_llm_item(item, transcript, len(requirements) + 1)
            if requirement.statement:
                requirements.append(requirement)
    return requirements


def _extract_solutions_with_ollama(transcripts: list[Transcript], config: AppConfig, warnings: list[str] | None) -> list[Solution]:
    client = _ollama_client(config)
    solutions: list[Solution] = []
    for transcript in transcripts:
        try:
            data = client.generate_json(
                model=config.agents.solution_extractor.model,
                system=_json_system_prompt(),
                user=_solutions_prompt(transcript),
            )
        except Exception as exc:
            return _handle_llm_extraction_failure(exc, transcripts, config, warnings, "solutions")
        for item in data.get("solutions", []):
            if not isinstance(item, dict):
                continue
            solution = _solution_from_llm_item(item, transcript, len(solutions) + 1)
            if solution.what:
                solutions.append(solution)
    return solutions


def _handle_llm_extraction_failure(
    exc: Exception,
    transcripts: list[Transcript],
    config: AppConfig,
    warnings: list[str] | None,
    kind: str,
) -> list[Requirement] | list[Solution]:
    if not config.run.allow_heuristic_fallback:
        raise RuntimeError(f"Ollama {kind} extraction failed and heuristic fallback is disabled: {exc}") from exc
    if warnings is not None:
        warnings.append(f"Ollama {kind} extraction failed, using heuristic fallback: {exc}")
    if kind == "requirements":
        return _extract_requirements_heuristic(transcripts)
    return _extract_solutions_heuristic(transcripts)


def _ollama_client(config: AppConfig) -> OllamaJSONClient:
    return OllamaJSONClient(
        config.run.ollama_base_url,
        config.run.temperature,
        config.run.ollama_timeout_seconds,
        think=config.run.ollama_think,
        num_predict=config.run.ollama_num_predict,
    )


def _extract_requirements_heuristic(transcripts: list[Transcript]) -> list[Requirement]:
    requirements: list[Requirement] = []
    for transcript in transcripts:
        for line in transcript.lines:
            normalized = line.text.lower()
            if _has_hint(normalized, REQUIREMENT_HINTS):
                requirements.append(
                    Requirement(
                        requirement_id=f"REQ-{len(requirements) + 1:04d}",
                        statement=_clean_statement(line.text),
                        source_transcript=transcript.transcript_id,
                        source_quote=line.text,
                        source_line_range=(line.line_number, line.line_number),
                        confidence=0.72,
                        constraints=_extract_constraints(line.text),
                    )
                )
    return requirements


def _extract_solutions_heuristic(transcripts: list[Transcript]) -> list[Solution]:
    solutions: list[Solution] = []
    for transcript in transcripts:
        for line in transcript.lines:
            normalized = line.text.lower()
            if _has_hint(normalized, SOLUTION_HINTS):
                solutions.append(
                    Solution(
                        solution_id=f"SOL-{len(solutions) + 1:04d}",
                        what=_clean_statement(line.text),
                        source_transcript=transcript.transcript_id,
                        source_quote=line.text,
                        source_line_range=(line.line_number, line.line_number),
                        confidence=0.72,
                        tech_stack=_extract_tech(line.text),
                        deferred=_extract_deferred(line.text),
                        scope_limits=_extract_scope_limits(line.text),
                    )
                )
    return solutions


def _json_system_prompt() -> str:
    return (
        "You are a senior requirements analysis agent. Return only valid JSON. "
        "Return compact JSON with no markdown, prose, or hidden reasoning."
    )


def _requirements_prompt(transcript: Transcript) -> str:
    return (
        "Extract business requirements from this transcript. Return JSON with key `requirements`, an array of objects. "
        "Each object must have: statement, source_quote, line_start, line_end, confidence, constraints, notes. "
        "Use only evidence in the transcript. Preserve original line numbers. "
        "Keep source_quote under 180 characters. Use [] for empty arrays. Do not duplicate or paraphrase the same requirement twice.\n\n"
        f"Transcript id: {transcript.transcript_id}\n"
        f"Transcript:\n{_format_transcript(transcript)}"
    )


def _solutions_prompt(transcript: Transcript) -> str:
    return (
        "Extract engineering solutions, implemented work, deferred work, and scope limits from this transcript. "
        "Return JSON with key `solutions`, an array of objects. Each object must have: what, source_quote, "
        "line_start, line_end, confidence, tech_stack, deferred, scope_limits, notes. "
        "Use only evidence in the transcript. Preserve original line numbers. "
        "Keep source_quote under 180 characters. tech_stack, deferred, scope_limits, and notes must be arrays. "
        "Use [] for empty arrays. Do not duplicate or paraphrase the same solution twice.\n\n"
        f"Transcript id: {transcript.transcript_id}\n"
        f"Transcript:\n{_format_transcript(transcript)}"
    )


def _format_transcript(transcript: Transcript) -> str:
    return "\n".join(f"[line {line.line_number}] {line.speaker}: {line.text}" for line in transcript.lines)


def _requirement_from_llm_item(item: dict[str, Any], transcript: Transcript, index: int) -> Requirement:
    line_start, line_end = _line_range(item, transcript)
    return Requirement(
        requirement_id=f"REQ-{index:04d}",
        statement=str(item.get("statement") or item.get("requirement") or "").strip(),
        source_transcript=transcript.transcript_id,
        source_quote=str(item.get("source_quote") or "").strip(),
        source_line_range=(line_start, line_end),
        confidence=_confidence_value(item.get("confidence")),
        constraints=_string_list(item.get("constraints")),
        notes=_string_list(item.get("notes")),
    )


def _solution_from_llm_item(item: dict[str, Any], transcript: Transcript, index: int) -> Solution:
    line_start, line_end = _line_range(item, transcript)
    return Solution(
        solution_id=f"SOL-{index:04d}",
        what=str(item.get("what") or item.get("solution") or "").strip(),
        source_transcript=transcript.transcript_id,
        source_quote=str(item.get("source_quote") or "").strip(),
        source_line_range=(line_start, line_end),
        confidence=_confidence_value(item.get("confidence")),
        tech_stack=_string_list(item.get("tech_stack")),
        deferred=_string_list(item.get("deferred")),
        scope_limits=_string_list(item.get("scope_limits")),
        notes=_string_list(item.get("notes")),
    )


def _line_range(item: dict[str, Any], transcript: Transcript) -> tuple[int, int]:
    fallback = transcript.lines[0].line_number if transcript.lines else 1
    line_start = int(item.get("line_start") or item.get("source_line_start") or fallback)
    line_end = int(item.get("line_end") or item.get("source_line_end") or line_start)
    return line_start, line_end


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
