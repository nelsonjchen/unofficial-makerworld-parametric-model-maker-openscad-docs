// PMM-ready OpenSCAD template.
// Use this as a starting point when adapting a local model for MakerWorld PMM.
// Read:
// - docs/pmm-openscad-api.md
// - docs/agent-workflow.md
// - docs/feature-reference.md
// - docs/compatibility-rules.md

// Basic user-facing parameters.
label_text = "MakerWorld";
width_mm = 80;
height_mm = 24;
thickness_mm = 3;

// Optional PMM UI parameters.
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

// Default single-plate output.
color(accent_hex)
core_model();

// Optional PMM multi-plate structure.
// Uncomment and adapt only if the model truly benefits from multi-plate 3MF.
//
// module mw_plate_1() {
//     core_model();
// }
//
// module mw_assembly_view() {
//     core_model();
// }
