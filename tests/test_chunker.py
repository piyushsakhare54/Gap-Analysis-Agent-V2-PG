import pytest

from src.chunking import chunk_transcripts
from src.schemas import Transcript, TranscriptLine


def make_transcript(count: int) -> Transcript:
    return Transcript(
        transcript_id="biz",
        kind="business",
        source_path="biz.txt",
        lines=[TranscriptLine(line_number=i, speaker="PM", text=f"line {i}") for i in range(1, count + 1)],
    )


def test_chunk_ranges_and_overlap() -> None:
    chunks = chunk_transcripts([make_transcript(100)], max_lines=40, overlap_lines=5)
    assert [(chunk.line_start, chunk.line_end) for chunk in chunks] == [(1, 40), (36, 75), (71, 100)]
    assert chunks[1].text.startswith("[line 36]")


def test_empty_transcript_list_returns_empty() -> None:
    assert chunk_transcripts([]) == []


def test_invalid_overlap_raises() -> None:
    with pytest.raises(ValueError):
        chunk_transcripts([make_transcript(10)], max_lines=5, overlap_lines=5)

