// Minimal PMM-oriented OpenSCAD pattern.
// See docs/feature-reference.md and docs/compatibility-rules.md.

label = "MakerWorld";
width_mm = 80;
height_mm = 24;
thickness_mm = 3;

linear_extrude(thickness_mm)
difference() {
    offset(r = 2)
        square([width_mm, height_mm], center = true);
    text(label, size = height_mm * 0.45, halign = "center", valign = "center");
}
