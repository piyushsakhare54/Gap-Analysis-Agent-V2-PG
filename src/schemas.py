from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class TranscriptLine(BaseModel):
    line_number: int
    speaker: str = "unknown"
    text: str


class Transcript(BaseModel):
    transcript_id: str
    kind: Literal["business", "engineering"]
    source_path: str
    lines: list[TranscriptLine] = Field(default_factory=list)


class Requirement(BaseModel):
    requirement_id: str
    statement: str
    source_transcript: str
    source_quote: str
    source_line_range: tuple[int, int]
    confidence: float = 0.7
    constraints: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class Solution(BaseModel):
    solution_id: str
    what: str
    source_transcript: str
    source_quote: str
    source_line_range: tuple[int, int]
    confidence: float = 0.7
    tech_stack: list[str] = Field(default_factory=list)
    deferred: list[str] = Field(default_factory=list)
    scope_limits: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class Gap(BaseModel):
    gap_id: str
    requirement_id: str
    requirement_statement: str
    status: Literal["unaddressed", "partial", "covered"]
    severity: Literal["low", "medium", "high"] = "medium"
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    confidence: float = 0.7
    verified: bool = False
    critic_notes: list[str] = Field(default_factory=list)


class Chunk(BaseModel):
    chunk_id: str
    transcript_id: str
    kind: Literal["business", "engineering"]
    source_path: str
    line_start: int
    line_end: int
    text: str
    speakers: list[str] = Field(default_factory=list)


class RetrievalMatch(BaseModel):
    requirement_id: str
    solution_id: str
    score: float
    reason: str | None = None


class RequirementMatchSet(BaseModel):
    requirement: Requirement
    matches: list[RetrievalMatch] = Field(default_factory=list)
    candidate_solutions: list[Solution] = Field(default_factory=list)


class ReportMetadata(BaseModel):
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mode: str = "standard"
    business_transcript_count: int = 0
    engineering_transcript_count: int = 0
    requirement_count: int = 0
    solution_count: int = 0
    gap_count: int = 0
    chunk_count: int = 0
    embedding_provider: str | None = None
    embedding_model: str | None = None
    top_k: int | None = None
    min_score: float | None = None
    warnings: list[str] = Field(default_factory=list)
    audit: dict[str, Any] = Field(default_factory=dict)


class GapReport(BaseModel):
    metadata: ReportMetadata = Field(default_factory=ReportMetadata)
    requirements: list[Requirement] = Field(default_factory=list)
    solutions: list[Solution] = Field(default_factory=list)
    gaps: list[Gap] = Field(default_factory=list)


def model_to_dict(model: BaseModel) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()

