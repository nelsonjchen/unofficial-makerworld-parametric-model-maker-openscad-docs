# Changelog

This changelog is implementation-oriented. Each entry highlights what changed, what an agent can do differently, and what tradeoffs still matter.

## 2024-05-10 - integration - PMM integrated into MakerWorld model pages

Provenance: `Official release`

**What changed:** MakerWorld announced that Parametric Model Maker was integrated into model pages so users could customize OpenSCAD-backed models directly from the model page.

**Agent impact:** Agents can assume a first-class model-page customization flow exists and should package PMM-ready scripts around that user journey.

**Tradeoffs:** Early PMM UX still had rough edges, so implementation guidance should separate existence of the flow from maturity of the UX.

Evidence:
- https://forum.bambulab.com/t/makerworld-update-05-10/74832

## 2024-08-06 - v0.8.0 - File upload support with default asset names

Provenance: `Official release`

**What changed:** PMM added file upload support for PNG, SVG, and STL workflows using documented built-in default filenames.

**Agent impact:** Agents can convert some local asset-backed models into PMM-compatible upload workflows, but should rewrite asset names to `default.png`, `default.svg`, or `default.stl`.

**Tradeoffs:** The release note described filename restrictions and did not present arbitrary co-upload naming as a safe default.

Evidence:
- https://forum.bambulab.com/t/paramatric-model-maker-v0-8-0-support-uploading-files/91853

## 2024-09-23 - v0.9.0 - Multi-color 3MF and `// color` parameter support

Provenance: `Official release`

**What changed:** PMM added multi-color 3MF export and documented a parameterized color UI using hex string variables with the `// color` marker.

**Agent impact:** Agents can expose user-facing color controls in PMM by switching to hex string parameters rather than only hard-coded OpenSCAD color literals.

**Tradeoffs:** This did not remove geometry or layout constraints, and later employee replies tied some generation issues to the new 3MF path and sizing behavior.

Evidence:
- https://forum.bambulab.com/t/paramatric-model-maker-v0-9-0-support-multi-color-modeling/100160

## 2025-01-19 - post-v0.9 clarification - Employee clarification around oversize 3MF failures

Provenance: `Employee-confirmed`

**What changed:** An employee explained that PMM's newer 3MF generation path could fail when a model was oversize and noted that plate splitting work was underway.

**Agent impact:** Agents should flag oversize risk explicitly and consider splitting large output or changing release strategy rather than assuming local success means PMM success.

**Tradeoffs:** A model can be logically valid OpenSCAD and still fail PMM generation because export and plate-layout constraints differ from local rendering.

Evidence:
- https://forum.bambulab.com/t/parametric-model-maker-3mf-cannot-be-generated/133844

## 2025-02-10 - v0.10.0 - Multi-plate 3MF, assembly view, 3MF profile config, and font picker UI

Provenance: `Official release`

**What changed:** PMM added `mw_plate_N()`, optional `mw_assembly_view()`, 3MF profile configuration, a richer font picker triggered by `// font`, and better oversized-model error messaging.

**Agent impact:** Agents can now build richer PMM releases for multi-part models, document profile-side concerns, and expose font selection more cleanly.

**Tradeoffs:** The release note explicitly warns that multi-plate scripts do not also provide STL download from that same script, so agents should treat this as a release-strategy choice.

Evidence:
- https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## 2025-02-16 - v0.10.0 follow-up - Auto-arrange size limitation discussed and then fixed for a reported model

Provenance: `Employee-confirmed`

**What changed:** Employee replies connected generation failures to Studio auto-arrange behavior, discussed a practical size ceiling around `240 x 235`, and later confirmed a reported issue was fixed.

**Agent impact:** Agents should treat PMM export failures as possibly layout-driven and include profile and arrangement notes when packaging larger models.

**Tradeoffs:** Disabling auto-arrange or splitting output may still be necessary depending on model shape and release design.

Evidence:
- https://forum.bambulab.com/t/parametric-model-maker-v0-10-0-multi-plate-3mf-generation/144618

## 2025-03-13 - backend clarification - Employee clarification on backend commit and manifold

Provenance: `Employee-confirmed`

**What changed:** An employee stated that PMM was using OpenSCAD commit `b550957ddac62e59428d08efa62e2f44c15a0b95` and that manifold was enabled.

**Agent impact:** Agents can document a concrete PMM backend assumption when local and hosted behavior diverge.

**Tradeoffs:** This still does not make arbitrary local include trees portable; backend version clarity helps debugging, not packaging safety by itself.

Evidence:
- https://forum.bambulab.com/t/parametric-model-maker-support-for-includes/150680

## 2025-10-25 - v1.1.0 - OpenSCAD workflow and backend refresh

Provenance: `Official release`

**What changed:** PMM v1.1.0 refreshed the UI, collapsed the OpenSCAD editor behind a Code button, added an Open SCAD File flow under the Creator Portal, and documented updated OpenSCAD and BOSL2 backend revisions.

**Agent impact:** Agents can describe the newer PMM editing workflow accurately and use the documented backend revisions when reasoning about reproducibility.

**Tradeoffs:** This is still an OpenSCAD-relevant workflow update even though PMM as a whole had broadened beyond OpenSCAD by then.

Evidence:
- https://forum.bambulab.com/t/parametric-model-maker-v1-1-0-major-ui-refresh/203564
