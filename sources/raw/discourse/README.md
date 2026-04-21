# Discourse Raw Snapshots

This directory stores raw JSON snapshots from Bambu Lab's public Discourse forum endpoints.

Each raw snapshot should have a sidecar `.meta.json` file that records:
- `source_type: discourse_json`
- `origin`
- `captured_at`
- `url`
- `capture_method`
- `verbatim`
- `notes`

Use `python3 scripts/fetch_sources.py` to refresh these files.
