# Pre-Upload Validation

- The script renders locally with default parameters.
- The user-facing parameters are simple and intentional.
- PMM-specific comments such as `// color` and `// font` are applied only where needed.
- Uploaded asset workflows use PMM-supported default filenames.
- The script does not depend on arbitrary local file layout.
- Single-plate models fit practical PMM sizing expectations.
- Multi-plate models expose `mw_plate_N()` cleanly and use `mw_assembly_view()` only for preview.
- The release notes and user description explain whether 3MF or STL is the primary expected output.
- Any community-only assumptions are labeled as such in comments or release notes.
