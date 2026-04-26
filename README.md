# Bambu MakerWorld OpenSCAD PMM Reference

This repository is an agent-first reference for Bambu Lab MakerWorld's [OpenSCAD](https://openscad.org/)-based [Parametric Model Maker (PMM)](https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564).

**Start here for the actual OpenSCAD authoring surface:** [PMM OpenSCAD API](docs/pmm-openscad-api.md).

**Generated docs site:** [MakerWorld PMM OpenSCAD Reference](https://nelsonjchen.github.io/unofficial-makerworld-parametric-model-maker-openscad-docs/).

**Generated font index:** [PMM Font Index](https://nelsonjchen.github.io/unofficial-makerworld-parametric-model-maker-openscad-docs/font-index/).

The main use case is practical:
- A user points Codex, Claude Code, or another agent at this repo.
- The agent learns PMM-specific OpenSCAD rules, packaging constraints, source-backed quirks, and common failure modes.
- The agent can then adapt an existing `.scad` file or generate a PMM-ready script and upload plan without digging through scattered forum threads.

This repo intentionally focuses on OpenSCAD. Fusion 360-specific guidance is out of scope unless a later PMM update changed the OpenSCAD workflow or backend itself.

## Why This Exists
The practical problem is that PMM documentation is scattered across release posts, support threads, UI examples, and community reverse-engineering instead of living in one obvious reference.

As of April 21, 2026, we could not find a single official Bambu wiki or help-center page that serves as a canonical reference for MakerWorld's Parametric Model Maker, even with searches like [this Google query](https://www.google.com/search?q=site%3Awiki.bambulab.com+%22Parametric+Model+Maker%22+OR+site%3Asupport.bambulab.com+%22Parametric+Model+Maker%22+OR+site%3Amakerworld.com%2Fhelp+%22Parametric+Model+Maker%22).

That pain shows up repeatedly in public discussions:
- [Any Documentation on Parametric Model Maker? post 1](https://forum.bambulab.com/t/any-documentation-on-parametric-model-maker/230605/1)
- [Any Documentation on Parametric Model Maker? post 7](https://forum.bambulab.com/t/any-documentation-on-parametric-model-maker/230605/7)
- [Any Documentation on Parametric Model Maker? post 8](https://forum.bambulab.com/t/any-documentation-on-parametric-model-maker/230605/8)
- [Parametric Model Maker V1.1.0 - Major UI Refresh, post 5](https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564/5)
- [Parametric Model Maker Review and Feedback, post 3](https://forum.bambulab.com/t/parametric-model-maker-review-and-feedback/75758/3)
- [Documentation on parametric model maker](https://www.reddit.com/r/makerworld/comments/1rayxnv/documentation_on_parametric_model_maker/)
- [Reddit comment link shared by the user](https://www.reddit.com/r/makerworld/comments/1rayxnv/comment/o6p0aza/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

This repository exists to turn that scattered knowledge into one agent-friendly OpenSCAD PMM reference with provenance, examples, and a refreshable evidence archive.

## Questions This Repo Should Answer
- How do I make this OpenSCAD script work in MakerWorld PMM?
- Which PMM-specific comments and modules exist?
- What file naming conventions are mandatory for uploads?
- What features are employee-confirmed versus inferred?
- Which PMM web assets are directly fetchable without auth, and which require browser context or login?
- What limitations should I rewrite around?
- What backend or library version is PMM using?
- How should I package a file-upload or multi-plate model for MakerWorld?

## Fast Start
If you are a coding agent, start here:
1. `AGENTS.md`
2. `docs/pmm-openscad-api.md`
3. `docs/agent-workflow.md`
4. `docs/feature-reference.md`
5. `docs/compatibility-rules.md`
6. `docs/web-discovery.md`
7. `docs/gotchas.md`
8. `docs/changelog.md`
9. `patterns/pmm-ready-template.scad`

If you want to refresh the evidence-backed data:

```bash
python3 scripts/fetch_sources.py
python3 scripts/discover_pmm_web.py
python3 scripts/fetch_pmm_syntax_demo.py
python3 scripts/build_index.py
python3 scripts/build_font_index.py
python3 scripts/build_changelog.py
python3 scripts/build_patterns_index.py
python3 scripts/build_docs.py
```

Or run the one-shot helper:

```bash
python3 scripts/build_all.py
```

To preview the GitHub Pages site locally:

```bash
pip install -r requirements-docs.txt
python3 scripts/build_all.py
mkdocs serve
```

The font index is generated from MakerWorld's public PMM font inventory snapshots. Browser previews are best-effort and provenance-labeled: clean webfont sources may render live previews, while font families with custom, conflicting, or restricted redistribution terms are documented without bundling questionable font files.

## Repository Layout
- `AGENTS.md`: retrieval-first instructions for coding agents.
- `docs/pmm-openscad-api.md`: author-facing PMM OpenSCAD API surface.
- `docs/`: curated reference docs and generated summaries.
- `patterns/`: PMM-oriented OpenSCAD examples and templates.
- `patterns/pmm-syntax-demo.scad`: PMM's extracted default editor source, refreshed from public web chunks.
- `checklists/`: migration, packaging, and validation checklists.
- `data/`: machine-readable indexes for agent retrieval.
- `data/bundled-library-index.json`: normalized bundled-library include methods, source links, and version clues.
- `data/font-index.json`: normalized PMM font inventory records.
- `data/font-preview-index.json`: font preview and provenance metadata for the generated font index.
- `data/pmm-web-discovery.json`: current public-web discovery summary for PMM assets.
- `sources/raw/discourse/`: raw public Discourse JSON snapshots from Bambu's forum.
- `sources/raw/makerworld/`: raw PMM app endpoints and public web-asset captures.
- `sources/raw/manual/`: intentional manual captures from PMM UI or related surfaces.
- `scripts/`: refresh and build tooling.

## Provenance Model
The docs distinguish between:
- `Official app endpoint`
- `Official release`
- `Employee-confirmed`
- `Manual UI capture`
- `Community-discovered`
- `Inference`

The preferred evidence order is:
1. Official app endpoints from MakerWorld.
2. Official release posts by Bambu staff.
3. Employee replies in support or bug threads.
4. Intentional manual captures from the PMM UI.
5. Community findings.
6. Explicitly labeled inference.

Raw MakerWorld endpoint snapshots and Discourse snapshots are stored with sidecar metadata. Manual UI captures are not auto-scraped in v1; they should be added intentionally and labeled with provenance.
