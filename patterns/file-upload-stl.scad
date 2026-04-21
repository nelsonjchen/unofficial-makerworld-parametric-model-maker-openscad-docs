// PMM STL upload pattern.
// Provenance: official release v0.8.0.
// Community follow-up suggests default.stl is the safest PMM-oriented convention.

insert_file = "default.stl";

difference() {
    cube([30, 30, 10], center = true);
    translate([0, 0, 2])
        import(insert_file);
}
