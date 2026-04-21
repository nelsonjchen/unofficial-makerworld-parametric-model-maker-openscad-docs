#!/usr/bin/env python3
"""Generate selected Markdown docs from normalized JSON data."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DOCS_DIR = REPO_ROOT / "docs"


def load_json(name: str) -> object:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def write_doc(name: str, lines: list[str]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_feature_reference(features: list[dict]) -> None:
    lines = [
        "# Feature Reference",
        "",
        "This page summarizes PMM-specific OpenSCAD features that are useful to coding agents and model authors.",
        "",
    ]
    for feature in features:
        lines.append(f"## {feature['feature_key']}")
        lines.append("")
        lines.append(f"- Status: `{feature['status']}`")
        lines.append(f"- Introduced in: `{feature['introduced_in']}`")
        lines.append(f"- Scope: `{feature['scope']}`")
        lines.append(f"- Provenance: `{feature['source_class']}`")
        if feature["syntax"]:
            lines.append("- Syntax:")
            for item in feature["syntax"]:
                lines.append(f"  - `{item}`")
        lines.append("- Constraints:")
        for item in feature["constraints"]:
            lines.append(f"  - {item}")
        lines.append(f"- Rewrite guidance: {feature['rewrite_guidance']}")
        lines.append(f"- Agent action: {feature['agent_action']}")
        lines.append("- Evidence:")
        for url in feature["evidence_urls"]:
            lines.append(f"  - {url}")
        lines.append("")
    write_doc("feature-reference.md", lines)


def render_compatibility_rules(rules: list[dict]) -> None:
    lines = [
        "# Compatibility Rules",
        "",
        "Use this page when deciding whether a local OpenSCAD pattern can be ported directly to PMM or needs a rewrite.",
        "",
    ]
    for rule in rules:
        lines.append(f"## {rule['feature_key']}")
        lines.append("")
        lines.append(f"- Status: `{rule['status']}`")
        lines.append(f"- Scope: `{rule['scope']}`")
        lines.append(f"- Provenance: `{rule['source_class']}`")
        if rule["syntax"]:
            lines.append("- Example syntax:")
            for item in rule["syntax"]:
                lines.append(f"  - `{item}`")
        lines.append("- Constraints:")
        for item in rule["constraints"]:
            lines.append(f"  - {item}")
        lines.append(f"- Rewrite guidance: {rule['rewrite_guidance']}")
        lines.append(f"- Agent action: {rule['agent_action']}")
        lines.append("- Evidence:")
        for url in rule["evidence_urls"]:
            lines.append(f"  - {url}")
        lines.append("")
    write_doc("compatibility-rules.md", lines)


def render_discourse_api(source_index: list[dict]) -> None:
    discourse_records = [record for record in source_index if record["source_type"] == "discourse_json"]
    makerworld_records = [record for record in source_index if record["source_type"] == "makerworld_json"]
    lines = [
        "# Discourse API",
        "",
        "Bambu Lab's forum is a Discourse instance and exposes public JSON endpoints that are useful for PMM research and changelog refreshes.",
        "",
        "## Endpoints Used",
        "",
        "- `/t/<id>.json` for topic detail and post streams",
        "- `/t/<slug>/<id>.json` as a slugged topic variant",
        "- `/search.json?q=...` for topic discovery",
        "- `/c/makerworld/makerlab/163.json` for the MakerLab category feed",
        "- `/latest.json` for broad discovery",
        "",
        "## Fetching Strategy",
        "",
        "- Use a browser-like user agent.",
        "- Treat the JSON payloads as evidence snapshots, not as a stable product API contract.",
        "- Save raw payloads and sidecar metadata under `sources/raw/discourse/`.",
        "",
        "## Current Snapshot Inventory",
        "",
        f"- MakerWorld app-endpoint artifacts indexed elsewhere: `{len(makerworld_records)}`",
        f"- Discourse artifacts indexed: `{len(discourse_records)}`",
        "- Manual UI captures are intentionally separate and are not fetched by the script.",
        "",
        "See `scripts/fetch_sources.py` for the concrete fetch implementation.",
    ]
    write_doc("discourse-api.md", lines)


def render_sources_and_provenance(source_index: list[dict]) -> None:
    counter = Counter(record["source_type"] for record in source_index)
    lines = [
        "# Sources And Provenance",
        "",
        "This repository separates evidence class from source type.",
        "",
        "## Source Types",
        "",
        "- `makerworld_json`: raw JSON captured from MakerWorld PMM app endpoints",
        "- `discourse_json`: raw JSON captured from Bambu's public Discourse forum endpoints",
        "- `manual_capture`: intentional notes or copied text from PMM UI surfaces",
        "",
        "## Provenance Labels",
        "",
        "- `Official app endpoint`",
        "- `Official release`",
        "- `Employee-confirmed`",
        "- `Manual UI capture`",
        "- `Community-discovered`",
        "- `Inference`",
        "",
        "## Preference Order",
        "",
        "1. Official app endpoints",
        "2. Official release posts by staff",
        "3. Employee replies in support or bug threads",
        "4. Manual UI captures with clear provenance",
        "5. Community findings",
        "6. Explicitly labeled inference",
        "",
        "## Current Source Inventory",
        "",
        f"- `makerworld_json`: `{counter.get('makerworld_json', 0)}`",
        f"- `discourse_json`: `{counter.get('discourse_json', 0)}`",
        f"- `manual_capture`: `{counter.get('manual_capture', 0)}`",
        "",
        "Manual UI captures should never be auto-scraped in v1. Add them intentionally under `sources/raw/manual/` using the provided template.",
    ]
    write_doc("sources-and-provenance.md", lines)


def main() -> None:
    features = load_json("feature-index.json")
    rules = load_json("compatibility-rules.json")
    source_index = load_json("source-index.json")

    render_feature_reference(features)
    render_compatibility_rules(rules)
    render_discourse_api(source_index)
    render_sources_and_provenance(source_index)


if __name__ == "__main__":
    main()
