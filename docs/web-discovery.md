# Public Web Discovery

This page summarizes how much of MakerWorld PMM can be rediscovered from public web assets without a logged-in browser session.

## Current Discovery Result

- Captured at: `2026-04-21T17:36:16Z`
- PMM page URL: `https://makerworld.com/en/makerlab/parametricModelMaker?pageType=generator`
- Headless page-fetch status: `ok`
- Headless page HTTP status: `200`
- Build manifest URL: `https://makerworld.com/_next/static/70KJ0RikzXL6bbz2JJlju/_buildManifest.js`
- Current chunk URL count: `2`
- Public fetchable artifact count: `8`
- Account or session-bound API candidate count: `0`

## What Works Without Auth

These assets were reachable directly in this discovery model:
- https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-0.8.0.json
- https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-show-0.0.1.json
- https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/language2family-0.0.1.zip
- https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json
- https://makerworld.com/_next/static/70KJ0RikzXL6bbz2JJlju/_buildManifest.js
- https://makerworld.com/_next/static/70KJ0RikzXL6bbz2JJlju/_ssgManifest.js
- https://makerworld.com/_next/static/chunks/openscad-84d6e74b207bcd6c.js
- https://makerworld.com/_next/static/chunks/pages/makerlab/parametricModelMaker-b38162896fad14ff.js

## What Needs Browser Context Or Login

- The top-level PMM HTML may be blocked by a Cloudflare challenge for headless clients even when lower-level static chunks and content-generator assets are public.
- Account-focused `api/v1/...` endpoints should be treated as browser- or login-bound unless separately confirmed.

## Refresh Guidance

1. Run `python3 scripts/discover_pmm_web.py` first.
2. If the PMM page itself is challenge-protected, seed discovery with a cleaned browser network log using `--seed-file` or known public chunk URLs using `--seed-url`.
3. Re-run `python3 scripts/build_index.py` and `python3 scripts/build_docs.py` after discovery if you changed the raw artifact set.

## Current Notes

- The top-level PMM page can be Cloudflare challenge-protected for headless or non-browser clients even when lower-level PMM assets remain directly fetchable.
- Public `_next/static` chunks and `makerworld.bblmw.com/makerworld/makerlab/content-generator/...` assets are the main unauthenticated discovery surface once a current chunk URL or build manifest URL is known.
