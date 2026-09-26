"""Local-first redaction for common prompt-sharing hazards."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class Finding:
    """A category and count of values replaced in the input."""

    category: str
    count: int


@dataclass(frozen=True)
class RedactionResult:
    text: str
    findings: tuple[Finding, ...]


_PATTERNS: tuple[tuple[str, Pattern[str], str], ...] = (
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    ("phone", re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)"), "[REDACTED_PHONE]"),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"), "[REDACTED_API_KEY]"),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    ("bearer", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{12,}"), "Bearer [REDACTED_TOKEN]"),
    ("secret_assignment", re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"), r"\1=[REDACTED_SECRET]"),
)


def redact(text: str) -> RedactionResult:
    """Replace common sensitive values without making network calls."""

    findings: list[Finding] = []
    redacted = text
    for category, pattern, replacement in _PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        if count:
            findings.append(Finding(category, count))
    return RedactionResult(redacted, tuple(findings))


def main() -> int:
    result = redact(sys.stdin.read())
    sys.stdout.write(result.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
