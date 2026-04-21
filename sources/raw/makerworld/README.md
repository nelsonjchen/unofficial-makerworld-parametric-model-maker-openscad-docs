# MakerWorld Raw Snapshots

This directory stores raw public PMM artifacts from MakerWorld-controlled endpoints and web assets rather than forum posts.

Examples:
- bundled library inventories
- installed font inventories
- public JS chunks
- build manifests
- ZIP assets discovered from PMM chunks

Each raw snapshot should have a sidecar `.meta.json` file that records:
- `source_type: makerworld_json` or `makerworld_web_asset`
- `origin`
- `captured_at`
- `url`
- `capture_method`
- `verbatim`
- `notes`

Use `python3 scripts/fetch_sources.py` for direct JSON endpoints and `python3 scripts/discover_pmm_web.py` for public web-asset discovery.
