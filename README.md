# Bambu MakerWorld OpenSCAD PMM Reference

This repository is an agent-first reference for Bambu Lab MakerWorld's [OpenSCAD](https://openscad.org/)-based [Parametric Model Maker (PMM)](https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564).

The main use case is practical:
- A user points Codex, Claude Code, or another agent at this repo.
- The agent learns PMM-specific OpenSCAD rules, packaging constraints, source-backed quirks, and common failure modes.
- The agent can then adapt an existing `.scad` file or generate a PMM-ready script and upload plan without digging through scattered forum threads.

This repo intentionally focuses on OpenSCAD. Fusion 360-specific guidance is out of scope unless a later PMM update changed the OpenSCAD workflow or backend itself.

## Why This Exists
The practical problem is that PMM documentation is scattered across release posts, support threads, UI examples, and community reverse-engineering instead of living in one obvious reference.

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
- What limitations should I rewrite around?
- What backend or library version is PMM using?
- How should I package a file-upload or multi-plate model for MakerWorld?

## Fast Start
If you are a coding agent, start here:
1. `AGENTS.md`
2. `docs/agent-workflow.md`
3. `docs/feature-reference.md`
4. `docs/compatibility-rules.md`
5. `docs/gotchas.md`
6. `docs/changelog.md`
7. `patterns/pmm-ready-template.scad`

If you want to refresh the evidence-backed data:

```bash
python3 scripts/fetch_sources.py
python3 scripts/build_index.py
python3 scripts/build_changelog.py
python3 scripts/build_patterns_index.py
python3 scripts/build_docs.py
```

Or run the one-shot helper:

```bash
python3 scripts/build_all.py
```

## Repository Layout
- `AGENTS.md`: retrieval-first instructions for coding agents.
- `docs/`: curated reference docs and generated summaries.
- `patterns/`: PMM-oriented OpenSCAD examples and templates.
- `checklists/`: migration, packaging, and validation checklists.
- `data/`: machine-readable indexes for agent retrieval.
- `sources/raw/discourse/`: raw public Discourse JSON snapshots from Bambu's forum.
- `sources/raw/manual/`: intentional manual captures from PMM UI or related surfaces.
- `scripts/`: refresh and build tooling.

## Provenance Model
The docs distinguish between:
- `Official release`
- `Employee-confirmed`
- `Manual UI capture`
- `Community-discovered`
- `Inference`

The preferred evidence order is:
1. Official release posts by Bambu staff.
2. Employee replies in support or bug threads.
3. Intentional manual captures from the PMM UI.
4. Community findings.
5. Explicitly labeled inference.

Raw Discourse snapshots are stored with sidecar metadata. Manual UI captures are not auto-scraped in v1; they should be added intentionally and labeled with provenance.
