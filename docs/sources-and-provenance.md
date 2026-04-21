# Sources And Provenance

This repository separates evidence class from source type.

## Source Types

- `discourse_json`: raw JSON captured from Bambu's public Discourse forum endpoints
- `manual_capture`: intentional notes or copied text from PMM UI surfaces

## Provenance Labels

- `Official release`
- `Employee-confirmed`
- `Manual UI capture`
- `Community-discovered`
- `Inference`

## Preference Order

1. Official release posts by staff
2. Employee replies in support or bug threads
3. Manual UI captures with clear provenance
4. Community findings
5. Explicitly labeled inference

## Current Source Inventory

- `discourse_json`: `24`
- `manual_capture`: `0`

Manual UI captures should never be auto-scraped in v1. Add them intentionally under `sources/raw/manual/` using the provided template.
