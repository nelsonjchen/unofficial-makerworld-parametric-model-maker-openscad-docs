# Convert Existing Script

Use this checklist when converting a normal OpenSCAD project into a PMM-oriented script.

- Identify which parameters should become user-facing PMM controls.
- Check for `include` or `use` statements that depend on local files.
- Distinguish bundled libraries such as BOSL2 from arbitrary local project includes before rewriting.
- Check for `import()` calls that assume arbitrary asset names.
- Flatten or rewrite fragile local project structure before PMM-specific tweaks.
- Keep the core model rendering correctly before adding PMM-only comments.
- Add `// color` only to hex string parameters intended for PMM color UI.
- Add `// font` only to font name parameters intended for PMM font UI.
- Decide whether the model should stay single-plate or move to `mw_plate_N()`.
- If using multi-plate, decide whether a separate STL-oriented script is still needed.
- Add clear user-facing notes about upload expectations, output tradeoffs, and geometry limits.
