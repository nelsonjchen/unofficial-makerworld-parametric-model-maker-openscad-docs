# Compatibility Rules

Use this page when deciding whether a local OpenSCAD pattern can be ported directly to PMM or needs a rewrite.

## avoid_arbitrary_local_includes

- Status: `caution`
- Scope: `includes`
- Provenance: `Employee-confirmed`
- Example syntax:
  - `include <local_file.scad>;`
- Constraints:
  - Local include trees are not a safe PMM default unless the library is known to exist in PMM.
- Rewrite guidance: Flatten local dependencies or inline the minimum needed helpers into a PMM-safe file.
- Agent action: Treat local include graphs as migration work, not drop-in PMM behavior.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## distinguish_bundled_bosl2_from_local_includes

- Status: `supported`
- Scope: `libraries`
- Provenance: `Official release`
- Example syntax:
  - `include <BOSL2/std.scad>;`
- Constraints:
  - Bundled PMM libraries such as BOSL2 are a different case from arbitrary local project includes.
  - Bambu documented a specific BOSL2 revision in the v1.1.0 PMM release.
- Rewrite guidance: Keep BOSL2 when it is actually helping the model; only flatten or remove dependencies that are not part of PMM's bundled environment.
- Agent action: Do not conclude that PMM cannot use BOSL2 just because PMM has trouble with arbitrary local include trees.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564
  - https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## require_default_asset_names

- Status: `supported`
- Scope: `uploads`
- Provenance: `Official release`
- Example syntax:
  - `"default.png"`
  - `"default.svg"`
  - `"default.stl"`
- Constraints:
  - PMM upload features are documented around built-in default filenames.
- Rewrite guidance: Rename or rewire uploaded asset variables to match documented PMM defaults.
- Agent action: Avoid arbitrary uploaded asset names in PMM-targeted scripts.
- Evidence:
  - https://forum.bambulab.com/t/paramatric-model-maker-v0-8-0-support-uploading-files/91853

## hex_string_color_only_for_ui

- Status: `supported`
- Scope: `colors`
- Provenance: `Official release`
- Example syntax:
  - `accent_hex = "#FF0000"; // color`
- Constraints:
  - Parameterized color UI is documented for hex strings rather than arbitrary color expressions.
- Rewrite guidance: Expose PMM color controls as hex string parameters and keep more complex color logic internal if needed.
- Agent action: Use simple hex-string parameters for PMM-exposed colors.
- Evidence:
  - https://forum.bambulab.com/t/paramatric-model-maker-v0-9-0-support-multi-color-modeling/100160

## font_comment_required

- Status: `supported`
- Scope: `fonts`
- Provenance: `Official release`
- Example syntax:
  - `font_name = "Roboto"; // font`
- Constraints:
  - The PMM font UI requires the `// font` marker.
- Rewrite guidance: Add `// font` only to parameters intended for PMM font selection.
- Agent action: Do not assume plain OpenSCAD font strings become PMM font controls automatically.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## multi_plate_stl_tradeoff

- Status: `caution`
- Scope: `export`
- Provenance: `Official release`
- Example syntax:
  - `module mw_plate_1() { ... }`
- Constraints:
  - The official release notes that multi-plate scripts cannot provide STL download from that script.
- Rewrite guidance: Consider separate release variants when both PMM multi-plate output and STL convenience matter.
- Agent action: Present multi-plate as a product decision, not only a code implementation detail.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## oversize_auto_arrange_risk

- Status: `caution`
- Scope: `layout`
- Provenance: `Employee-confirmed`
- Constraints:
  - Oversize models may fail 3MF generation.
  - Employee replies connect this to auto-arrange behavior and practical plate limits.
- Rewrite guidance: Split large output into multiple plates or document profile-setting expectations when a model approaches layout limits.
- Agent action: Flag oversize and auto-arrange risk in the upload plan.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-3mf-cannot-be-generated/133844
  - https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618
  - https://forum.bambulab.com/t/parametric-model-maker-model-is-rotated-after-generation/172901

## preview_comments_not_supported_feature

- Status: `unsupported`
- Scope: `comments`
- Provenance: `Employee-confirmed`
- Example syntax:
  - `// preview[...]`
- Constraints:
  - An employee explicitly said the preview comment example was not used by PMM itself.
- Rewrite guidance: Remove or ignore preview-comment reliance when porting a script to PMM.
- Agent action: Do not spend effort preserving preview-comment behavior as if it were a PMM feature.
- Evidence:
  - https://forum.bambulab.com/t/parametic-model-maker-colors-documentation/77524

## uploaded_stl_name_is_fragile

- Status: `caution`
- Scope: `uploads`
- Provenance: `Community-discovered`
- Example syntax:
  - `import("oven_knob_solid.stl");`
- Constraints:
  - Community evidence suggests PMM STL-backed workflows are safer when aligned with the documented `default.stl` pattern.
- Rewrite guidance: Prefer the official default-file convention over arbitrary co-uploaded STL naming assumptions.
- Agent action: Treat arbitrary uploaded STL filenames as risky unless separately confirmed by current PMM behavior.
- Evidence:
  - https://forum.bambulab.com/t/openscad-stl-import/247687
  - https://forum.bambulab.com/t/paramatric-model-maker-v0-8-0-support-uploading-files/91853

## avoid_direct_special_module_calls

- Status: `caution`
- Scope: `multi-plate`
- Provenance: `Community-discovered`
- Example syntax:
  - `mw_plate_1();`
  - `mw_assembly_view();`
- Constraints:
  - Community troubleshooting suggests special PMM modules should define output rather than be treated as ordinary helper calls.
- Rewrite guidance: Keep reusable geometry in neutral helper modules and reserve PMM-specific modules for output structure.
- Agent action: Do not build the whole model around directly calling PMM special modules as ordinary functions.
- Evidence:
  - https://forum.bambulab.com/t/parametric-model-maker-model-times-out-help/211145
