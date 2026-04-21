// PMM font picker pattern.
// Provenance: official release v0.10.0.
// Evidence: forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

text_value = "PMM";
font_name = "Roboto"; // font
plate_width = 80;
plate_height = 24;

linear_extrude(3)
difference() {
    offset(r = 2)
        square([plate_width, plate_height], center = true);
    text(text_value, font = font_name, size = 12, halign = "center", valign = "center");
}
