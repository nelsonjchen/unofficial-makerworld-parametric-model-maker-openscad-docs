// PMM multi-plate 3MF pattern.
// Provenance: official release v0.10.0.
// Note: scripts using this feature are documented as not offering STL download from that script.

part_a = 40;
part_b = 25;

module left_part() {
    cube([part_a, 20, 3], center = true);
}

module right_part() {
    cylinder(h = 3, d = part_b, $fn = 64);
}

module mw_plate_1() {
    left_part();
}

module mw_plate_2() {
    right_part();
}

module mw_assembly_view() {
    translate([-25, 0, 0]) left_part();
    translate([25, 0, 0]) right_part();
}
