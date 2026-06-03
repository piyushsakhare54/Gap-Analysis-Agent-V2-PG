# Requirements Gap Analysis Agent

An end-to-end Python pipeline that compares business requirements against engineering implementation evidence from transcripts and generates a verified gap report.

The project is designed for interview/demo use and local experimentation with open-source models. It supports both a fast deterministic baseline and a large-transcript mode powered by local Ollama models plus open-source embeddings.

## What It Does

Business and engineering conversations often happen in different meetings. This project helps answer:

- Which business requirements were implemented?
- Which requirements are only partially covered?
- Which requirements are missing, deferred, or out of scope?
- What evidence supports each gap?

The pipeline reads transcript files, extracts structured requirements and solutions, matches them semantically, runs focused gap analysis, verifies candidate gaps, and writes Markdown, JSON, or JSONL reports.

## Pipeline Overview

```text
Business transcripts
  -> parser
  -> chunker
  -> requirement extractor
  -> dedupe / merge

Engineering transcripts
  -> parser
  -> chunker
  -> solution extractor
  -> dedupe / merge

Requirements + solutions
  -> embeddings
  -> vector retrieval
  -> top-k requirement-to-solution matching
  -> focused gap analysis
  -> critic verification
  -> report writer
```

## Key Features

- Supports `.txt`, `.md`, and `.jsonl` transcripts
- Standard mode for quick local runs
- Large transcript mode with overlap-based chunking
- Local open-source LLM support through Ollama
- Qwen3:8B-ready config for extraction, gap analysis, and critic verification
- Open-source embedding support through `BAAI/bge-m3`
- Deterministic hashing embedding fallback
- Local in-memory cosine vector index, so FAISS is optional
- Markdown, JSON, and JSONL report output
- Unit tests for chunking, dedupe, retrieval, LLM parsing, JSON repair, and pipeline behavior

## Project Structure

```text
.
+-- main.py
+-- configs/
|   +-- default.yaml
|   +-- qwen_local.yaml
+-- src/
|   +-- agents/
|   +-- chunking/
|   +-- merge/
|   +-- parsers/
|   +-- retrieval/
|   +-- rules/
|   +-- reporting/
|   +-- config.py
|   +-- orchestrator.py
|   +-- orchestrator_large.py
|   +-- schemas.py
+-- tests/
+-- transcripts/
|   +-- business/
|   +-- engineering/
|   +-- eval_business/
|   +-- eval_engineering/
+-- docs/
```

## Requirements

- Python 3.10+
- Ollama, only if running local LLM mode
- Optional Hugging Face token for faster `BAAI/bge-m3` downloads

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file only for local use. Do not commit it.

```env
HF_TOKEN=hf_your_huggingface_read_token_here
```

`HF_TOKEN` is optional for public models, but it gives higher Hugging Face rate limits and faster downloads.

## Run Standard Mode

Standard mode uses the default config and is useful for fast tests and local fallback behavior.

```bash
python main.py --business transcripts/business --engineering transcripts/engineering --output reports/report.md --format markdown
```

JSON output:

```bash
python main.py --business transcripts/business --engineering transcripts/engineering --output reports/report.json --format json
```

## Run Large Transcript Mode

Large mode uses transcript chunking, dedupe, embeddings, retrieval, focused gap analysis, and critic verification.

```bash
python main.py --mode large --business transcripts/business --engineering transcripts/engineering --output reports/large_report.md --format markdown
```

## Run With Ollama and Qwen

Install Ollama from:

[https://ollama.com/download](https://ollama.com/download)

Pull the recommended local model:

```bash
ollama pull qwen3:8b
```

Check the model is installed:

```bash
ollama list
```

Run the Qwen-powered large pipeline:

```bash
python main.py --mode large --config configs/qwen_local.yaml --business transcripts/eval_business --engineering transcripts/eval_engineering --output reports/eval_large_qwen.md --format markdown
```

JSON output:

```bash
python main.py --mode large --config configs/qwen_local.yaml --business transcripts/eval_business --engineering transcripts/eval_engineering --output reports/eval_large_qwen.json --format json
```

## Configs

### `configs/default.yaml`

Good for fast local runs and tests.

- heuristic extraction / analysis
- hashing embeddings
- no external model required

### `configs/qwen_local.yaml`

Good for the product-grade local LLM demo.

- Qwen through Ollama for extraction
- Qwen through Ollama for gap analysis
- Qwen through Ollama for critic verification
- `BAAI/bge-m3` through `sentence-transformers` for embeddings
- heuristic fallback disabled

Current local model:

```yaml
model: qwen3:8b
```

If you install another model, update all four model entries in `configs/qwen_local.yaml`.

## Example Evaluation Dataset

The repo includes a larger evaluation dataset:

```text
transcripts/eval_business/enterprise_eval_business.txt
transcripts/eval_engineering/enterprise_eval_engineering.txt
```

It intentionally includes covered, partial, deferred, and missing requirements so the gap report can be evaluated.

Examples of intended gaps:

- PDF billing export not included
- dashboard performance deferred
- suspicious login spike detection not implemented
- legal hold not implemented
- EU data residency unavailable
- dark mode not implemented
- custom domains and TLS not implemented
- SCIM not implemented

## Output Report

Markdown reports include:

- metadata
- pipeline audit
- extracted requirements
- extracted solutions
- verified gaps
- evidence and recommendations

Example metadata:

```text
Mode: large
Embedding provider: sentence_transformers
Embedding model: BAAI/bge-m3
Top k: 3
Pipeline Audit:
  requirements_extractor: ollama
  solution_extractor: ollama
  gap_analyzer: ollama
  gap_critic: ollama
```

## Tests

Run:

```bash
python -m pytest -q
```

The test suite covers:

- transcript chunking
- deduplication
- retrieval
- full large pipeline behavior
- LLM confidence parsing
- Ollama JSON repair

## Troubleshooting

### Ollama returns `HTTP Error 404`

The configured model is not installed.

Check installed models:

```bash
ollama list
```

Pull the model:

```bash
ollama pull qwen3:8b
```

Or update `configs/qwen_local.yaml` to use the installed model name.

### Ollama takes too long

Use a smaller model or tune the config.

Recommended for slower machines:

```yaml
retrieval:
  top_k: 3
  chunk_max_lines: 35
  chunk_overlap_lines: 5
  gap_analysis_batch_size: 5
```

Possible models:

```text
qwen3:4b   faster, lower reasoning quality
qwen3:8b   balanced
qwen3:14b  better quality, slower
qwen3:32b  heavy for many local machines
```

### Qwen returns malformed JSON

The Ollama client includes JSON cleanup and repair for common LLM output issues:

- markdown fences
- missing commas between objects
- trailing commas
- confidence labels such as `high`, `medium`, and `low`

### Hugging Face says unauthenticated requests

Set `HF_TOKEN` in `.env`:

```env
HF_TOKEN=hf_your_token_here
```

## Production Upgrade Ideas

- Replace local in-memory vector search with Qdrant
- Use Supabase Postgres with `pgvector` for persistent retrieval
- Add async/batched Ollama calls
- Add a web dashboard
- Add run history and report comparison
- Add stronger schema validation and retry policies
- Explore knowledge graph or GNN-based reasoning as future work

## GitHub Notes

Do not commit:

- `.env`
- `.venv`
- `__pycache__`
- generated reports
- local model files
- IDE folders

The included `.gitignore` excludes these local artifacts.
