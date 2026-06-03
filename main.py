from __future__ import annotations

import argparse
from pathlib import Path

from src.config import load_config
from src.orchestrator import run_pipeline
from src.orchestrator_large import run_large_pipeline
from src.reporting import write_report
from dotenv import load_dotenv

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Requirements Gap Analysis Agent")
    parser.add_argument("--mode", choices=["standard", "large"], default="standard")
    parser.add_argument("--business", required=True, type=Path, help="Business transcript file or directory")
    parser.add_argument("--engineering", required=True, type=Path, help="Engineering transcript file or directory")
    parser.add_argument("--output", required=True, type=Path, help="Report output path")
    parser.add_argument("--format", choices=["markdown", "json", "jsonl"], default="markdown")
    parser.add_argument("--config", type=Path, default=None, help="Optional YAML config override")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    if args.mode == "large":
        report = run_large_pipeline(args.business, args.engineering, config)
    else:
        report = run_pipeline(args.business, args.engineering, config)
    write_report(report, args.output, args.format)
    print(f"Wrote {args.mode} {args.format} report to {args.output}")


if __name__ == "__main__":
    main()

