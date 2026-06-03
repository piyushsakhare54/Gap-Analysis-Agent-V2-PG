from src.agents.extractors import _confidence_value as extractor_confidence
from src.agents.gap_analyzer import _confidence_value as gap_confidence


def test_llm_confidence_labels_are_normalized() -> None:
    assert extractor_confidence("high") == 0.85
    assert extractor_confidence("medium") == 0.65
    assert extractor_confidence("low") == 0.4
    assert gap_confidence("high") == 0.85


def test_llm_confidence_numbers_are_clamped() -> None:
    assert extractor_confidence("90") == 0.9
    assert extractor_confidence(1.5) == 1.0
    assert extractor_confidence("not sure") == 0.75

