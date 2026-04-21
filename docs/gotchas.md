# Gotchas

This page focuses on PMM-specific pitfalls that agents are likely to trip over while adapting OpenSCAD.

## Uploaded Assets Use PMM Default Filenames
Provenance: `Official release`

If you want PMM file upload support, do not assume arbitrary filenames. The documented defaults are:
- `default.png`
- `default.svg`
- `default.stl`

This matters because a locally working `import("my-logo.svg")` may fail conceptually in PMM unless the script is rewritten around PMM's supported naming scheme.

Evidence:
- [Paramatric Model Maker V0.8.0 support uploading files!](https://forum.bambulab.com/t/91853)

## Parameterized Colors Need Hex Strings Plus `// color`
Provenance: `Official release`

Color export support and parameterized color UI are not the same thing. PMM's documented parameter UI expects hex string variables annotated with `// color`.

Evidence:
- [Paramatric Model Maker V0.9.0 - Support Multi-Color Modeling](https://forum.bambulab.com/t/100160)

## Font Picker UI Requires `// font`
Provenance: `Official release`

If an agent adds a font parameter but forgets the `// font` marker, the script may still be valid OpenSCAD, but the PMM font picker will not appear.

Evidence:
- [Parametric Model Maker V0.10.0 - Multi-Plate 3MF Generation](https://forum.bambulab.com/t/144618)

## Multi-Plate 3MF Has A Real STL Tradeoff
Provenance: `Official release`

Multi-plate support is useful, but the release note explicitly warns that scripts using this feature prevent users from downloading STL from that script. Agents should treat this as a release-strategy decision, not just a code change.

Evidence:
- [Parametric Model Maker V0.10.0 - Multi-Plate 3MF Generation](https://forum.bambulab.com/t/144618)

## Oversize And Auto-Arrange Failures Are Easy To Trigger
Provenance: `Employee-confirmed`

An employee explained that generation failures could come from Studio trying to auto-arrange objects, and discussed a practical size ceiling around `240 x 235` in that context. This means an agent should think about layout and profile settings, not just geometry.

Evidence:
- [Parametric Model Maker: 3MF cannot be generated](https://forum.bambulab.com/t/133844)
- [Parametric Model Maker V0.10.0 - Multi-Plate 3MF Generation](https://forum.bambulab.com/t/144618)

## Local Includes Are Not A Safe Default
Provenance: `Employee-confirmed`

Community usage and employee replies indicate PMM can work with supplied platform libraries, but not with arbitrary local include trees the same way a local OpenSCAD project does. Agents should flatten or inline fragile local dependencies unless the dependency is clearly available in PMM.

Evidence:
- [Parametric Model Maker support for includes](https://forum.bambulab.com/t/150680)

## `// preview[...]` Is Not A PMM Feature
Provenance: `Employee-confirmed`

An employee explained that a `// preview[...]` style comment seen in examples was not actually used by PMM itself, and that PMM mainly follows OpenSCAD Customizer behavior with some Thingiverse-compatibility intent. Agents should not rely on preview comments as PMM functionality.

Evidence:
- [Parametic Model Maker - colors? documentation?](https://forum.bambulab.com/t/77524)

## Arbitrary Co-Uploaded STL Names Are Risky
Provenance: `Community-discovered`

A later community thread suggests that uploaded STL-backed workflows may need the PMM-supported `default.stl` approach rather than arbitrary co-uploaded filenames. Treat this as useful but less authoritative than release-note guidance.

Evidence:
- [OpenSCAD stl import](https://forum.bambulab.com/t/247687)

## Heavy Geometry May Timeout Even When Local OpenSCAD Eventually Renders
Provenance: `Community-discovered`

PMM rendering appears to have practical runtime constraints. An agent should simplify geometry, reduce expensive global detail settings, and be cautious with heavy BOSL2 usage where performance matters.

Evidence:
- [Parametric Model Maker - Model Times out - help?](https://forum.bambulab.com/t/211145)
- [Parametric Model Maker - Timeout on simple SCAD](https://forum.bambulab.com/t/188591)
