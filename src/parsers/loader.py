from __future__ import annotations

import json
from pathlib import Path

from src.schemas import Transcript, TranscriptLine


SUPPORTED_EXTENSIONS = {".txt", ".md", ".jsonl"}


def load_transcripts(path: Path, kind: str) -> list[Transcript]:
    if not path.exists():
        raise FileNotFoundError(f"Transcript path does not exist: {path}")
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    return [_parse_file(file_path, kind) for file_path in files]


def _parse_file(path: Path, kind: str) -> Transcript:
    if path.suffix.lower() == ".jsonl":
        lines = _parse_jsonl(path)
    else:
        lines = _parse_text(path)
    return Transcript(
        transcript_id=path.stem,
        kind=kind,
        source_path=str(path),
        lines=lines,
    )


def _parse_text(path: Path) -> list[TranscriptLine]:
    parsed: list[TranscriptLine] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            text = raw.strip()
            if not text:
                continue
            speaker, body = _split_speaker(text)
            parsed.append(TranscriptLine(line_number=line_number, speaker=speaker, text=body))
    return parsed


def _parse_jsonl(path: Path) -> list[TranscriptLine]:
    parsed: list[TranscriptLine] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            speaker = str(item.get("speaker") or item.get("role") or "unknown")
            text = str(item.get("text") or item.get("content") or "").strip()
            if text:
                parsed.append(TranscriptLine(line_number=line_number, speaker=speaker, text=text))
    return parsed


def _split_speaker(text: str) -> tuple[str, str]:
    if ":" not in text:
        return "unknown", text
    prefix, body = text.split(":", 1)
    if 1 <= len(prefix) <= 40 and all(ch.isalnum() or ch in " _-" for ch in prefix):
        return prefix.strip(), body.strip()
    return "unknown", text

