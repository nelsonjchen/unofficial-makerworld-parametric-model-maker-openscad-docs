# Multi-Plate Release

Use this checklist before shipping a PMM script with multi-plate output.

- Confirm the model genuinely benefits from multiple printable plates.
- Keep shared geometry in normal helper modules instead of duplicating logic across plates.
- Define each printable plate in `mw_plate_N()`.
- Add `mw_assembly_view()` when users need a full assembled preview.
- Confirm the assembly view is visually helpful and not confused with a printable plate.
- Decide whether you need a separate STL-oriented script for users who do not want the multi-plate 3MF path.
- Validate the output against oversize and auto-arrange risks.
- Add user-facing release notes explaining the download/output tradeoff.
