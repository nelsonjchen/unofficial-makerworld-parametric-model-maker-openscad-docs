// PMM SVG upload pattern.
// Provenance: official release v0.8.0.
// PMM expects the built-in default filename for user-uploaded SVG workflows.

svg_file = "default.svg";
badge_size = 40;

linear_extrude(2)
offset(r = 1)
square([badge_size, badge_size], center = true);

translate([0, 0, 2])
linear_extrude(1.2)
scale([0.5, 0.5, 1])
import(file = svg_file, center = true);
