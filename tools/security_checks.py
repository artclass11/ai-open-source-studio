"""Conservative, dependency-free repository safety checks."""

from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
ignored = {".git", ".venv", "__pycache__", ".pytest_cache"}
secret_patterns = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{10,}"),
    re.compile(r"BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY"),
]
for path in root.rglob("*"):
    if not path.is_file() or any(part in ignored for part in path.parts):
        continue
    if path.stat().st_size > 1_000_000:
        raise SystemExit(f"file too large for public repo: {path}")
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    for pattern in secret_patterns:
        if pattern.search(text):
            raise SystemExit(f"possible secret found in {path}")
print("security checks passed")
