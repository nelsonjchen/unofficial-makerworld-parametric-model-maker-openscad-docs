# Sources And Provenance

This repository separates evidence class from source type.

## Source Types

- `makerworld_json`: raw JSON captured from MakerWorld PMM app endpoints
- `makerworld_web_asset`: raw non-JSON public PMM web artifacts such as JS chunks, manifests, or ZIP assets
- `discourse_json`: raw JSON captured from Bambu's public Discourse forum endpoints
- `manual_capture`: intentional notes or copied text from PMM UI surfaces

## Provenance Labels

- `Official app endpoint`
- `Official release`
- `Employee-confirmed`
- `Manual UI capture`
- `Community-discovered`
- `Inference`

## Preference Order

1. Official app endpoints
2. Official release posts by staff
3. Employee replies in support or bug threads
4. Manual UI captures with clear provenance
5. Community findings
6. Explicitly labeled inference

## Current Source Inventory

- `makerworld_json`: `5`
- `makerworld_web_asset`: `12`
- `discourse_json`: `24`
- `manual_capture`: `0`

Manual UI captures should never be auto-scraped in v1. Add them intentionally under `sources/raw/manual/` using the provided template.
