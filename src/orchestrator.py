from __future__ import annotations

from pathlib import Path

from src.agents import analyze_gaps, extract_requirements, extract_solutions, verify_gaps
from src.config import AppConfig
from src.parsers import load_transcripts
from src.schemas import GapReport, ReportMetadata


def run_pipeline(business_dir: Path, engineering_dir: Path, config: AppConfig) -> GapReport:
    warnings: list[str] = []
    business_transcripts = load_transcripts(business_dir, "business")
    engineering_transcripts = load_transcripts(engineering_dir, "engineering")
    requirements = extract_requirements(business_transcripts, config, warnings)
    solutions = extract_solutions(engineering_transcripts, config, warnings)
    candidate_gaps = analyze_gaps(requirements, solutions, config, warnings)
    gaps = verify_gaps(candidate_gaps, requirements, solutions, config, warnings)
    metadata = ReportMetadata(
        mode="standard",
        business_transcript_count=len(business_transcripts),
        engineering_transcript_count=len(engineering_transcripts),
        requirement_count=len(requirements),
        solution_count=len(solutions),
        gap_count=len(gaps),
        warnings=warnings,
        audit={
            "requirements_extractor": config.agents.requirements_extractor.provider,
            "solution_extractor": config.agents.solution_extractor.provider,
            "gap_analyzer": config.agents.gap_analyzer.provider,
            "gap_critic": config.agents.gap_critic.provider,
        },
    )
    return GapReport(metadata=metadata, requirements=requirements, solutions=solutions, gaps=gaps)
