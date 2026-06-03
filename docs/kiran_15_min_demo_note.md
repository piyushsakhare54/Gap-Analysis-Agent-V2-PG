# 15-Minute Demo Plan: Requirements Gap Analysis Agent

Hi Kiran,

In our 15-minute call, I will walk you through a product-grade AI pipeline I built in PyCharm for requirements gap analysis from large business and engineering transcripts.

## What I Will Show

I will demonstrate a working Python project that reads business transcripts and engineering transcripts, extracts structured requirements and implementation details, compares them, and generates a verified gap report.

The current setup runs locally with:

- Qwen3:8B through Ollama for LLM reasoning
- BAAI/bge-m3 for open-source embeddings
- Python 3.10+ modular pipeline
- Markdown and JSON report outputs
- PyCharm-ready project structure

## Why This Is Useful

In real projects, business teams discuss requirements in one set of meetings, while engineering teams discuss implementation decisions in another. This creates a common problem: some business requirements are fully implemented, some are partially implemented, and some are missed.

The agent helps identify those gaps automatically.

## End-to-End Pipeline I Will Explain

1. Load business and engineering transcripts
2. Split large transcripts into overlapping chunks
3. Use Qwen to extract business requirements from business chunks
4. Use Qwen to extract engineering solutions from engineering chunks
5. Deduplicate repeated items caused by chunk overlap
6. Use BAAI/bge-m3 embeddings to semantically match requirements to solutions
7. Retrieve top-k candidate solutions for each requirement
8. Use Qwen for focused gap analysis
9. Use Qwen critic verification to reduce false positives
10. Generate final Markdown or JSON reports

## What Makes It Product-Grade

- Large transcript mode avoids LLM context overflow
- Local open-source model support through Ollama
- Open-source embedding model support
- Config-driven model selection
- Deterministic fallback available for testing
- Modular codebase with schemas, agents, retrieval, chunking, merge, and reporting layers
- Unit tests for chunking, deduplication, retrieval, LLM parsing, and pipeline behavior
- Interview-friendly architecture with clear future upgrade paths like Qdrant or Supabase pgvector

## Demo Flow

I will show:

- The PyCharm project structure
- The config file using `qwen3:8b`
- The larger evaluation transcript dataset
- The command to run the pipeline
- The generated gap report
- How the report proves which requirements are covered, partial, or missing

Command I will run:

```bash
python main.py --mode large --config configs/qwen_local.yaml --business transcripts/eval_business --engineering transcripts/eval_engineering --output piyush/eval_large_qwen.md --format markdown
```

## Main Takeaway

The product is not just a prompt. It is an end-to-end AI system with parsing, chunking, LLM extraction, embedding-based retrieval, focused reasoning, critic verification, and report generation.

