from pathlib import Path

from src.config import load_config
from src.orchestrator_large import run_large_pipeline
from src.schemas import GapReport


def test_run_large_pipeline_produces_report() -> None:
    config = load_config(Path("configs/default.yaml"))
    report = run_large_pipeline(Path("transcripts/business"), Path("transcripts/engineering"), config)
    assert isinstance(report, GapReport)
    assert report.requirements
    assert report.solutions
    assert report.gaps
    assert report.metadata.mode == "large"

