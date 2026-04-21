# Agent Guide

This repository is designed to help an implementation agent turn ordinary OpenSCAD into MakerWorld Parametric Model Maker-compatible OpenSCAD.

## Read Order
When you need to modify or generate a PMM-ready script, read in this order:
1. `docs/agent-workflow.md`
2. `docs/feature-reference.md`
3. `docs/compatibility-rules.md`
4. `docs/gotchas.md`
5. `docs/changelog.md`
6. `patterns/pmm-ready-template.scad`

Use `data/feature-index.json`, `data/compatibility-rules.json`, and `data/changelog.json` for quick retrieval once you know the repo shape.

## Questions This Repo Should Answer
- How do I make this OpenSCAD script work in MakerWorld PMM?
- Which PMM-specific comments and modules exist?
- What file naming conventions are mandatory for uploads?
- What features are employee-confirmed versus inferred?
- Which PMM web assets are directly fetchable without auth, and which require browser context or login?
- What limitations should I rewrite around?
- What backend or library version is PMM using?
- How should I package a file-upload or multi-plate model for MakerWorld?

## Default Agent Workflow
1. Inspect the user's OpenSCAD and identify parameters, imports, includes, colors, fonts, and export shape.
2. Compare that script against `docs/compatibility-rules.md`.
3. Rewrite unsupported patterns before adding PMM-specific sugar.
4. Add PMM UI-facing parameters such as `// color` or `// font` only where appropriate.
5. Add PMM-specific modules such as `mw_plate_N()` or `mw_assembly_view()` only when the model truly benefits from them.
6. Produce a packaging and upload plan using the checklists in `checklists/`.

## Task-Specific Guidance
### Convert a normal OpenSCAD script into PMM-compatible form
- Start with `checklists/convert-existing-script.md`.
- Remove or replace fragile local includes.
- Do not assume this means PMM cannot use bundled libraries such as BOSL2. The main risk is arbitrary local project files, not every library include.
- Replace arbitrary uploaded asset names with PMM-supported defaults when using file upload features.
- Add PMM-specific comments and modules only after the core geometry works.

### Add PMM UI parameters
- Use `patterns/basic-parameterized-model.scad` as the baseline.
- For colors, see `patterns/color-parameter.scad`.
- For fonts, see `patterns/font-parameter.scad`.
- Keep parameters simple and user-facing.

### Add file-upload support
- Use `patterns/file-upload-svg.scad` or `patterns/file-upload-stl.scad`.
- Follow the default filename restrictions from `docs/feature-reference.md`.
- Document the upload expectation in the packaging plan.

### Add multi-plate support
- Use `patterns/multi-plate-3mf.scad` and `patterns/assembly-view.scad`.
- Read `checklists/multi-plate-release.md` before choosing this path.
- Remember that multi-plate 3MF trades off against STL download convenience for that script.

### Detect and rewrite unsupported constructs
- Use `docs/compatibility-rules.md` and `docs/gotchas.md`.
- Treat local include trees and arbitrary co-uploaded asset names as suspicious.
- Distinguish bundled PMM libraries such as BOSL2 from arbitrary local include trees before rewriting working code.
- Prefer shared helper modules over recursive or special-case PMM module calls.

### Produce a MakerWorld upload package plan
- Use `docs/publishing-workflow.md`.
- Use `checklists/pre-upload-validation.md`.
- Include user-facing notes about tradeoffs such as file upload expectations, multi-plate behavior, or oversize risk.

## Provenance Rules
- Prefer `Official app endpoint` evidence when a question is directly answered by MakerWorld's own JSON payloads, such as installed libraries or font inventories.
- Use `docs/web-discovery.md` and `data/pmm-web-discovery.json` when you need current PMM chunk URLs, public asset discovery notes, or auth-vs-browser-context guidance.
- Prefer `Official release` and `Employee-confirmed` evidence.
- Use `Manual UI capture` only when the forum does not cover a detail and the capture is clearly labeled.
- Treat `Community-discovered` as useful but not authoritative.
- If you infer behavior, label it as `Inference`.

## Stable Interfaces
Agents should rely on these public outputs:
- `docs/feature-reference.md`
- `docs/compatibility-rules.md`
- `docs/agent-workflow.md`
- `docs/publishing-workflow.md`
- `docs/web-discovery.md`
- `docs/gotchas.md`
- `docs/changelog.md`
- `patterns/pmm-ready-template.scad`
- `data/feature-index.json`
- `data/compatibility-rules.json`
- `data/changelog.json`
- `data/pmm-web-discovery.json`
- `data/source-index.json`
