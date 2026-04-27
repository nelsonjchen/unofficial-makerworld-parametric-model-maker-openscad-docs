# PMM Font Index

Browse `1881` MakerWorld PMM font families and `8267` exact PMM font strings. The browser is family-first: select a family to inspect styles, exact OpenSCAD names, PMM font-dialog filter metadata, preview aliases, and provenance warnings. See [font provenance notes](font-provenance-notes.md) for licensing caveats and source evidence.

Local preview workflow:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
python3 scripts/build_font_index.py
.venv/bin/mkdocs serve -a 127.0.0.1:8000
```

Then open `http://127.0.0.1:8000/unofficial-makerworld-parametric-model-maker-openscad-docs/font-index/`.

<div id="pmm-font-index" class="pmm-font-index">
  <p class="pmm-font-index__loading">Loading generated font index...</p>
</div>

<link rel="stylesheet" href="../assets/font-index.css">
<script src="../assets/font-index.js"></script>
