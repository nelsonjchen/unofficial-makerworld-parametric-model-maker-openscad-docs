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


def load_json_optional(name: str) -> object | None:
    path = DATA_DIR / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


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
    makerworld_asset_records = [record for record in source_index if record["source_type"] == "makerworld_web_asset"]
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
        f"- MakerWorld public web assets indexed elsewhere: `{len(makerworld_asset_records)}`",
        f"- Discourse artifacts indexed: `{len(discourse_records)}`",
        "- Manual UI captures are intentionally separate and are not fetched by the script.",
        "",
        "See `scripts/fetch_sources.py` for forum and direct JSON fetches, and `docs/web-discovery.md` for public PMM web-asset discovery.",
    ]
    write_doc("discourse-api.md", lines)


def render_web_discovery(discovery: dict | None) -> None:
    if discovery is None:
        lines = [
            "# Public Web Discovery",
            "",
            "Run `python3 scripts/discover_pmm_web.py` to generate the current PMM public-web discovery summary.",
        ]
        write_doc("web-discovery.md", lines)
        return

    page_fetch = discovery.get("page_fetch", {})
    public_fetches = discovery.get("public_fetches", [])
    account_candidates = discovery.get("account_api_candidates", [])
    public_urls = [record["url"] for record in public_fetches if record.get("ok")]
    lines = [
        "# Public Web Discovery",
        "",
        "This page summarizes how much of MakerWorld PMM can be rediscovered from public web assets without a logged-in browser session.",
        "",
        "## Current Discovery Result",
        "",
        f"- Captured at: `{discovery.get('captured_at')}`",
        f"- PMM page URL: `{discovery.get('page_url')}`",
        f"- Headless page-fetch status: `{page_fetch.get('status')}`",
        f"- Headless page HTTP status: `{page_fetch.get('http_status')}`",
        f"- Build manifest URL: `{discovery.get('build_manifest_url') or 'not discovered live in this run'}`",
        f"- Current chunk URL count: `{len(discovery.get('current_chunk_urls', []))}`",
        f"- Public fetchable artifact count: `{len(public_urls)}`",
        f"- Account or session-bound API candidate count: `{len(account_candidates)}`",
        "",
        "## What Works Without Auth",
        "",
        "These assets were reachable directly in this discovery model:",
    ]
    for url in public_urls:
        lines.append(f"- {url}")
    if not public_urls:
        lines.append("- No public assets were fetched in this run.")

    lines.extend(
        [
            "",
            "## What Needs Browser Context Or Login",
            "",
            "- The top-level PMM HTML may be blocked by a Cloudflare challenge for headless clients even when lower-level static chunks and content-generator assets are public.",
            "- Account-focused `api/v1/...` endpoints should be treated as browser- or login-bound unless separately confirmed.",
        ]
    )
    for record in account_candidates[:20]:
        lines.append(f"- `{record['auth_hint']}`: {record['url']}")

    lines.extend(
        [
            "",
            "## Refresh Guidance",
            "",
            "1. Run `python3 scripts/discover_pmm_web.py` first.",
            "2. If the PMM page itself is challenge-protected, seed discovery with a cleaned browser network log using `--seed-file` or known public chunk URLs using `--seed-url`.",
            "3. Run `python3 scripts/fetch_pmm_syntax_demo.py` to extract the current PMM default editor source from the generator lazy chunk.",
            "4. Re-run `python3 scripts/build_index.py` and `python3 scripts/build_docs.py` after discovery if you changed the raw artifact set.",
            "",
            "## Current Notes",
            "",
        ]
    )
    for note in discovery.get("notes", []):
        lines.append(f"- {note}")

    write_doc("web-discovery.md", lines)


def render_syntax_demo(status: dict | None) -> None:
    if status is None:
        lines = [
            "# PMM Syntax Demo",
            "",
            "Run `python3 scripts/fetch_pmm_syntax_demo.py` to extract PMM's current default OpenSCAD source from public MakerWorld web chunks.",
        ]
        write_doc("pmm-syntax-demo.md", lines)
        return

    source_path = REPO_ROOT / status.get("raw_path", "")
    source = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    lines = [
        "# PMM Syntax Demo",
        "",
        "This is the current default OpenSCAD source that MakerWorld PMM loads into the editor for the generator flow.",
        "",
        f"- Extraction status: `{status.get('status')}`",
        f"- Captured at: `{status.get('captured_at')}`",
        f"- Source chunk: {status.get('source_url')}",
        f"- Raw source: [`{status.get('raw_path')}`](../{status.get('raw_path')})",
        f"- Pattern copy: [`{status.get('pattern_path')}`](../{status.get('pattern_path')})",
        f"- Lines: `{status.get('line_count')}`",
        f"- SHA-256: `{status.get('content_sha256')}`",
        "",
        "Refresh it with `python3 scripts/fetch_pmm_syntax_demo.py`. If a headless fetch misses the current chunk, pass a cleaned browser network export with `--seed-file`.",
        "",
        "```scad",
        source.rstrip(),
        "```",
    ]
    write_doc("pmm-syntax-demo.md", lines)


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
        "- `makerworld_web_asset`: raw non-JSON public PMM web artifacts such as JS chunks, manifests, or ZIP assets",
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
        f"- `makerworld_web_asset`: `{counter.get('makerworld_web_asset', 0)}`",
        f"- `discourse_json`: `{counter.get('discourse_json', 0)}`",
        f"- `manual_capture`: `{counter.get('manual_capture', 0)}`",
        "",
        "Manual UI captures should never be auto-scraped in v1. Add them intentionally under `sources/raw/manual/` using the provided template.",
        "",
        "External project workflows, such as community repositories that publish PMM-ready OpenSCAD, may be cited inline as examples. They are lower-authority evidence than official app endpoints, official releases, employee-confirmed behavior, or labeled manual captures, and should not be used as standalone proof of PMM feature support.",
    ]
    write_doc("sources-and-provenance.md", lines)


def main() -> None:
    features = load_json("feature-index.json")
    rules = load_json("compatibility-rules.json")
    source_index = load_json("source-index.json")
    web_discovery = load_json_optional("pmm-web-discovery.json")
    syntax_demo = load_json_optional("pmm-syntax-demo.json")

    render_feature_reference(features)
    render_compatibility_rules(rules)
    render_discourse_api(source_index)
    render_web_discovery(web_discovery)
    render_syntax_demo(syntax_demo)
    render_sources_and_provenance(source_index)


if __name__ == "__main__":
    main()
