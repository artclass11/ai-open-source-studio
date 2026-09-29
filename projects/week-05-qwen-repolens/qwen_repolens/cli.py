from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import DEFAULT_MODEL, analyze, scan_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repolens",
        description="Local AI repository auditor powered by Qwen3.5-4B.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect", help="Audit a local repository.")
    inspect_cmd.add_argument("path", type=Path)
    inspect_cmd.add_argument("--question", default=None)
    inspect_cmd.add_argument("--image", type=Path, default=None)
    inspect_cmd.add_argument("--model", default=DEFAULT_MODEL)
    inspect_cmd.add_argument("--max-files", type=int, default=250)
    inspect_cmd.add_argument("--format", choices=("text", "json"), default="text")
    inspect_cmd.add_argument("--output", type=Path, default=None)
    return parser


def render_text(report: dict, files_count: int, skipped: int, model_name: str) -> str:
    lines = [
        "RepoLens",
        f"Model: {model_name}",
        f"Files considered: {files_count}",
        f"Files skipped: {skipped}",
        "",
        "## Executive summary",
        report.get("summary", "No summary returned."),
        "",
        "## Architecture",
        report.get("architecture", "No architecture returned."),
        "",
        "## Key files",
    ]
    for item in report.get("key_files", []):
        lines.append(f"- {item.get('path', '?')} — {item.get('reason', '')}")

    lines += ["", "## Risks"]
    for item in report.get("risks", []):
        lines.append(
            f"- {item.get('severity', 'unknown').upper()} — "
            f"{item.get('title', '')}: {item.get('evidence', '')} "
            f"Recommendation: {item.get('recommendation', '')}"
        )

    lines += ["", "## Next steps"]
    for item in report.get("next_steps", []):
        lines.append(f"- {item}")

    lines += ["", "## Uncertainty", report.get("uncertainty", "None stated.")]
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "inspect":
        files, stats = scan_repository(args.path, max_files=args.max_files)
        if not files:
            print("No supported text files were found.")
            return 2

        report = analyze(
            files,
            question=args.question,
            model_name=args.model,
            image_path=args.image,
        )

        if args.format == "json":
            rendered = json.dumps(
                {
                    "model": args.model,
                    "files_considered": stats.considered,
                    "files_skipped": stats.skipped,
                    "bytes_read": stats.bytes_read,
                    "report": report,
                },
                indent=2,
                ensure_ascii=False,
            )
        else:
            rendered = render_text(report, stats.considered, stats.skipped, args.model)

        if args.output:
            args.output.write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
