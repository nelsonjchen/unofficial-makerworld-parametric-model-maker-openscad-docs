# Agent Workflow

This is the operational path for turning a normal OpenSCAD model into a MakerWorld PMM-friendly model.

## 1. Inspect The Existing Script
- Identify the user-facing parameters.
- Identify any `include` or `use` statements.
- Identify any `import()` calls for SVG, STL, or PNG-backed workflows.
- Identify color usage, font usage, and whether multiple printable parts exist.
- Identify whether the current script already separates assembly and output geometry.

## 2. Compare Against PMM Constraints
Check the script against:
- `docs/compatibility-rules.md`
- `docs/gotchas.md`
- `data/compatibility-rules.json`

At this stage, answer:
- Does the script depend on local includes that PMM is unlikely to have?
- Is the script using a bundled PMM library such as BOSL2, or is it using arbitrary local project includes?
- Does it assume arbitrary co-uploaded asset names?
- Does it need PMM-specific comments like `// color` or `// font`?
- Does it need multi-plate support or would that complicate the release?

## 3. Rewrite Unsupported Or Fragile Constructs First
Before adding PMM sugar:
- Collapse fragile local includes into one PMM-safe file if needed.
- Do not strip out bundled PMM libraries such as BOSL2 just because local includes are risky.
- Replace arbitrary asset references with supported default filenames when using file upload features.
- Remove non-portable assumptions about local filesystem layout.
- Prefer simple helper modules over PMM magic until the model is stable.

## 4. Add PMM-Facing Parameters
Only after the script is structurally safe:
- Add basic scalar or string parameters that map cleanly to user intent.
- Use hex string colors with `// color` when you want PMM to expose a color picker.
- Use `// font` when you want PMM to expose a font picker.

See:
- `patterns/basic-parameterized-model.scad`
- `patterns/color-parameter.scad`
- `patterns/font-parameter.scad`

## 5. Add PMM-Specific Modules If Needed
Use PMM-specific modules only when the model benefits from them:
- `mw_plate_N()` for multi-plate 3MF output.
- `mw_assembly_view()` for previewing a complete assembly.

Use these carefully:
- Multi-plate output is powerful, but it changes how users download and print.
- Assembly view improves comprehension, but it should not be confused with printable output.

See:
- `patterns/multi-plate-3mf.scad`
- `patterns/assembly-view.scad`

## 6. Build A Packaging Plan
Before handing work back to the user, produce:
- The PMM-ready `.scad` file.
- Any required default asset naming notes such as `default.svg` or `default.stl`.
- A release recommendation: single-plate, multi-plate, or split scripts.
- User-facing notes about tradeoffs.

Use:
- `docs/publishing-workflow.md`
- `checklists/convert-existing-script.md`
- `checklists/pre-upload-validation.md`
- `checklists/multi-plate-release.md`

## 7. Cite Provenance
When explaining why a rewrite is needed:
- Prefer `Official release` or `Employee-confirmed` evidence.
- Link to the relevant docs in this repo first.
- Fall back to raw source material only when a user needs provenance or newer details.
