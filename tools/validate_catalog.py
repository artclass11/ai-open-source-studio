"""Validate the bounded weekly project catalog."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "projects/catalog.json").read_text())
assert data["schema_version"] == 1
ids = [item["id"] for item in data["projects"]]
assert len(ids) == len(set(ids)), "duplicate project id"
for item in data["projects"]:
    assert set(item) == {"id", "title", "summary", "release_tag", "status"}
    assert item["status"] in {"queued", "published"}
    assert item["id"].startswith("week-")
print(f"catalog valid: {len(ids)} projects")
