# Sources

This repository stores evidence in two broad classes.

## `sources/raw/makerworld/`
These files are direct public PMM artifacts from MakerWorld-controlled endpoints or web assets rather than forum posts.

Examples:
- bundled OpenSCAD library inventories
- installed font inventories
- public JS chunks
- build manifests
- ZIP assets exposed by the PMM web app

Every fetched artifact should have a sidecar metadata file describing:
- `source_type`
- `origin`
- `captured_at`
- `url`
- `capture_method`
- `verbatim`
- `notes`

## `sources/raw/discourse/`
These files are public Discourse JSON snapshots fetched from Bambu Lab's forum.

They are sourced from public endpoints such as:
- `/t/<id>.json`
- `/search.json?q=...`
- `/c/.../.json`
- `/latest.json`

Every fetched artifact should have a sidecar metadata file describing:
- `source_type`
- `origin`
- `captured_at`
- `url`
- `capture_method`
- `verbatim`
- `notes`

## `sources/raw/manual/`
These files are intentional manual captures, not auto-scraped data.

Examples:
- copied PMM UI text
- copied example snippets from PMM dialogs
- screenshot transcriptions
- hand-recorded observations from MakerWorld PMM

Manual captures must include:
- capture date
- source URL if available
- whether the content is verbatim, paraphrased, or transcribed from a screenshot
- any notes about uncertainty

## Evidence Preference
Docs should prefer:
1. MakerWorld app endpoints.
2. Discourse release posts by Bambu staff.
3. Employee-confirmed details in support or bug threads.
4. Manual UI captures with explicit provenance.
5. Community-derived behavior notes.
6. Explicitly labeled inference.
