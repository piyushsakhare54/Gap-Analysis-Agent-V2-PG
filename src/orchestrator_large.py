from __future__ import annotations

import re
from pathlib import Path

from src.agents import analyze_match_sets_gaps, extract_requirements, extract_solutions, verify_gaps
from src.chunking import chunk_transcripts
from src.config import AppConfig
from src.merge import dedupe_requirements, dedupe_solutions
from src.parsers import load_transcripts
from src.retrieval import EmbeddingProvider, match_requirements_to_solutions
from src.schemas import (
    Chunk,
    Gap,
    GapReport,
    ReportMetadata,
    Requirement,
    RequirementMatchSet,
    Solution,
    Transcript,
    TranscriptLine,
)


LINE_PATTERN = re.compile(r"^\[line (?P<number>\d+)\]\s*(?P<speaker>[^:]+):\s*(?P<text>.*)$")


def run_large_pipeline(business_dir: Path, engineering_dir: Path, config: AppConfig) -> GapReport:
    warnings: list[str] = []
    business_transcripts = load_transcripts(business_dir, "business")
    engineering_transcripts = load_transcripts(engineering_dir, "engineering")
    business_chunks = chunk_transcripts(
        business_transcripts,
        max_lines=config.retrieval.chunk_max_lines,
        overlap_lines=config.retrieval.chunk_overlap_lines,
    )
    engineering_chunks = chunk_transcripts(
        engineering_transcripts,
        max_lines=config.retrieval.chunk_max_lines,
        overlap_lines=config.retrieval.chunk_overlap_lines,
    )
    requirements = dedupe_requirements(extract_requirements_from_chunks(business_chunks, config, warnings))
    solutions = dedupe_solutions(extract_solutions_from_chunks(engineering_chunks, config, warnings))
    embedding_provider = EmbeddingProvider(
        provider=config.retrieval.embedding_provider,
        model_name=config.retrieval.embedding_model,
        warnings=warnings,
        allow_fallback=config.run.allow_heuristic_fallback,
    )
    match_sets = match_requirements_to_solutions(
        requirements,
        solutions,
        embedding_provider,
        top_k=config.retrieval.top_k,
        min_score=config.retrieval.min_score,
    )
    candidate_gaps = analyze_focused_gaps(match_sets, config, warnings)
    gaps = verify_gaps(candidate_gaps, requirements, solutions, config, warnings)
    metadata = ReportMetadata(
        mode="large",
        business_transcript_count=len(business_transcripts),
        engineering_transcript_count=len(engineering_transcripts),
        requirement_count=len(requirements),
        solution_count=len(solutions),
        gap_count=len(gaps),
        chunk_count=len(business_chunks) + len(engineering_chunks),
        embedding_provider=embedding_provider.active_provider,
        embedding_model=config.retrieval.embedding_model,
        top_k=config.retrieval.top_k,
        min_score=config.retrieval.min_score,
        warnings=warnings,
        audit={
            "requirements_extractor": config.agents.requirements_extractor.provider,
            "solution_extractor": config.agents.solution_extractor.provider,
            "gap_analyzer": config.agents.gap_analyzer.provider,
            "gap_critic": config.agents.gap_critic.provider,
            "retrieval": "cosine",
        },
    )
    return GapReport(metadata=metadata, requirements=requirements, solutions=solutions, gaps=gaps)


def extract_requirements_from_chunks(chunks: list[Chunk], config: AppConfig, warnings: list[str]) -> list[Requirement]:
    requirements: list[Requirement] = []
    for chunk in chunks:
        requirements.extend(extract_requirements([_chunk_to_transcript(chunk)], config, warnings))
    for index, requirement in enumerate(requirements, start=1):
        requirement.requirement_id = f"REQ-CAND-{index:04d}"
    return requirements


def extract_solutions_from_chunks(chunks: list[Chunk], config: AppConfig, warnings: list[str]) -> list[Solution]:
    solutions: list[Solution] = []
    for chunk in chunks:
        solutions.extend(extract_solutions([_chunk_to_transcript(chunk)], config, warnings))
    for index, solution in enumerate(solutions, start=1):
        solution.solution_id = f"SOL-CAND-{index:04d}"
    return solutions


def analyze_focused_gaps(
    match_sets: list[RequirementMatchSet],
    config: AppConfig,
    warnings: list[str],
) -> list[Gap]:
    candidate_gaps = analyze_match_sets_gaps(match_sets, config, warnings)
    seen: set[tuple[str, str]] = set()
    unique: list[Gap] = []
    for gap in candidate_gaps:
        key = (gap.requirement_id, gap.status)
        if key not in seen:
            seen.add(key)
            unique.append(gap)
    for index, gap in enumerate(unique, start=1):
        gap.gap_id = f"GAP-{index:04d}"
    return unique


def _chunk_to_transcript(chunk: Chunk) -> Transcript:
    lines: list[TranscriptLine] = []
    for raw_line in chunk.text.splitlines():
        match = LINE_PATTERN.match(raw_line)
        if not match:
            continue
        lines.append(
            TranscriptLine(
                line_number=int(match.group("number")),
                speaker=match.group("speaker").strip(),
                text=match.group("text").strip(),
            )
        )
    return Transcript(
        transcript_id=chunk.transcript_id,
        kind=chunk.kind,
        source_path=chunk.source_path,
        lines=lines,
    )
