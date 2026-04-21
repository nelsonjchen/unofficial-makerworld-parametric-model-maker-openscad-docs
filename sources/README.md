# Sources

This repository stores evidence in two broad classes.

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
1. Discourse release posts by Bambu staff.
2. Employee-confirmed details in support or bug threads.
3. Manual UI captures with explicit provenance.
4. Community-derived behavior notes.
5. Explicitly labeled inference.
