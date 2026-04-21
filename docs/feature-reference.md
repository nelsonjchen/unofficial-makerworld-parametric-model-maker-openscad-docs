# Feature Reference

This page summarizes PMM-specific OpenSCAD features that are useful to coding agents and model authors.

## model_page_integration

- Status: `supported`
- Introduced in: `2024-05-10`
- Scope: `ui`
- Provenance: `Official release`
- Constraints:
  - PMM is integrated into MakerWorld model pages rather than being only a separate tool entrypoint.
- Rewrite guidance: Assume model-page customization exists; do not design around the older detached workflow.
- Agent action: Package the script for a model-page PMM flow rather than an entirely off-page customizer.
- Evidence:
  - https://forum.bambulab.com/t/makerworld-update-05-10/74832

## file_upload_default_assets

- Status: `supported`
- Introduced in: `v0.8.0`
- Scope: `uploads`
- Provenance: `Official release`
- Syntax:
  - `yourFileName = "default.png";`
  - `yourFileName = "default.svg";`
  - `yourFileName = "default.stl";`
- Constraints:
  - The official release documents built-in default filenames rather than arbitrary file naming.
  - Custom default files are not described as supported in the release note.
- Rewrite guidance: Rewrite arbitrary uploaded asset names to PMM-supported defaults when building a PMM-safe script.
- Agent action: Use default filenames for PMM upload parameters and explain the upload expectation to users.
- Evidence:
  - https://forum.bambulab.com/t/paramatric-model-maker-v0-8-0-support-uploading-files/91853

## parameterized_color_ui

- Status: `supported`
- Introduced in: `v0.9.0`
- Scope: `colors`
- Provenance: `Official release`
- Syntax:
  - `accent = "#FF0000"; // color`
- Constraints:
  - Parameterized colors are documented using hex string values with the `// color` comment.
- Rewrite guidance: Convert user-facing color parameters to hex strings and add `// color` only where PMM UI exposure is intended.
- Agent action: Prefer hex string parameters over non-parameterized literal color arrays for PMM UI controls.
- Evidence:
  - https://forum.bambulab.com/t/paramatric-model-maker-v0-9-0-support-multi-color-modeling/100160

## font_picker_ui

- Status: `supported`
- Introduced in: `v0.10.0`
- Scope: `fonts`
- Provenance: `Official release`
- Syntax:
  - `font_name = "Roboto"; // font`
- Constraints:
  - The `// font` comment is required to enable the PMM font picker UI.
- Rewrite guidance: If a model exposes fonts to PMM users, add a dedicated font-name parameter with the required comment marker.
- Agent action: Do not assume a font parameter will become a PMM UI control unless `// font` is present.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## multi_plate_3mf

- Status: `supported`
- Introduced in: `v0.10.0`
- Scope: `export`
- Provenance: `Official release`
- Syntax:
  - `module mw_plate_1() { ... }`
  - `module mw_plate_2() { ... }`
- Constraints:
  - Each printable plate uses an `mw_plate_N()` module.
  - The official release warns that multi-plate scripts do not offer STL download from that script.
- Rewrite guidance: Only choose multi-plate when the user actually benefits from a 3MF-first release strategy.
- Agent action: Use PMM multi-plate modules for multi-part outputs and explain the STL tradeoff.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## assembly_view

- Status: `supported`
- Introduced in: `v0.10.0`
- Scope: `preview`
- Provenance: `Official release`
- Syntax:
  - `module mw_assembly_view() { ... }`
- Constraints:
  - The assembly view is documented as a preview aid and is not included in the exported 3MF.
- Rewrite guidance: Use assembly view to improve comprehension for multi-part models without confusing it with printable geometry.
- Agent action: Add `mw_assembly_view()` when users need a full-preview assembly, not as the only output definition.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## profile_configuration

- Status: `supported`
- Introduced in: `v0.10.0`
- Scope: `profiles`
- Provenance: `Official release`
- Constraints:
  - Only selected profile settings are documented as configurable and the upload action must persist the changes.
- Rewrite guidance: Treat profile configuration as a PMM-side release concern rather than a pure OpenSCAD concern.
- Agent action: Mention profile settings when layout or auto-arrange behavior matters.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## customizer_compatibility

- Status: `partial`
- Introduced in: `pre-v0.9`
- Scope: `compatibility`
- Provenance: `Employee-confirmed`
- Constraints:
  - An employee said PMM mainly follows the OpenSCAD Customizer manual.
  - Thingiverse-like preview comments were explicitly said to be unused by PMM itself.
- Rewrite guidance: Model PMM parameter behavior after OpenSCAD Customizer first, and treat extra comment conventions as non-authoritative unless confirmed.
- Agent action: Do not depend on `// preview[...]` or undocumented comment syntax as PMM functionality.
- Evidence:
  - https://forum.bambulab.com/t/parametic-model-maker-colors-documentation/77524

## bundled_bosl2_library

- Status: `supported`
- Introduced in: `pre-v1.1.0`
- Scope: `libraries`
- Provenance: `Official release`
- Syntax:
  - `include <BOSL2/std.scad>;`
- Constraints:
  - PMM distinguishes between bundled platform libraries and arbitrary local include trees.
  - The v1.1.0 PMM release explicitly documented a BOSL2 backend revision, which strongly indicates BOSL2 support in PMM.
- Rewrite guidance: Do not strip or inline BOSL2 solely because local include trees are risky. First distinguish bundled PMM libraries from local project files.
- Agent action: It is reasonable to keep BOSL2 includes when targeting PMM, while still checking for version-specific APIs and performance costs.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564
  - https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## backend_manifold_enabled

- Status: `supported`
- Introduced in: `2025-03-13`
- Scope: `backend`
- Provenance: `Employee-confirmed`
- Constraints:
  - An employee explicitly stated that the PMM backend used commit `b550957ddac62e59428d08efa62e2f44c15a0b95` and manifold was enabled.
- Rewrite guidance: If local and PMM behavior differ, account for a specific PMM backend revision rather than assuming the latest local OpenSCAD release.
- Agent action: Document backend-version assumptions when diagnosing geometry or export discrepancies.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## backend_refresh_v1_1_0

- Status: `supported`
- Introduced in: `v1.1.0`
- Scope: `backend`
- Provenance: `Official release`
- Constraints:
  - The OpenSCAD-backed PMM workflow moved the code editor behind a Code button.
  - The release documented an OpenSCAD backend based on commit `c8fbef05ba900e46892e9a44ea05f7d88e576e13` and BOSL2 commit `99fcfc6867e739aa1cd8ffc49fe39276036681f1`.
- Rewrite guidance: Use these documented revisions when explaining environment differences or library behavior.
- Agent action: Account for the documented backend and BOSL2 revisions when troubleshooting reproducibility.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564
