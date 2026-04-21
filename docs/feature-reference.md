# Feature Reference

This page summarizes PMM-specific OpenSCAD features that are useful to coding agents and model authors.

## bundled_library_inventory_endpoint

- Status: `supported`
- Introduced in: `libraries-0.8.0 endpoint`
- Scope: `libraries`
- Provenance: `Official app endpoint`
- Syntax:
  - `include <BOSL2/*.scad>;`
  - `include <threads-scad/threads.scad>;`
- Constraints:
  - MakerWorld exposes a direct JSON inventory of bundled OpenSCAD libraries.
  - This inventory is stronger evidence for bundled-library support than forum inference alone.
- Rewrite guidance: When judging library support, check the MakerWorld library inventory before flattening working bundled includes.
- Agent action: Use the bundled library inventory as the primary source for whether PMM ships a given library.
- Evidence:
  - https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json

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
- Provenance: `Official app endpoint`
- Syntax:
  - `include <BOSL2/std.scad>;`
- Constraints:
  - PMM distinguishes between bundled platform libraries and arbitrary local include trees.
  - MakerWorld's library inventory explicitly lists BOSL2 as a bundled library.
  - The v1.1.0 PMM release also documented a BOSL2 backend revision.
- Rewrite guidance: Do not strip or inline BOSL2 solely because local include trees are risky. First distinguish bundled PMM libraries from local project files.
- Agent action: It is reasonable to keep BOSL2 includes when targeting PMM, while still checking for version-specific APIs and performance costs.
- Evidence:
  - https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json
  - https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564
  - https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## installed_fonts_inventory_endpoint

- Status: `supported`
- Introduced in: `fonts-0.8.0 endpoint`
- Scope: `fonts`
- Provenance: `Official app endpoint`
- Syntax:
  - `"Roboto"`
  - `"Roboto:style=Bold"`
  - `"Noto Sans JP"`
- Constraints:
  - MakerWorld exposes a direct JSON inventory of installed font names.
  - This inventory is the best available source for exact font availability.
- Rewrite guidance: When a model depends on fonts, validate against the endpoint-backed font inventory rather than guessing from UI screenshots or forum anecdotes.
- Agent action: Use the MakerWorld font inventory as the primary source for exact PMM font availability and names.
- Evidence:
  - https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-0.8.0.json

## font_catalog_endpoint

- Status: `supported`
- Introduced in: `fonts-show-0.0.1 asset`
- Scope: `fonts`
- Provenance: `Official app endpoint`
- Syntax:
  - `"AR One Sans"`
  - `"Abyssinica SIL"`
  - `"Noto Sans Arabic"`
- Constraints:
  - MakerWorld exposes a broader PMM font catalog endpoint that returns a `fontNames` list.
  - This catalog is much larger than the smaller installed-font inventory and is useful for UI or multilingual discovery work.
- Rewrite guidance: Use the broad catalog for font research, then validate must-have fonts against the installed runtime inventory before promising deterministic output.
- Agent action: Check `fonts-show-0.0.1.json` when exploring PMM font availability, but keep `fonts-0.8.0.json` as the stricter runtime compatibility check.
- Evidence:
  - https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-show-0.0.1.json

## language_to_font_family_map_asset

- Status: `supported`
- Introduced in: `language2family-0.0.1 asset`
- Scope: `fonts`
- Provenance: `Official app endpoint`
- Syntax:
  - `language2family-0.0.1.zip`
  - `language_support_family_2.json`
- Constraints:
  - MakerWorld publishes a ZIP asset containing `language_support_family_2.json`.
  - The JSON maps language-script identifiers to large font-family lists and is useful for multilingual font fallback research.
- Rewrite guidance: When a PMM model needs broad language coverage, use the language-to-family map as a discovery aid before narrowing choices to installed or tested fonts.
- Agent action: Use the language-support asset when selecting fallback families for multilingual text parameters.
- Evidence:
  - https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/language2family-0.0.1.zip

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
