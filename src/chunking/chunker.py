from __future__ import annotations

from src.schemas import Chunk, Transcript


def chunk_transcripts(transcripts: list[Transcript], max_lines: int = 40, overlap_lines: int = 5) -> list[Chunk]:
    if max_lines <= 0:
        raise ValueError("max_lines must be greater than zero.")
    if overlap_lines < 0:
        raise ValueError("overlap_lines must be zero or greater.")
    if overlap_lines >= max_lines:
        raise ValueError("overlap_lines must be smaller than max_lines.")

    chunks: list[Chunk] = []
    step = max_lines - overlap_lines
    for transcript in transcripts:
        if not transcript.lines:
            continue
        start = 0
        chunk_number = 1
        while start < len(transcript.lines):
            selected = transcript.lines[start : start + max_lines]
            line_start = selected[0].line_number
            line_end = selected[-1].line_number
            text = "\n".join(
                f"[line {line.line_number}] {line.speaker}: {line.text}" for line in selected
            )
            speakers = sorted({line.speaker for line in selected if line.speaker})
            chunks.append(
                Chunk(
                    chunk_id=f"{transcript.transcript_id}-CHUNK-{chunk_number:04d}",
                    transcript_id=transcript.transcript_id,
                    kind=transcript.kind,
                    source_path=transcript.source_path,
                    line_start=line_start,
                    line_end=line_end,
                    text=text,
                    speakers=speakers,
                )
            )
            if start + max_lines >= len(transcript.lines):
                break
            start += step
            chunk_number += 1
    return chunks

