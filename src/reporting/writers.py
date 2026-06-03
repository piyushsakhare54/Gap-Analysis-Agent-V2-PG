from __future__ import annotations

import json
from pathlib import Path

from src.schemas import GapReport, model_to_dict


def write_report(report: GapReport, output_path: Path, report_format: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if report_format == "json":
        output_path.write_text(json.dumps(model_to_dict(report), indent=2), encoding="utf-8")
    elif report_format == "jsonl":
        with output_path.open("w", encoding="utf-8") as handle:
            for gap in report.gaps:
                handle.write(json.dumps(model_to_dict(gap)) + "\n")
    elif report_format == "markdown":
        output_path.write_text(_to_markdown(report), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported report format: {report_format}")


def _to_markdown(report: GapReport) -> str:
    metadata = report.metadata
    lines = [
        "# Requirements Gap Analysis Report",
        "",
        "## Metadata",
        f"- Mode: {metadata.mode}",
        f"- Generated at: {metadata.generated_at}",
        f"- Requirements: {len(report.requirements)}",
        f"- Solutions: {len(report.solutions)}",
        f"- Gaps: {len(report.gaps)}",
    ]
    if metadata.mode == "large":
        lines.extend(
            [
                f"- Chunks: {metadata.chunk_count}",
                f"- Embedding provider: {metadata.embedding_provider}",
                f"- Embedding model: {metadata.embedding_model}",
                f"- Top k: {metadata.top_k}",
                f"- Min score: {metadata.min_score}",
            ]
        )
    if metadata.warnings:
        lines.extend(["", "## Warnings", *[f"- {warning}" for warning in metadata.warnings]])
    if metadata.audit:
        lines.extend(["", "## Pipeline Audit"])
        for key, value in metadata.audit.items():
            lines.append(f"- {key}: {value}")

    lines.extend(["", "## Requirements"])
    for requirement in report.requirements:
        lines.append(f"- **{requirement.requirement_id}** {requirement.statement}")

    lines.extend(["", "## Solutions"])
    for solution in report.solutions:
        lines.append(f"- **{solution.solution_id}** {solution.what}")

    lines.extend(["", "## Verified Gaps"])
    if not report.gaps:
        lines.append("No verified gaps found.")
    for gap in report.gaps:
        lines.extend(
            [
                f"### {gap.gap_id}: {gap.status.title()} ({gap.severity})",
                f"- Requirement: {gap.requirement_id} - {gap.requirement_statement}",
                f"- Recommendation: {gap.recommendation}",
                f"- Verified: {gap.verified}",
                "- Evidence:",
                *[f"  - {item}" for item in gap.evidence],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
