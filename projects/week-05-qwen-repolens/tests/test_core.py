from pathlib import Path

from qwen_repolens.core import RepoFile, build_prompt, chunk_files, extract_json, scan_repository


def test_scan_skips_secrets_and_binary(tmp_path: Path):
    (tmp_path / "app.py").write_text("print('ok')", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=x", encoding="utf-8")
    (tmp_path / "image.bin").write_bytes(b"\x00\x01\x02")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.js").write_text("bad", encoding="utf-8")

    files, stats = scan_repository(tmp_path)

    assert [f.path for f in files] == ["app.py"]
    assert stats.skipped == 3


def test_chunk_files_is_bounded():
    files = [RepoFile(path=f"{i}.py", text="x" * 20, size=20) for i in range(10)]
    chunks = chunk_files(files, max_chars=120)
    assert len(chunks) >= 2
    assert all(len(chunk) <= 180 for chunk in chunks)


def test_extract_json_accepts_fenced_output():
    data = extract_json(chr(96) * 3 + 'json\n{"ok": true}\n' + chr(96) * 3)
    assert data["ok"] is True


def test_prompt_includes_evidence():
    files = [RepoFile(path="src/app.py", text="def main(): pass", size=16)]
    prompt = build_prompt(files, question="Where is the entry point?")
    assert "src/app.py" in prompt
    assert "Where is the entry point?" in prompt
    assert "Never invent" in prompt
