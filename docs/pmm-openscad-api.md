# PMM OpenSCAD API

This is the practical OpenSCAD-facing API surface for Bambu MakerWorld Parametric Model Maker.

PMM is not documented as a formal language extension by Bambu. In this repo, "API" means the supported comments, module names, file naming conventions, runtime assets, and workflow contracts that OpenSCAD authors can target when making a MakerWorld-customizable model.

This reference was generated with AI assistance and may miss details or get something wrong. If you find an issue, please [open a repository issue](https://github.com/nelsonjchen/unofficial-makerworld-parametric-model-maker-openscad-docs/issues) with the correction or missing case.

## Quick Reference

| Surface | Syntax | Use It For | Status |
| --- | --- | --- | --- |
| Color picker | `accent = "#FF0000"; // color` | Expose a PMM color UI for a hex string parameter. | Supported |
| Font picker | `font_name = "Roboto"; // font` | Expose a PMM font selector for a font-name parameter. | Supported |
| Multi-plate output | `module mw_plate_1() { ... }` | Define printable plates for generated 3MF output. | Supported |
| Assembly preview | `module mw_assembly_view() { ... }` | Show a whole-model preview for multi-part output. | Supported |
| File upload defaults | `"default.png"`, `"default.svg"`, `"default.stl"` | Refer to PMM-uploaded default assets. | Supported |
| Bundled libraries | `include <BOSL2/std.scad>;` | Use MakerWorld-bundled OpenSCAD libraries. | Supported, inventory-backed |
| Font inventory | `fonts-0.8.0.json` | Check exact installed PMM font names. | Supported, endpoint-backed |
| Broad font catalog | `fonts-show-0.0.1.json` | Discover PMM-visible font options. | Supported, endpoint-backed |

## Parameter API

PMM primarily follows OpenSCAD Customizer-style parameters:

```scad
label_text = "MakerWorld";
width_mm = 80;
height_mm = 24;
```

Prefer simple top-level assignments for user-facing controls. Keep complex derived values inside helper modules or functions so the PMM UI presents the few knobs a maker actually needs.

Do not rely on undocumented comment systems unless separately confirmed. In particular, `// preview[...]` is documented in this repo as not a PMM feature.

Evidence:
- [Customizer compatibility](feature-reference.md#customizer_compatibility)
- [Preview comments are unsupported](compatibility-rules.md#preview_comments_not_supported_feature)

## Color Picker

Use `// color` on a hex string parameter when you want PMM to expose a color picker.

```scad
body_color = "#2F80ED"; // color
accent_color = "#F2994A"; // color

color(body_color)
cube([40, 20, 4]);
```

Guidance:
- Use hex strings such as `"#FF0000"`.
- Put `// color` only on parameters meant for the PMM UI.
- Keep internal color calculations separate from user-facing color controls.

Evidence:
- [Parameterized color UI](feature-reference.md#parameterized_color_ui)
- [Color parameter pattern](../patterns/color-parameter.scad)

## Font Picker

Use `// font` on a font-name parameter when you want PMM to expose a font selector.

```scad
label = "Hello";
font_name = "Roboto"; // font

linear_extrude(2)
text(label, font = font_name, size = 12, halign = "center", valign = "center");
```

Guidance:
- Check the [installed font inventory](../sources/raw/makerworld/fonts-0.8.0.json) for stricter runtime compatibility.
- Use the [broader font catalog](../sources/raw/makerworld/fonts-show-0.0.1.json) for discovery.
- For multilingual fallback research, see the [language-to-family map asset](../sources/raw/makerworld/language2family-0.0.1.zip).

Evidence:
- [Font picker UI](feature-reference.md#font_picker_ui)
- [Font inventory validation rule](compatibility-rules.md#validate_fonts_against_installed_inventory)
- [Font parameter pattern](../patterns/font-parameter.scad)

## File Upload Defaults

PMM file-upload workflows are documented around built-in default filenames:

```scad
svg_file = "default.svg";

linear_extrude(2)
import(svg_file);
```

```scad
stl_file = "default.stl";

import(stl_file);
```

Guidance:
- Prefer `default.png`, `default.svg`, or `default.stl` over arbitrary co-uploaded names.
- Treat arbitrary uploaded filenames as fragile unless you have current UI evidence.
- Include the expected default asset name in the MakerWorld upload plan.

Evidence:
- [File upload default assets](feature-reference.md#file_upload_default_assets)
- [Default asset name rule](compatibility-rules.md#require_default_asset_names)
- [SVG upload pattern](../patterns/file-upload-svg.scad)
- [STL upload pattern](../patterns/file-upload-stl.scad)

## Multi-Plate 3MF Output

Define printable plates with `mw_plate_N()` modules.

```scad
module part_a() {
    cube([30, 20, 4]);
}

module part_b() {
    cylinder(h = 8, r = 10);
}

module mw_plate_1() {
    part_a();
}

module mw_plate_2() {
    part_b();
}
```

Guidance:
- Use sequential plate modules such as `mw_plate_1()`, `mw_plate_2()`, and so on.
- Keep reusable model geometry in neutral helper modules.
- Use `mw_plate_N()` as PMM output definitions, not as ordinary helper calls.
- Multi-plate scripts are 3MF-first and have a documented STL-download tradeoff.

Evidence:
- [Multi-plate 3MF](feature-reference.md#multi_plate_3mf)
- [Multi-plate STL tradeoff](compatibility-rules.md#multi_plate_stl_tradeoff)
- [Multi-plate pattern](../patterns/multi-plate-3mf.scad)

## Assembly View

Use `mw_assembly_view()` when a multi-part model needs a combined preview.

```scad
module mw_assembly_view() {
    part_a();
    translate([40, 0, 0])
        part_b();
}
```

Guidance:
- Assembly view is for previewing the full assembly.
- Do not use assembly view as the only printable output.
- It is not included in exported 3MF output.

Evidence:
- [Assembly view](feature-reference.md#assembly_view)
- [Assembly view pattern](../patterns/assembly-view.scad)

## Bundled Library Runtime

PMM can use MakerWorld-bundled OpenSCAD libraries. Do not remove BOSL2 just because arbitrary local include trees are risky.

```scad
include <BOSL2/std.scad>;
```

Current bundled-library evidence is stored in the raw [MakerWorld library inventory](../sources/raw/makerworld/libraries-0.8.0.json), with a normalized agent index at [data/bundled-library-index.json](../data/bundled-library-index.json).

Important limitation: the MakerWorld inventory lists source URLs, descriptions, and include methods. It does not pin an installed commit for every library. Treat upstream repo HEADs and latest tags as upstream information, not proof of PMM's installed runtime. The only bundled-library pinned revision currently captured in this repo is the BOSL2 commit Bambu documented in the v1.1.0 release.

| Library | PMM Include Method | Source | Version Or Revision Clue |
| --- | --- | --- | --- |
| BOSL2 | `include <BOSL2/*.scad>;` | [BelfrySCAD/BOSL2](https://github.com/BelfrySCAD/BOSL2) | Inventory description says `v2.0`; Bambu v1.1.0 release documents BOSL2 commit [`99fcfc6867e739aa1cd8ffc49fe39276036681f1`](https://github.com/BelfrySCAD/BOSL2/commit/99fcfc6867e739aa1cd8ffc49fe39276036681f1). |
| UB | `include <ub.scad>;` | [UBaer21/UB.scad](https://github.com/UBaer21/UB.scad) | Inventory description says `OpenSCAD v.21 and above`; this appears to be compatibility text, not a PMM-pinned UB revision. |
| KeyV2 | `include <KeyV2/*.scad>;` | [rsheldiii/keyv2](https://github.com/rsheldiii/keyv2) | No PMM-pinned version or commit listed in the inventory. |
| gridfinity-rebuilt-openscad | `include <gridfinity-rebuilt-openscad/*.scad>;` | [kennetek/gridfinity-rebuilt-openscad](https://github.com/kennetek/gridfinity-rebuilt-openscad) | No PMM-pinned version or commit listed in the inventory. |
| threads-scad | `include <threads-scad/threads.scad>;` | [rcolyer/threads-scad](https://github.com/rcolyer/threads-scad/) | No PMM-pinned version or commit listed in the inventory. |
| Getriebe | `include <Getriebe.scad>;` | [OpenSCAD-Getriebebibliothek](https://github.com/janssen86/OpenSCAD-Getriebebibliothek/tree/master) | No PMM-pinned version listed; inventory source URL points at upstream `master`. |
| knurledFinishLib_v2 | `include <knurledFinishLib_v2.scad>;` | [Thingiverse thing 32122](https://www.thingiverse.com/thing:32122) | Library name and description indicate `v2`, but no PMM-pinned commit or release artifact is listed. |

Guidance:
- Distinguish bundled PMM libraries from local project includes.
- Flatten or inline arbitrary local dependencies when PMM is unlikely to have them.
- For BOSL2-specific behavior, account for the PMM-documented BOSL2 revision when troubleshooting.

Evidence:
- [Bundled library inventory endpoint](feature-reference.md#bundled_library_inventory_endpoint)
- [Bundled BOSL2 library](feature-reference.md#bundled_bosl2_library)
- [Bundled BOSL2 vs local includes](compatibility-rules.md#distinguish_bundled_bosl2_from_local_includes)

## Backend And Export Contract

PMM OpenSCAD output is shaped by MakerWorld's backend and export pipeline, not only by local OpenSCAD rendering.

Account for:
- documented OpenSCAD backend revisions
- manifold being enabled in employee-confirmed backend notes
- 3MF generation behavior
- auto-arrange and oversize model failures
- multi-color and multi-plate export behavior

Evidence:
- [Backend manifold enabled](feature-reference.md#backend_manifold_enabled)
- [Backend refresh v1.1.0](feature-reference.md#backend_refresh_v1_1_0)
- [Oversize auto-arrange risk](compatibility-rules.md#oversize_auto_arrange_risk)
- [Gotchas](gotchas.md)

## Minimal PMM-Ready Skeleton

```scad
label_text = "MakerWorld";
width_mm = 80;
height_mm = 24;
thickness_mm = 3;
accent_hex = "#FF6600"; // color
font_name = "Roboto"; // font

module core_model() {
    linear_extrude(thickness_mm)
    difference() {
        offset(r = 2)
            square([width_mm, height_mm], center = true);
        text(label_text, font = font_name, size = height_mm * 0.45, halign = "center", valign = "center");
    }
}

color(accent_hex)
core_model();
```

Use the [PMM-ready template](../patterns/pmm-ready-template.scad) as the editable starter template.

## Related References

- [Agent workflow](agent-workflow.md)
- [Feature reference](feature-reference.md)
- [Compatibility rules](compatibility-rules.md)
- [Publishing workflow](publishing-workflow.md)
- [Web discovery](web-discovery.md)
- [Pre-upload validation checklist](../checklists/pre-upload-validation.md)
