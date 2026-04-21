// PMM color parameter pattern.
// Provenance: official release v0.9.0.
// Evidence: forum.bambulab.com/t/paramatric-model-maker-v0-9-0-support-multi-color-modeling/100160

accent_hex = "#FF6600"; // color
base_hex = "#E6E6E6"; // color
size_mm = 20;

color(base_hex)
cube([size_mm * 2, size_mm, 2], center = true);

translate([0, 0, 2])
color(accent_hex)
cylinder(h = 4, d = size_mm, $fn = 64);
