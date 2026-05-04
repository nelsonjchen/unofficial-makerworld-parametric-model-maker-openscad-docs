# Community Tooling

This page collects external project workflows that are useful examples for PMM-oriented OpenSCAD authors. These are community practice examples, not authoritative PMM feature evidence. Use them to shape local tooling and release process, then rely on this repo's API, feature, compatibility, and provenance docs for PMM behavior claims.

## HomeRacker

[kellerlabs/homeracker](https://github.com/kellerlabs/homeracker) is a practical example of maintaining a larger OpenSCAD model family while publishing MakerWorld-friendly parametric exports.

The useful pattern is:

- Keep source models organized as reusable OpenSCAD libraries plus renderable `parts/` entrypoints with OpenSCAD Customizer parameters.
- Treat local project includes as a source-authoring convenience, then generate flattened export files for MakerWorld.
- Preserve `include <BOSL2/std.scad>` rather than inlining BOSL2, because BOSL2 is a bundled PMM library while arbitrary project-local include trees are the portability risk.
- Validate both source and flattened outputs with an OpenSCAD render step before publishing.
- Keep MakerWorld descriptions in git-tracked Markdown and convert them to MakerWorld-ready HTML during release.

HomeRacker's tooling centers on [`scadm`](https://pypi.org/project/scadm/), an externally installable OpenSCAD dependency and workflow helper. It is close in spirit to a small bundler for OpenSCAD projects: a project declares dependencies and flatten targets in `scadm.json`, then `scadm flatten --all` resolves local include trees into generated single-file exports suitable for MakerWorld-style upload flows. `scadm render` validates source or flattened models through OpenSCAD.

Install example:

```bash
pip install scadm
```

This is a useful reference workflow for larger PMM projects, but it is not a required dependency for this repository.

Relevant HomeRacker references:

- [HomeRacker repository](https://github.com/kellerlabs/homeracker)
- [scadm on PyPI](https://pypi.org/project/scadm/)
- [MakerWorld export workflow](https://github.com/kellerlabs/homeracker/blob/main/cmd/export/README.md)
- [scadm README](https://github.com/kellerlabs/homeracker/blob/main/cmd/scadm/README.md)
- [MakerWorld description workflow](https://github.com/kellerlabs/homeracker/blob/main/docs/makerworld-workflow.md)
- [scadm.json example](https://github.com/kellerlabs/homeracker/blob/main/scadm.json)

## How To Use This Example

For a small one-file model, this workflow is probably more structure than you need. For a model family with shared OpenSCAD modules, tests, generated previews, or repeated MakerWorld releases, it points to a robust split:

- Author against maintainable local source files.
- Export PMM-facing single-file scripts from those sources.
- Keep bundled platform libraries such as BOSL2 as bundled-library includes.
- Validate generated exports before upload.
- Version user-facing MakerWorld listing text alongside the model source.
