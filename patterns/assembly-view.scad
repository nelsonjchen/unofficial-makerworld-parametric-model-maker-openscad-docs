// PMM assembly view pattern.
// Keep printable geometry in the plate modules and reserve assembly view for the combined preview.

module base_plate() {
    cube([60, 20, 3], center = true);
}

module top_plate() {
    cube([30, 20, 3], center = true);
}

module mw_plate_1() {
    base_plate();
}

module mw_plate_2() {
    top_plate();
}

module mw_assembly_view() {
    base_plate();
    translate([0, 0, 15]) top_plate();
}
