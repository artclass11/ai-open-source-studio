from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_MODEL = "Qwen/Qwen3.5-4B"

TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".kts", ".go", ".rs",
    ".c", ".h", ".cc", ".cpp", ".hpp", ".cs", ".swift", ".php", ".rb", ".r",
    ".sql", ".sh", ".bash", ".zsh", ".ps1", ".md", ".mdx", ".txt", ".rst",
    ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".xml", ".html", ".css",
    ".scss", ".sass", ".vue", ".svelte", ".graphql", ".proto"
}

SKIP_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".venv", "venv", "node_modules",
    "dist", "build", "target", "coverage", "__pycache__", ".next", ".nuxt",
    ".cache", ".pytest_cache", ".mypy_cache", ".tox"
}

SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
    "credentials.json", "service-account.json", ".npmrc"
}

MAX_FILE_BYTES = 160_000


@dataclass(frozen=True)
class RepoFile:
    path: str
    text: str
    size: int


@dataclass(frozen=True)
class ScanStats:
    considered: int
    skipped: int
    bytes_read: int


def _is_secret_name(name: str) -> bool:
    lower = name.lower()
    return lower in SECRET_NAMES or lower.endswith((".pem", ".key", ".p12", ".pfx"))


def _looks_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:4096]
    except OSError:
        return True
    return b"\x00" in sample


def scan_repository(root: str | Path, max_files: int = 250) -> tuple[list[RepoFile], ScanStats]:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError(f"Repository path is not a directory: {root}")

    files: list[RepoFile] = []
    skipped = 0
    bytes_read = 0

    for path in sorted(root_path.rglob("*")):
        if len(files) >= max_files:
            skipped += 1
            continue
        if not path.is_file():
            continue

        rel = path.relative_to(root_path)
        if any(part in SKIP_DIRS for part in rel.parts) or _is_secret_name(path.name):
            skipped += 1
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            skipped += 1
            continue

        try:
            size = path.stat().st_size
        except OSError:
            skipped += 1
            continue
        if size > MAX_FILE_BYTES or _looks_binary(path):
            skipped += 1
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            skipped += 1
            continue

        files.append(RepoFile(path=rel.as_posix(), text=text, size=size))
        bytes_read += size

    return files, ScanStats(considered=len(files), skipped=skipped, bytes_read=bytes_read)


def chunk_files(files: Iterable[RepoFile], max_chars: int = 100_000) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    current_chars = 0

    for item in files:
        block = f"\n### FILE: {item.path}\n{item.text}\n"
        if current and current_chars + len(block) > max_chars:
            blocks.append("".join(current))
            current = []
            current_chars = 0
        current.append(block)
        current_chars += len(block)

    if current:
        blocks.append("".join(current))
    return blocks


def build_prompt(
    files: list[RepoFile],
    question: str | None = None,
    image_attached: bool = False,
) -> str:
    file_index = "\n".join(f"- {f.path} ({f.size} bytes)" for f in files)
    context_chunks = chunk_files(files, max_chars=95_000)
    context = context_chunks[0] if context_chunks else ""

    task = question or "Audit this repository and explain its architecture, risks, and the most useful next engineering steps."
    image_note = (
        "A screenshot is also supplied. Use it only as supporting evidence for UI or architecture observations."
        if image_attached
        else "No screenshot is supplied."
    )

    return f"""You are RepoLens, a careful local software reviewer.

User task:
{task}

{image_note}

Repository file index:
{file_index}

Repository contents:
{context}

Return valid JSON with exactly these top-level keys:
summary, architecture, key_files, risks, next_steps, uncertainty.

Rules:
- Base observations only on the supplied repository evidence.
- Never invent files, dependencies, endpoints, tests, or behavior.
- key_files must be an array of objects with path and reason.
- risks must be an array of objects with severity, title, evidence, and recommendation.
- next_steps must be an array of concrete engineering tasks.
- uncertainty must explicitly mention important gaps or missing evidence.
- Do not expose secrets even if they appear in supplied text.
"""


def extract_json(text: str) -> dict:
    cleaned = text.strip()
    fence = chr(96) * 3
    fenced = re.search(
        fence + r"(?:json)?\s*(.*?)\s*" + fence,
        cleaned,
        re.DOTALL | re.IGNORECASE,
    )
    if fenced:
        cleaned = fenced.group(1).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("Model did not return a JSON object.")
    return json.loads(cleaned[start : end + 1])


def load_model(model_name: str = DEFAULT_MODEL):
    try:
        from transformers import AutoModelForMultimodalLM, AutoProcessor
    except ImportError as exc:
        raise RuntimeError("Install the project dependencies before running RepoLens.") from exc

    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForMultimodalLM.from_pretrained(model_name, device_map="auto")
    return processor, model


def analyze(
    files: list[RepoFile],
    question: str | None = None,
    model_name: str = DEFAULT_MODEL,
    image_path: str | Path | None = None,
) -> dict:
    processor, model = load_model(model_name)

    content: list[dict] = [{
        "type": "text",
        "text": build_prompt(
            files,
            question=question,
            image_attached=image_path is not None,
        ),
    }]

    if image_path is not None:
        from PIL import Image
        image = Image.open(image_path).convert("RGB")
        content.insert(0, {"type": "image", "image": image})

    messages = [{"role": "user", "content": content}]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=1400, do_sample=False)
    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    decoded = processor.decode(generated, skip_special_tokens=True)
    return extract_json(decoded)
