#!/usr/bin/env python3
"""Build a normalized bundled OpenSCAD library index from MakerWorld evidence."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = REPO_ROOT / "sources" / "raw" / "makerworld" / "libraries-0.8.0.json"
DATA_PATH = REPO_ROOT / "data" / "bundled-library-index.json"
SOURCE_URL = "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json"

VERSION_NOTES = {
    "BOSL2": {
        "version_hint": "Inventory description says `v2.0`; Bambu's v1.1.0 release separately documents BOSL2 commit `99fcfc6867e739aa1cd8ffc49fe39276036681f1`.",
        "pinned_revision": "99fcfc6867e739aa1cd8ffc49fe39276036681f1",
        "pinned_revision_url": "https://github.com/BelfrySCAD/BOSL2/commit/99fcfc6867e739aa1cd8ffc49fe39276036681f1",
        "pinned_revision_source": "https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564",
    },
    "UB": {
        "version_hint": "Inventory description says `OpenSCAD v.21 and above`; this appears to describe OpenSCAD compatibility, not a PMM-pinned UB revision.",
    },
    "KeyV2": {
        "version_hint": "No library version or PMM-pinned commit is listed in the MakerWorld inventory.",
    },
    "gridfinity-rebuilt-openscad": {
        "version_hint": "No library version or PMM-pinned commit is listed in the MakerWorld inventory.",
    },
    "threads-scad": {
        "version_hint": "No library version or PMM-pinned commit is listed in the MakerWorld inventory.",
    },
    "Getriebe": {
        "version_hint": "No library version or PMM-pinned commit is listed; the inventory source URL points at the upstream `master` branch.",
    },
    "knurledFinishLib_v2": {
        "version_hint": "Library name and description indicate `v2`, but no PMM-pinned commit or release artifact is listed.",
    },
}


def main() -> None:
    payload = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    records = []
    for library in payload.get("Libraries", []):
        note = VERSION_NOTES.get(library["name"], {})
        records.append(
            {
                "name": library["name"],
                "include_method": library["includeMethod"],
                "source_url": library["url"],
                "makerworld_description": library["description"].strip(),
                "version_hint": note.get("version_hint", "No version hint recorded."),
                "pinned_revision": note.get("pinned_revision"),
                "pinned_revision_url": note.get("pinned_revision_url"),
                "pinned_revision_source": note.get("pinned_revision_source"),
                "source_class": "Official app endpoint",
                "source_type": "makerworld_json",
                "evidence_urls": [SOURCE_URL],
            }
        )

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(records, indent=2, sort_keys=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
