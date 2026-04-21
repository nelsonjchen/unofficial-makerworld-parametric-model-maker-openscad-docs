#!/usr/bin/env python3
"""Build normalized source, topic, feature, and compatibility indexes."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DISCOURSE_DIR = REPO_ROOT / "sources" / "raw" / "discourse"
RAW_MAKERWORLD_DIR = REPO_ROOT / "sources" / "raw" / "makerworld"
RAW_MANUAL_DIR = REPO_ROOT / "sources" / "raw" / "manual"
DATA_DIR = REPO_ROOT / "data"

EMPLOYEE_USERNAMES = {"PineappleBun_BBL", "ypy", "MakerWorld"}

TOPIC_NOTES = {
    74832: {"summary": "MakerWorld update that integrated PMM into model pages.", "scope": "OpenSCAD", "tags": ["release", "integration"]},
    75758: {"summary": "Early community feedback thread about PMM UX and documentation gaps.", "scope": "OpenSCAD", "tags": ["feedback", "ux"]},
    77524: {"summary": "Employee-confirmed early color limitation and Customizer compatibility notes.", "scope": "OpenSCAD", "tags": ["colors", "compatibility"]},
    91853: {"summary": "Official v0.8.0 release thread for PMM file upload support.", "scope": "OpenSCAD", "tags": ["release", "uploads"]},
    100160: {"summary": "Official v0.9.0 release thread for multi-color 3MF and // color support.", "scope": "OpenSCAD", "tags": ["release", "colors", "3mf"]},
    128380: {"summary": "Maintenance outage thread showing operational fragility and community impact.", "scope": "OpenSCAD", "tags": ["ops", "availability"]},
    133844: {"summary": "Employee-confirmed oversize and 3MF generation behavior after color-related changes.", "scope": "OpenSCAD", "tags": ["3mf", "oversize"]},
    142549: {"summary": "Community thread on bezier or BOSL2 path issues.", "scope": "OpenSCAD", "tags": ["bosl2", "geometry"]},
    144618: {"summary": "Official v0.10.0 release thread for multi-plate 3MF, // font, and profile config.", "scope": "OpenSCAD", "tags": ["release", "multi-plate", "fonts"]},
    150680: {"summary": "Employee-confirmed notes on includes, backend commit, and manifold.", "scope": "OpenSCAD", "tags": ["includes", "backend"]},
    154198: {"summary": "Community feature request around custom fonts.", "scope": "OpenSCAD", "tags": ["fonts", "request"]},
    156334: {"summary": "Community-written tutorial that confirms real documentation demand.", "scope": "OpenSCAD", "tags": ["tutorial", "documentation"]},
    172894: {"summary": "Community request around output filename customization.", "scope": "OpenSCAD", "tags": ["filenames", "request"]},
    172899: {"summary": "Community request around preserving model information in generated assets.", "scope": "OpenSCAD", "tags": ["metadata", "request"]},
    172901: {"summary": "Employee-confirmed auto-arrange explanation for rotated model behavior.", "scope": "OpenSCAD", "tags": ["auto-arrange", "layout"]},
    188591: {"summary": "Employee-confirmed outage and timeout incident affecting 3MF export.", "scope": "OpenSCAD", "tags": ["timeout", "ops"]},
    203564: {"summary": "Official v1.1.0 release thread with OpenSCAD UI and backend updates.", "scope": "OpenSCAD", "tags": ["release", "backend", "ui"]},
    211145: {"summary": "Community performance and timeout discussion for complex PMM models.", "scope": "OpenSCAD", "tags": ["timeout", "performance"]},
    230605: {"summary": "Recent thread asking for PMM documentation, confirming discoverability pain.", "scope": "OpenSCAD", "tags": ["documentation"]},
    247687: {"summary": "Community thread suggesting default.stl conventions for STL-backed workflows.", "scope": "OpenSCAD", "tags": ["uploads", "stl"]},
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def parse_manual_capture_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block = text[4:end]
    metadata = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def build_topic_index() -> tuple[list[dict], dict[int, dict]]:
    records = []
    topic_map = {}
    for path in sorted(RAW_DISCOURSE_DIR.glob("topic-*.json")):
        if path.name.endswith(".meta.json"):
            continue
        data = load_json(path)
        first_post = data["post_stream"]["posts"][0]
        topic_id = int(data["id"])
        slug = data.get("slug") or str(topic_id)
        record = {
            "topic_id": topic_id,
            "title": data["title"],
            "url": f"https://forum.bambulab.com/t/{slug}/{topic_id}",
            "created_at": first_post["created_at"],
            "author_username": first_post["username"],
            "post_count": len(data["post_stream"]["posts"]),
            "has_employee_reply": any(post["username"] in EMPLOYEE_USERNAMES for post in data["post_stream"]["posts"]),
            "source_type": "discourse_json",
            "scope": TOPIC_NOTES.get(topic_id, {}).get("scope", "OpenSCAD"),
            "summary": TOPIC_NOTES.get(topic_id, {}).get("summary", ""),
            "tags": TOPIC_NOTES.get(topic_id, {}).get("tags", []),
            "raw_path": str(path.relative_to(REPO_ROOT)),
            "meta_path": str(path.with_suffix(path.suffix + ".meta.json").relative_to(REPO_ROOT)),
        }
        records.append(record)
        topic_map[topic_id] = record
    records.sort(key=lambda item: item["topic_id"])
    return records, topic_map


def build_source_index() -> list[dict]:
    records = []
    for path in sorted(RAW_MAKERWORLD_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.name == "README.md" or path.name.endswith(".meta.json"):
            continue
        meta_path = path.with_suffix(path.suffix + ".meta.json")
        metadata = load_json(meta_path) if meta_path.exists() else {}
        records.append(
            {
                "path": str(path.relative_to(REPO_ROOT)),
                "metadata_path": str(meta_path.relative_to(REPO_ROOT)) if meta_path.exists() else None,
                "source_type": metadata.get("source_type", "makerworld_json"),
                "origin": metadata.get("origin", "MakerWorld PMM app endpoint"),
                "captured_at": metadata.get("captured_at"),
                "url": metadata.get("url"),
                "capture_method": metadata.get("capture_method"),
                "verbatim": metadata.get("verbatim", True),
                "notes": metadata.get("notes", ""),
            }
        )
    for path in sorted(RAW_DISCOURSE_DIR.glob("*.json")):
        if path.name.endswith(".meta.json"):
            continue
        meta_path = path.with_suffix(path.suffix + ".meta.json")
        metadata = load_json(meta_path) if meta_path.exists() else {}
        record = {
            "path": str(path.relative_to(REPO_ROOT)),
            "metadata_path": str(meta_path.relative_to(REPO_ROOT)) if meta_path.exists() else None,
            "source_type": metadata.get("source_type", "discourse_json"),
            "origin": metadata.get("origin", "Bambu Lab Community Forum (Discourse)"),
            "captured_at": metadata.get("captured_at"),
            "url": metadata.get("url"),
            "capture_method": metadata.get("capture_method"),
            "verbatim": metadata.get("verbatim", True),
            "notes": metadata.get("notes", ""),
        }
        records.append(record)
    for path in sorted(RAW_MANUAL_DIR.glob("*.md")):
        if path.name in {"README.md", "template-manual-capture.md"}:
            continue
        metadata = parse_manual_capture_frontmatter(path)
        if not metadata:
            continue
        records.append(
            {
                "path": str(path.relative_to(REPO_ROOT)),
                "metadata_path": None,
                "source_type": metadata.get("source_type", "manual_capture"),
                "origin": metadata.get("origin", "PMM UI"),
                "captured_at": metadata.get("captured_at"),
                "url": metadata.get("url", ""),
                "capture_method": metadata.get("capture_method", ""),
                "verbatim": metadata.get("verbatim", "false").lower() == "true",
                "notes": metadata.get("notes", ""),
            }
        )
    return records


def build_feature_index(topic_map: dict[int, dict]) -> list[dict]:
    def evidence(topic_ids: list[int]) -> list[str]:
        return [topic_map[topic_id]["url"] for topic_id in topic_ids if topic_id in topic_map]

    return [
        {
            "feature_key": "bundled_library_inventory_endpoint",
            "status": "supported",
            "introduced_in": "libraries-0.8.0 endpoint",
            "scope": "libraries",
            "syntax": ["include <BOSL2/*.scad>;", "include <threads-scad/threads.scad>;"],
            "constraints": [
                "MakerWorld exposes a direct JSON inventory of bundled OpenSCAD libraries.",
                "This inventory is stronger evidence for bundled-library support than forum inference alone.",
            ],
            "rewrite_guidance": "When judging library support, check the MakerWorld library inventory before flattening working bundled includes.",
            "agent_action": "Use the bundled library inventory as the primary source for whether PMM ships a given library.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json"
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "model_page_integration",
            "status": "supported",
            "introduced_in": "2024-05-10",
            "scope": "ui",
            "syntax": [],
            "constraints": ["PMM is integrated into MakerWorld model pages rather than being only a separate tool entrypoint."],
            "rewrite_guidance": "Assume model-page customization exists; do not design around the older detached workflow.",
            "agent_action": "Package the script for a model-page PMM flow rather than an entirely off-page customizer.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([74832]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "file_upload_default_assets",
            "status": "supported",
            "introduced_in": "v0.8.0",
            "scope": "uploads",
            "syntax": ['yourFileName = "default.png";', 'yourFileName = "default.svg";', 'yourFileName = "default.stl";'],
            "constraints": [
                "The official release documents built-in default filenames rather than arbitrary file naming.",
                "Custom default files are not described as supported in the release note.",
            ],
            "rewrite_guidance": "Rewrite arbitrary uploaded asset names to PMM-supported defaults when building a PMM-safe script.",
            "agent_action": "Use default filenames for PMM upload parameters and explain the upload expectation to users.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([91853]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "parameterized_color_ui",
            "status": "supported",
            "introduced_in": "v0.9.0",
            "scope": "colors",
            "syntax": ['accent = "#FF0000"; // color'],
            "constraints": ["Parameterized colors are documented using hex string values with the `// color` comment."],
            "rewrite_guidance": "Convert user-facing color parameters to hex strings and add `// color` only where PMM UI exposure is intended.",
            "agent_action": "Prefer hex string parameters over non-parameterized literal color arrays for PMM UI controls.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([100160]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "font_picker_ui",
            "status": "supported",
            "introduced_in": "v0.10.0",
            "scope": "fonts",
            "syntax": ['font_name = "Roboto"; // font'],
            "constraints": ["The `// font` comment is required to enable the PMM font picker UI."],
            "rewrite_guidance": "If a model exposes fonts to PMM users, add a dedicated font-name parameter with the required comment marker.",
            "agent_action": "Do not assume a font parameter will become a PMM UI control unless `// font` is present.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "multi_plate_3mf",
            "status": "supported",
            "introduced_in": "v0.10.0",
            "scope": "export",
            "syntax": ["module mw_plate_1() { ... }", "module mw_plate_2() { ... }"],
            "constraints": [
                "Each printable plate uses an `mw_plate_N()` module.",
                "The official release warns that multi-plate scripts do not offer STL download from that script.",
            ],
            "rewrite_guidance": "Only choose multi-plate when the user actually benefits from a 3MF-first release strategy.",
            "agent_action": "Use PMM multi-plate modules for multi-part outputs and explain the STL tradeoff.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "assembly_view",
            "status": "supported",
            "introduced_in": "v0.10.0",
            "scope": "preview",
            "syntax": ["module mw_assembly_view() { ... }"],
            "constraints": ["The assembly view is documented as a preview aid and is not included in the exported 3MF."],
            "rewrite_guidance": "Use assembly view to improve comprehension for multi-part models without confusing it with printable geometry.",
            "agent_action": "Add `mw_assembly_view()` when users need a full-preview assembly, not as the only output definition.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "profile_configuration",
            "status": "supported",
            "introduced_in": "v0.10.0",
            "scope": "profiles",
            "syntax": [],
            "constraints": ["Only selected profile settings are documented as configurable and the upload action must persist the changes."],
            "rewrite_guidance": "Treat profile configuration as a PMM-side release concern rather than a pure OpenSCAD concern.",
            "agent_action": "Mention profile settings when layout or auto-arrange behavior matters.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "customizer_compatibility",
            "status": "partial",
            "introduced_in": "pre-v0.9",
            "scope": "compatibility",
            "syntax": [],
            "constraints": [
                "An employee said PMM mainly follows the OpenSCAD Customizer manual.",
                "Thingiverse-like preview comments were explicitly said to be unused by PMM itself.",
            ],
            "rewrite_guidance": "Model PMM parameter behavior after OpenSCAD Customizer first, and treat extra comment conventions as non-authoritative unless confirmed.",
            "agent_action": "Do not depend on `// preview[...]` or undocumented comment syntax as PMM functionality.",
            "source_class": "Employee-confirmed",
            "source_type": "discourse_json",
            "evidence_urls": evidence([77524]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "bundled_bosl2_library",
            "status": "supported",
            "introduced_in": "pre-v1.1.0",
            "scope": "libraries",
            "syntax": ["include <BOSL2/std.scad>;"],
            "constraints": [
                "PMM distinguishes between bundled platform libraries and arbitrary local include trees.",
                "MakerWorld's library inventory explicitly lists BOSL2 as a bundled library.",
                "The v1.1.0 PMM release also documented a BOSL2 backend revision.",
            ],
            "rewrite_guidance": "Do not strip or inline BOSL2 solely because local include trees are risky. First distinguish bundled PMM libraries from local project files.",
            "agent_action": "It is reasonable to keep BOSL2 includes when targeting PMM, while still checking for version-specific APIs and performance costs.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json",
                *evidence([203564, 150680]),
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "installed_fonts_inventory_endpoint",
            "status": "supported",
            "introduced_in": "fonts-0.8.0 endpoint",
            "scope": "fonts",
            "syntax": ['"Roboto"', '"Roboto:style=Bold"', '"Noto Sans JP"'],
            "constraints": [
                "MakerWorld exposes a direct JSON inventory of installed font names.",
                "This inventory is the best available source for exact font availability.",
            ],
            "rewrite_guidance": "When a model depends on fonts, validate against the endpoint-backed font inventory rather than guessing from UI screenshots or forum anecdotes.",
            "agent_action": "Use the MakerWorld font inventory as the primary source for exact PMM font availability and names.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-0.8.0.json"
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "font_catalog_endpoint",
            "status": "supported",
            "introduced_in": "fonts-show-0.0.1 asset",
            "scope": "fonts",
            "syntax": ['"AR One Sans"', '"Abyssinica SIL"', '"Noto Sans Arabic"'],
            "constraints": [
                "MakerWorld exposes a broader PMM font catalog endpoint that returns a `fontNames` list.",
                "This catalog is much larger than the smaller installed-font inventory and is useful for UI or multilingual discovery work.",
            ],
            "rewrite_guidance": "Use the broad catalog for font research, then validate must-have fonts against the installed runtime inventory before promising deterministic output.",
            "agent_action": "Check `fonts-show-0.0.1.json` when exploring PMM font availability, but keep `fonts-0.8.0.json` as the stricter runtime compatibility check.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-show-0.0.1.json"
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "language_to_font_family_map_asset",
            "status": "supported",
            "introduced_in": "language2family-0.0.1 asset",
            "scope": "fonts",
            "syntax": ["language2family-0.0.1.zip", "language_support_family_2.json"],
            "constraints": [
                "MakerWorld publishes a ZIP asset containing `language_support_family_2.json`.",
                "The JSON maps language-script identifiers to large font-family lists and is useful for multilingual font fallback research.",
            ],
            "rewrite_guidance": "When a PMM model needs broad language coverage, use the language-to-family map as a discovery aid before narrowing choices to installed or tested fonts.",
            "agent_action": "Use the language-support asset when selecting fallback families for multilingual text parameters.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_web_asset",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/language2family-0.0.1.zip"
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "backend_manifold_enabled",
            "status": "supported",
            "introduced_in": "2025-03-13",
            "scope": "backend",
            "syntax": [],
            "constraints": ["An employee explicitly stated that the PMM backend used commit `b550957ddac62e59428d08efa62e2f44c15a0b95` and manifold was enabled."],
            "rewrite_guidance": "If local and PMM behavior differ, account for a specific PMM backend revision rather than assuming the latest local OpenSCAD release.",
            "agent_action": "Document backend-version assumptions when diagnosing geometry or export discrepancies.",
            "source_class": "Employee-confirmed",
            "source_type": "discourse_json",
            "evidence_urls": evidence([150680]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "backend_refresh_v1_1_0",
            "status": "supported",
            "introduced_in": "v1.1.0",
            "scope": "backend",
            "syntax": [],
            "constraints": [
                "The OpenSCAD-backed PMM workflow moved the code editor behind a Code button.",
                "The release documented an OpenSCAD backend based on commit `c8fbef05ba900e46892e9a44ea05f7d88e576e13` and BOSL2 commit `99fcfc6867e739aa1cd8ffc49fe39276036681f1`.",
            ],
            "rewrite_guidance": "Use these documented revisions when explaining environment differences or library behavior.",
            "agent_action": "Account for the documented backend and BOSL2 revisions when troubleshooting reproducibility.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([203564]),
            "manual_capture_refs": [],
        },
    ]


def build_compatibility_rules(topic_map: dict[int, dict]) -> list[dict]:
    def evidence(topic_ids: list[int]) -> list[str]:
        return [topic_map[topic_id]["url"] for topic_id in topic_ids if topic_id in topic_map]

    return [
        {
            "feature_key": "avoid_arbitrary_local_includes",
            "status": "caution",
            "introduced_in": "2025-03-13",
            "scope": "includes",
            "syntax": ["include <local_file.scad>;"],
            "constraints": ["Local include trees are not a safe PMM default unless the library is known to exist in PMM."],
            "rewrite_guidance": "Flatten local dependencies or inline the minimum needed helpers into a PMM-safe file.",
            "agent_action": "Treat local include graphs as migration work, not drop-in PMM behavior.",
            "source_class": "Employee-confirmed",
            "source_type": "discourse_json",
            "evidence_urls": evidence([150680]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "distinguish_bundled_bosl2_from_local_includes",
            "status": "supported",
            "introduced_in": "v1.1.0",
            "scope": "libraries",
            "syntax": ["include <BOSL2/std.scad>;"],
            "constraints": [
                "Bundled PMM libraries such as BOSL2 are a different case from arbitrary local project includes.",
                "MakerWorld's library inventory explicitly lists BOSL2 as bundled.",
                "Bambu also documented a specific BOSL2 revision in the v1.1.0 PMM release.",
            ],
            "rewrite_guidance": "Keep BOSL2 when it is actually helping the model; only flatten or remove dependencies that are not part of PMM's bundled environment.",
            "agent_action": "Do not conclude that PMM cannot use BOSL2 just because PMM has trouble with arbitrary local include trees.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/libraries-0.8.0.json",
                *evidence([203564, 150680]),
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "require_default_asset_names",
            "status": "supported",
            "introduced_in": "v0.8.0",
            "scope": "uploads",
            "syntax": ['"default.png"', '"default.svg"', '"default.stl"'],
            "constraints": ["PMM upload features are documented around built-in default filenames."],
            "rewrite_guidance": "Rename or rewire uploaded asset variables to match documented PMM defaults.",
            "agent_action": "Avoid arbitrary uploaded asset names in PMM-targeted scripts.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([91853]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "hex_string_color_only_for_ui",
            "status": "supported",
            "introduced_in": "v0.9.0",
            "scope": "colors",
            "syntax": ['accent_hex = "#FF0000"; // color'],
            "constraints": ["Parameterized color UI is documented for hex strings rather than arbitrary color expressions."],
            "rewrite_guidance": "Expose PMM color controls as hex string parameters and keep more complex color logic internal if needed.",
            "agent_action": "Use simple hex-string parameters for PMM-exposed colors.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([100160]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "font_comment_required",
            "status": "supported",
            "introduced_in": "v0.10.0",
            "scope": "fonts",
            "syntax": ['font_name = "Roboto"; // font'],
            "constraints": ["The PMM font UI requires the `// font` marker."],
            "rewrite_guidance": "Add `// font` only to parameters intended for PMM font selection.",
            "agent_action": "Do not assume plain OpenSCAD font strings become PMM font controls automatically.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "validate_fonts_against_installed_inventory",
            "status": "caution",
            "introduced_in": "fonts-show-0.0.1 asset",
            "scope": "fonts",
            "syntax": ['font_name = "Some Font"; // font'],
            "constraints": [
                "MakerWorld exposes both a broad PMM font catalog and a smaller installed-font inventory.",
                "A font being visible in the broad catalog does not by itself prove it is part of the smaller runtime inventory you want to target deterministically.",
            ],
            "rewrite_guidance": "When a font is essential to geometry or layout, validate it against the installed inventory rather than relying only on the broader display catalog.",
            "agent_action": "Treat `fonts-show-0.0.1.json` as discovery data and `fonts-0.8.0.json` as the stricter runtime check.",
            "source_class": "Official app endpoint",
            "source_type": "makerworld_json",
            "evidence_urls": [
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-show-0.0.1.json",
                "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/fonts-0.8.0.json",
            ],
            "manual_capture_refs": [],
        },
        {
            "feature_key": "multi_plate_stl_tradeoff",
            "status": "caution",
            "introduced_in": "v0.10.0",
            "scope": "export",
            "syntax": ["module mw_plate_1() { ... }"],
            "constraints": ["The official release notes that multi-plate scripts cannot provide STL download from that script."],
            "rewrite_guidance": "Consider separate release variants when both PMM multi-plate output and STL convenience matter.",
            "agent_action": "Present multi-plate as a product decision, not only a code implementation detail.",
            "source_class": "Official release",
            "source_type": "discourse_json",
            "evidence_urls": evidence([144618]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "oversize_auto_arrange_risk",
            "status": "caution",
            "introduced_in": "2025-01-19",
            "scope": "layout",
            "syntax": [],
            "constraints": [
                "Oversize models may fail 3MF generation.",
                "Employee replies connect this to auto-arrange behavior and practical plate limits.",
            ],
            "rewrite_guidance": "Split large output into multiple plates or document profile-setting expectations when a model approaches layout limits.",
            "agent_action": "Flag oversize and auto-arrange risk in the upload plan.",
            "source_class": "Employee-confirmed",
            "source_type": "discourse_json",
            "evidence_urls": evidence([133844, 144618, 172901]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "preview_comments_not_supported_feature",
            "status": "unsupported",
            "introduced_in": "2024-05-28",
            "scope": "comments",
            "syntax": ["// preview[...]"],
            "constraints": ["An employee explicitly said the preview comment example was not used by PMM itself."],
            "rewrite_guidance": "Remove or ignore preview-comment reliance when porting a script to PMM.",
            "agent_action": "Do not spend effort preserving preview-comment behavior as if it were a PMM feature.",
            "source_class": "Employee-confirmed",
            "source_type": "discourse_json",
            "evidence_urls": evidence([77524]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "uploaded_stl_name_is_fragile",
            "status": "caution",
            "introduced_in": "2026-04-08",
            "scope": "uploads",
            "syntax": ['import("oven_knob_solid.stl");'],
            "constraints": ["Community evidence suggests PMM STL-backed workflows are safer when aligned with the documented `default.stl` pattern."],
            "rewrite_guidance": "Prefer the official default-file convention over arbitrary co-uploaded STL naming assumptions.",
            "agent_action": "Treat arbitrary uploaded STL filenames as risky unless separately confirmed by current PMM behavior.",
            "source_class": "Community-discovered",
            "source_type": "discourse_json",
            "evidence_urls": evidence([247687, 91853]),
            "manual_capture_refs": [],
        },
        {
            "feature_key": "avoid_direct_special_module_calls",
            "status": "caution",
            "introduced_in": "2025-11-25",
            "scope": "multi-plate",
            "syntax": ["mw_plate_1();", "mw_assembly_view();"],
            "constraints": ["Community troubleshooting suggests special PMM modules should define output rather than be treated as ordinary helper calls."],
            "rewrite_guidance": "Keep reusable geometry in neutral helper modules and reserve PMM-specific modules for output structure.",
            "agent_action": "Do not build the whole model around directly calling PMM special modules as ordinary functions.",
            "source_class": "Community-discovered",
            "source_type": "discourse_json",
            "evidence_urls": evidence([211145]),
            "manual_capture_refs": [],
        },
    ]


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    topic_index, topic_map = build_topic_index()
    source_index = build_source_index()
    feature_index = build_feature_index(topic_map)
    compatibility_rules = build_compatibility_rules(topic_map)

    write_json(DATA_DIR / "topic-index.json", topic_index)
    write_json(DATA_DIR / "source-index.json", source_index)
    write_json(DATA_DIR / "feature-index.json", feature_index)
    write_json(DATA_DIR / "compatibility-rules.json", compatibility_rules)


if __name__ == "__main__":
    main()
