# Discourse API

Bambu Lab's forum is a Discourse instance and exposes public JSON endpoints that are useful for PMM research and changelog refreshes.

## Endpoints Used

- `/t/<id>.json` for topic detail and post streams
- `/t/<slug>/<id>.json` as a slugged topic variant
- `/search.json?q=...` for topic discovery
- `/c/makerworld/makerlab/163.json` for the MakerLab category feed
- `/latest.json` for broad discovery

## Fetching Strategy

- Use a browser-like user agent.
- Treat the JSON payloads as evidence snapshots, not as a stable product API contract.
- Save raw payloads and sidecar metadata under `sources/raw/discourse/`.

## Current Snapshot Inventory

- Discourse artifacts indexed: `24`
- Manual UI captures are intentionally separate and are not fetched by the script.

See `scripts/fetch_sources.py` for the concrete fetch implementation.
