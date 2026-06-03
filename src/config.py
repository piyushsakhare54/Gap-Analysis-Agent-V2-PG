from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    provider: str = "heuristic"
    temperature: float = 0
    allow_heuristic_fallback: bool = True
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout_seconds: int = 900
    ollama_think: bool = False
    ollama_num_predict: int = 8192


class AgentConfig(BaseModel):
    provider: str = "heuristic"
    model: str = "heuristic"


class AgentsConfig(BaseModel):
    requirements_extractor: AgentConfig = Field(default_factory=AgentConfig)
    solution_extractor: AgentConfig = Field(default_factory=AgentConfig)
    gap_analyzer: AgentConfig = Field(default_factory=AgentConfig)
    gap_critic: AgentConfig = Field(default_factory=AgentConfig)


class RetrievalConfig(BaseModel):
    embedding_provider: str = "hashing"
    embedding_model: str = "BAAI/bge-m3"
    top_k: int = 5
    min_score: float = 0.15
    chunk_max_lines: int = 40
    chunk_overlap_lines: int = 5
    gap_analysis_batch_size: int = 8


class AppConfig(BaseModel):
    run: RunConfig = Field(default_factory=RunConfig)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to load YAML configs. Install requirements.txt.") from exc
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {path}")
    return data


def load_config(path: Path | None = None) -> AppConfig:
    default_path = Path("configs/default.yaml")
    data = _read_yaml(default_path)
    if path:
        data = _deep_merge(data, _read_yaml(path))
    return AppConfig(**data)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
