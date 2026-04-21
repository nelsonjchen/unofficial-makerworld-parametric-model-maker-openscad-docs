# MakerWorld Raw Snapshots

This directory stores raw JSON snapshots from MakerWorld-controlled PMM endpoints rather than forum posts.

Examples:
- bundled library inventories
- installed font inventories

Each raw snapshot should have a sidecar `.meta.json` file that records:
- `source_type: makerworld_json`
- `origin`
- `captured_at`
- `url`
- `capture_method`
- `verbatim`
- `notes`

Use `python3 scripts/fetch_sources.py` to refresh these files.
