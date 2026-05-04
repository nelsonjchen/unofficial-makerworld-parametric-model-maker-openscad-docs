# Publishing Workflow

This is the practical path from a local OpenSCAD script to a MakerWorld-customizable PMM model.

## 1. Stabilize The Local OpenSCAD
- Make sure the script renders locally with the intended default parameters.
- Remove dependencies on arbitrary local file layout where possible.
- Decide whether the model is single-plate or truly needs multi-plate output.

For larger source trees, a generated-export workflow can be easier to maintain than hand-editing a single PMM file. See `docs/community-tooling.md` for a community example.

## 2. PMM-Enable The Script
- Convert important user-facing values into simple top-level parameters.
- Add `// color` only to hex string parameters you want PMM to expose as colors.
- Add `// font` only to font name parameters you want PMM to expose in the font picker.
- If using file upload features, switch to PMM-supported default asset names.

## 3. Choose A Packaging Strategy
### Single file, single plate
Use this when:
- The model fits one plate.
- STL download simplicity matters.
- The model does not need an assembly preview.

### Single file, multi-plate 3MF
Use this when:
- The model has multiple printable parts that do not fit or should not be arranged as a single plate.
- A richer PMM experience is worth the STL tradeoff.

### Split release strategy
Use this when:
- You want a multi-plate 3MF workflow for PMM users.
- You also want a simpler STL-oriented path.

## 4. Validate PMM-Specific Risks
Before release, check:
- Oversize risk.
- Auto-arrange risk.
- Timeout risk for heavier geometry.
- Import or include fragility.
- User confusion around assembly preview versus printable plates.

## 5. Upload And Test In PMM
- Upload or open the script in MakerWorld PMM.
- Confirm the parameters render as intended.
- Confirm file upload parameters behave as expected.
- If using multi-plate, confirm each plate output and the assembly preview are understandable.

## 6. Add User-Facing Notes
Tell users what matters:
- Whether the model expects uploaded assets such as SVG or STL.
- Whether the model is multi-plate and therefore optimized for 3MF.
- Whether users should expect STL or 3MF as the better download path.
- Any size or arrangement notes that can prevent generation failure.

## 7. Keep Evidence Nearby
When possible, note the rationale with links to:
- `docs/feature-reference.md`
- `docs/compatibility-rules.md`
- `docs/gotchas.md`
- `docs/changelog.md`

External project workflows can be cited inline as examples, but do not use them as proof that PMM supports a feature.
