"""Generate the next reviewed project and mark it published."""

from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog_path = root / "projects" / "catalog.json"
data = json.loads(catalog_path.read_text())
queued = next((item for item in data["projects"] if item["status"] == "queued"), None)
if queued is None:
    raise SystemExit("No queued project remains; refusing to publish arbitrary content.")

project_dir = root / "projects" / queued["id"]
project_dir.mkdir(parents=True, exist_ok=False)
module_name = queued["id"].replace("-", "_")
(project_dir / "README.md").write_text(
    f"# {queued['title']}\n\n{queued['summary']}\n\n"
    "This weekly release is generated from the reviewed studio catalog. "
    "It is intentionally local-first, dependency-light, and transparent about its limits.\n\n"
    "## Responsible use\n\n"
    "Use synthetic examples when testing. Review outputs before relying on them, "
    "and do not use this tool to make high-impact decisions about people without appropriate human oversight.\n"
)
(project_dir / f"{module_name}.py").write_text(
    '"""A transparent starter module for this reviewed weekly project."""\n\n'
    f"PROJECT_ID = {queued['id']!r}\n"
    f"PROJECT_TITLE = {queued['title']!r}\n"
    f"PROJECT_SUMMARY = {queued['summary']!r}\n\n"
    "def describe() -> dict[str, str]:\n"
    "    return {\"id\": PROJECT_ID, \"title\": PROJECT_TITLE, \"summary\": PROJECT_SUMMARY}\n"
)
(project_dir / "test_project.py").write_text(
    f"from {module_name} import describe\n\n\n"
    "def test_project_metadata_is_present():\n"
    "    metadata = describe()\n"
    "    assert metadata['id'].startswith('week-')\n"
    "    assert metadata['title']\n"
    "    assert metadata['summary']\n"
)
queued["status"] = "published"
catalog_path.write_text(json.dumps(data, indent=2) + "\n")
print(f"generated {queued['id']}")
