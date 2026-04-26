#!/usr/bin/env python3
"""Build PMM font indexes and the generated font reference pages."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote_plus


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "sources" / "raw" / "makerworld"
DATA_DIR = REPO_ROOT / "data"
DOCS_DIR = REPO_ROOT / "docs"
ASSET_DIR = DOCS_DIR / "assets"

INSTALLED_PATH = RAW_DIR / "fonts-0.8.0.json"
BROAD_PATH = RAW_DIR / "fonts-show-0.0.1.json"
METADATA_PATH = RAW_DIR / "fonts-0.9.0.json"

PMM_FILTER_KEYS = {
    "Expressive": "Feeling",
    "Theme": "Appearance",
    "Script": "Calligraphy",
    "Serif": "Serif",
    "Sans": "Sans Serif",
    "Seasonal": "Seasonal",
}

GOOGLE_CSS_BAD_FAMILIES = {
    "Abhaya Libre ExtraBold",
    "Abhaya Libre Medium",
    "Abhaya Libre SemiBold",
    "Aksara Bali Galang",
    "Aldo",
    "Alumni Sans Collegiate One SC",
    "AmstelvarAlpha",
    "Asap Black",
    "Asap Extra",
    "Asap ExtraLight",
    "Asap Light",
    "Asap Medium",
    "Asap Semi",
    "BM HANNA_TTF",
    "Batang",
    "BatangChe",
    "Bhavuka",
    "Big Shoulders Display SC",
    "Big Shoulders Inline Display SC",
    "Big Shoulders Inline Text SC",
    "Big Shoulders Stencil Display SC",
    "Big Shoulders Stencil Text SC",
    "Big Shoulders Text SC",
    "Buda",
    "Bungee Color",
    "Decovar Alpha",
    "Decovar Alpha Regular24",
    "Digital Numbers",
    "DotumChe",
    "Encode Sans Condensed Thin",
    "Encode Sans SC Condensed Thin",
    "Fjord",
    "Fragment Mono SC",
    "GulimChe",
    "Gungsuh",
    "GungsuhChe",
    "Hannari",
    "HarmonyOS Sans SC",
    "HeadlandOne",
    "Hermeneus One",
    "Hind Colombo",
    "Hind Jalandhar",
    "Hind Kochi",
    "IM FELL DW Pica",
    "IM FELL DW Pica SC",
    "IM FELL Double Pica",
    "IM FELL Double Pica SC",
    "IM FELL English",
    "IM FELL English SC",
    "IM FELL French Canon",
    "IM FELL French Canon SC",
    "IM FELL Great Primer",
    "IM FELL Great Primer SC",
    "JejuGothic",
    "JejuHallasan",
    "JejuMyeongjo",
    "KoPub Batang",
    "Kokoro",
    "Komikazoom",
    "Liberation Sans",
    "Ligconsolata",
    "Maven Pro VF Beta",
    "Merge One",
    "Mervale Script",
    "Miama",
    "Molle",
    "Myanmar Khyay",
    "Myanmar Sans Pro",
    "NATS",
    "Nanum Pen",
    "NanumGothic",
    "NanumGothicCoding",
    "NanumMyeongjo",
    "Nico Moji",
    "Nikukyu",
    "Norwester",
    "Noto Color Emoji Compat Test",
    "Noto Serif Hmong Nyiakeng",
    "NovaMono",
    "Open Sans Condensed",
    "Open Sans Hebrew",
    "Open Sans Hebrew Condensed",
    "Podkova VF Beta",
    "PoetsenOne",
    "Porter Sans Block",
    "Rounded Mplus 1c Bold",
    "Saira ExtraCondensed",
    "Saira SemiCondensed",
    "Sansation Light",
    "Signika Negative SC",
    "Signika SC",
    "SirinStencil",
    "Sitara",
    "Souliyo Unicode",
    "Space Grotesk Light",
    "Strong",
    "Sunflower",
    "Supermercado",
    "TharLon",
    "UnifrakturCook",
    "Yaldevi Colombo",
    "Yaldevi Colombo ExtraLight",
    "Yaldevi Colombo Light",
    "Yaldevi Colombo Medium",
    "Yaldevi Colombo SemiBold",
    "Yinmar",
}

ALIAS_OVERRIDES = {
    "HeadlandOne": "Headland One",
    "IM FELL DW Pica": "IM Fell DW Pica",
    "IM FELL DW Pica SC": "IM Fell DW Pica SC",
    "IM FELL Double Pica": "IM Fell Double Pica",
    "IM FELL Double Pica SC": "IM Fell Double Pica SC",
    "IM FELL English": "IM Fell English",
    "IM FELL English SC": "IM Fell English SC",
    "IM FELL French Canon": "IM Fell French Canon",
    "IM FELL French Canon SC": "IM Fell French Canon SC",
    "IM FELL Great Primer": "IM Fell Great Primer",
    "IM FELL Great Primer SC": "IM Fell Great Primer SC",
    "Nanum Pen": "Nanum Pen Script",
    "NanumGothic": "Nanum Gothic",
    "NanumGothicCoding": "Nanum Gothic Coding",
    "NanumMyeongjo": "Nanum Myeongjo",
    "NovaMono": "Nova Mono",
    "PoetsenOne": "Poetsen One",
    "Saira ExtraCondensed": "Saira Extra Condensed",
    "Saira SemiCondensed": "Saira Semi Condensed",
    "SirinStencil": "Sirin Stencil",
}

FONT_OVERRIDES = {
    "Aldo": {
        "license_confidence": "conflicting",
        "preview_status": "fallback-only",
        "preview_family": None,
        "license_summary": "Likely Sacha Rein/Trypo Aldo SemiBold. Public sources are not cleanly redistributable; do not self-host font files.",
        "evidence_urls": [
            "https://www.dafont.com/aldo.font",
            "https://www.dafont.com/faq.php",
            "https://sacharein.com/aldopro",
            "https://www.myfonts.com/collections/aldo-pro-font-sacha-rein?tab=licensing",
            "https://www.fonts4free.net/aldo-font.html",
        ],
    },
    "HarmonyOS Sans SC": {
        "license_confidence": "restricted-redistribution",
        "preview_status": "self-hosted-preview",
        "preview_family": "HarmonyOS Sans SC",
        "font_css_url": "vendor-fonts/harmonyos-sans-sc/harmonyos-sans-sc.css",
        "fallback_stack": "Noto Sans SC, Source Han Sans SC, PingFang SC, Microsoft YaHei, sans-serif",
        "license_summary": "Self-hosted preview. Redistribution terms require care; see the linked license sources.",
        "evidence_urls": [
            "https://github.com/huawei-fonts/HarmonyOS-Sans",
            "https://github.com/ajacocks/harmonyos-sans-font/blob/main/LICENSE",
            "https://developer.huawei.com/consumer/cn/design/resource-V1/",
            "https://developer.huawei.com/images/download/general/HarmonyOS-Sans.zip",
            "https://gitee.com/openharmony/utils_system_resources/blob/master/LICENSE_Fonts",
            "https://gitee.com/openharmony/global_system_resources/blob/master/README.md",
        ],
    },
    "Komikazoom": {
        "license_confidence": "custom-license",
        "preview_status": "external-preview",
        "preview_family": None,
        "license_summary": "Apostrophic Labs freeware permits use, including commercial use, but converted or repackaged self-hosted webfonts are not cleanly authorized.",
        "evidence_urls": [
            "https://www.1001fonts.com/komikazoom-font.html",
            "https://st.1001fonts.net/license/komikazoom/readme.txt",
            "https://web.archive.org/web/20030408055445/www.hardcovermedia.com/lab/Pages/info.html",
            "https://fontzillion.com/fonts/apostrophic-labs/komikazoom",
            "https://www.fontget.com/font/komikazoom/",
        ],
    },
    "Liberation Sans": {
        "license_confidence": "clean",
        "preview_status": "fallback-only",
        "preview_family": None,
        "license_summary": "Official Liberation Fonts repository identifies the family as SIL OFL. It is PMM-installed but not served by Google Fonts CSS.",
        "evidence_urls": ["https://github.com/liberationfonts/liberation-fonts"],
    },
    "Norwester": {
        "license_confidence": "clean",
        "preview_status": "fallback-only",
        "preview_family": None,
        "license_summary": "Font Squirrel lists Norwester under SIL OFL. The docs site does not bundle the font file.",
        "evidence_urls": ["https://www.fontsquirrel.com/license/norwester"],
    },
    "Nanum Pen": {
        "license_confidence": "likely-clean",
        "preview_status": "google-css",
        "preview_family": "Nanum Pen Script",
        "license_summary": "PMM name appears to map to NAVER Nanum Pen / Nanum Pen Script; NAVER documents Nanum fonts under SIL OFL.",
        "evidence_urls": [
            "https://help.naver.com/support/contents/contents.help?categoryNo=3497&serviceNo=1074",
            "https://fonts.adobe.com/fonts/nanum-pen-script",
        ],
    },
    "PoetsenOne": {
        "license_confidence": "clean",
        "preview_status": "google-css",
        "preview_family": "Poetsen One",
        "license_summary": "PMM uses the compact legacy name; public sources identify Poetsen One as SIL OFL.",
        "evidence_urls": ["https://online-fonts.com/fonts/poetsenone"],
    },
    "Strong": {
        "license_confidence": "likely-clean",
        "preview_status": "fallback-only",
        "preview_family": None,
        "license_summary": "PMM render appears to match the Gaslight/Cyreal Strong Regular font. Public font metadata identifies it as SIL OFL with Reserved Font Name Strong.",
        "evidence_urls": [
            "https://www.fontmirror.com/strong",
            "https://online-fonts.com/fonts/strong",
            "https://www.figma.com/fonts/strong/",
            "https://www.wfonts.com/font/strong",
        ],
    },
    "Open Sans Condensed": {
        "license_confidence": "clean",
        "preview_status": "google-css",
        "preview_family": "Open Sans",
        "license_summary": "Legacy PMM family name; preview uses modern Open Sans with width styling where the browser supports it.",
        "evidence_urls": [
            "https://github.com/googlefonts/opensans",
            "https://fontsource.org/fonts/open-sans",
        ],
    },
    "Open Sans Hebrew": {
        "license_confidence": "clean",
        "preview_status": "google-css",
        "preview_family": "Open Sans",
        "license_summary": "Legacy PMM family name; modern Open Sans includes Hebrew support.",
        "evidence_urls": [
            "https://github.com/googlefonts/opensans",
            "https://fontsource.org/fonts/open-sans",
        ],
    },
    "Open Sans Hebrew Condensed": {
        "license_confidence": "clean",
        "preview_status": "google-css",
        "preview_family": "Open Sans",
        "license_summary": "Legacy PMM family name; preview uses modern Open Sans best-effort rather than a self-hosted legacy Hebrew Condensed file.",
        "evidence_urls": [
            "https://github.com/googlefonts/opensans",
            "https://fontsource.org/fonts/open-sans",
        ],
    },
}

WEIGHT_BY_STYLE = {
    "Thin": 100,
    "ExtraLight": 200,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
    "ExtraBold": 800,
    "Black": 900,
    "ExtraBlack": 950,
}

LICENSE_LABELS = {
    "clean": "Clean",
    "likely-clean": "Likely clean",
    "custom-license": "Custom license",
    "restricted-redistribution": "Restricted redistribution",
    "conflicting": "Conflicting",
    "unknown": "Unknown",
}


def load_font_names(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("fontNames", [])


def load_font_metadata() -> dict[str, dict]:
    if not METADATA_PATH.exists():
        return {}
    payload = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    metadata = {}
    for item in payload.get("familyMetadataList", []):
        family = item.get("family")
        if family:
            metadata[family] = item
    return metadata


def metadata_for_family(family: str, metadata: dict[str, dict]) -> dict | None:
    return metadata.get(family) or metadata.get(ALIAS_OVERRIDES.get(family, ""))


def compact_metadata(item: dict | None) -> dict:
    if not item:
        return {
            "source": "missing",
            "category": None,
            "stroke": None,
            "subsets": [],
            "filters": {key: [] for key in PMM_FILTER_KEYS},
        }
    return {
        "source": "fonts-0.9.0",
        "category": item.get("category"),
        "stroke": item.get("stroke"),
        "subsets": [subset for subset in item.get("subsets", []) if subset != "menu"],
        "primary_script": item.get("primaryScript") or "",
        "primary_language": item.get("primaryLanguage") or "",
        "is_noto": bool(item.get("isNoto")),
        "is_open_source": item.get("isOpenSource"),
        "filters": {key: sorted(set(item.get(key, []))) for key in PMM_FILTER_KEYS},
    }


def split_font_name(raw_name: str) -> tuple[str, str]:
    if ":style=" not in raw_name:
        return raw_name, "Regular"
    family, style = raw_name.split(":style=", 1)
    return family, style or "Regular"


def style_to_weight(style: str) -> int | None:
    normalized = style.replace(" Italic", "").replace("Italic", "").strip()
    for token in ("Condensed", "ExtraCondensed", "SemiCondensed", "12pt", "20pt"):
        normalized = normalized.replace(token, "").strip()
    normalized = re.sub(r"\s+", " ", normalized)
    if not normalized:
        normalized = "Regular"
    return WEIGHT_BY_STYLE.get(normalized)


def is_italic(style: str) -> bool:
    return "Italic" in style


def google_css_url(family: str) -> str:
    return f"https://fonts.googleapis.com/css2?family={quote_plus(family)}&display=swap"


def font_css_url(preview: dict, preview_family: str | None) -> str | None:
    if preview.get("font_css_url"):
        return preview["font_css_url"]
    if preview["preview_status"] == "google-css" and preview_family:
        return google_css_url(preview_family)
    return None


def default_preview_for_family(family: str) -> dict:
    alias = ALIAS_OVERRIDES.get(family)
    if alias:
        return {
            "preview_status": "google-css",
            "preview_family": alias,
            "license_confidence": "likely-clean",
            "license_summary": "Preview uses a verified naming alias for the PMM-listed family.",
            "evidence_urls": [],
        }
    if family in GOOGLE_CSS_BAD_FAMILIES:
        return {
            "preview_status": "fallback-only",
            "preview_family": None,
            "license_confidence": "unknown",
            "license_summary": "No direct Google Fonts CSS preview was confirmed for this PMM-listed family.",
            "evidence_urls": [],
        }
    return {
        "preview_status": "google-css",
        "preview_family": family,
        "license_confidence": "clean",
        "license_summary": "Preview is loaded from Google Fonts CSS; exact PMM runtime behavior still comes from MakerWorld.",
        "evidence_urls": ["https://developers.google.com/fonts/faq"],
    }


def build_records() -> tuple[list[dict], dict, dict]:
    installed = load_font_names(INSTALLED_PATH)
    broad = load_font_names(BROAD_PATH)
    metadata = load_font_metadata()
    installed_set = set(installed)
    broad_set = set(broad)
    all_names = sorted(installed_set | broad_set)

    records = []
    family_records = defaultdict(list)
    for idx, raw_name in enumerate(all_names, start=1):
        family, style = split_font_name(raw_name)
        pmm_metadata = compact_metadata(metadata_for_family(family, metadata))
        preview = default_preview_for_family(family)
        preview.update(FONT_OVERRIDES.get(family, {}))
        preview_family = preview.get("preview_family")
        local_font_css_url = font_css_url(preview, preview_family)
        record = {
            "id": f"font-{idx}",
            "pmm_name": raw_name,
            "family": family,
            "style": style,
            "weight": style_to_weight(style),
            "italic": is_italic(style),
            "in_installed_inventory": raw_name in installed_set,
            "in_broad_catalog": raw_name in broad_set,
            "source_inventories": [
                label
                for label, present in (
                    ("installed-runtime", raw_name in installed_set),
                    ("broad-catalog", raw_name in broad_set),
                )
                if present
            ],
            "preview_status": preview["preview_status"],
            "preview_family": preview_family,
            "google_css_url": google_css_url(preview_family) if preview["preview_status"] == "google-css" and preview_family else None,
            "fallback_stack": preview.get("fallback_stack", "system-ui, sans-serif"),
            "license_confidence": preview["license_confidence"],
            "license_summary": preview["license_summary"],
            "evidence_urls": preview["evidence_urls"],
            "pmm_metadata": pmm_metadata,
        }
        if local_font_css_url and preview["preview_status"] != "google-css":
            record["font_css_url"] = local_font_css_url
        records.append(record)
        family_records[family].append(record)

    pmm_filter_options = {
        key: sorted({
            value
            for item in metadata.values()
            for value in item.get(key, [])
        })
        for key in PMM_FILTER_KEYS
    }
    pmm_filter_options["subsets"] = sorted({
        subset
        for item in metadata.values()
        for subset in item.get("subsets", [])
        if subset != "menu"
    })

    summary = {
        "installed_entry_count": len(installed),
        "installed_family_count": len({split_font_name(name)[0] for name in installed}),
        "broad_entry_count": len(broad),
        "broad_family_count": len({split_font_name(name)[0] for name in broad}),
        "combined_entry_count": len(records),
        "combined_family_count": len(family_records),
        "preview_status_counts": dict(Counter(record["preview_status"] for record in records)),
        "license_confidence_counts": dict(Counter(record["license_confidence"] for record in records)),
        "pmm_metadata_family_count": len(metadata),
        "pmm_metadata_matched_family_count": len({
            record["family"]
            for record in records
            if record["pmm_metadata"]["source"] != "missing"
        }),
    }
    return records, summary, pmm_filter_options


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_font_index_page(summary: dict) -> None:
    lines = [
        "# PMM Font Index",
        "",
        f"Browse `{summary['combined_family_count']}` MakerWorld PMM font families and `{summary['combined_entry_count']}` exact PMM font strings. The browser is family-first: select a family to inspect styles, exact OpenSCAD names, PMM font-dialog filter metadata, preview aliases, and provenance warnings. See [font provenance notes](font-provenance-notes.md) for licensing caveats and source evidence.",
        "",
        '<div id="pmm-font-index" class="pmm-font-index">',
        '  <p class="pmm-font-index__loading">Loading generated font index...</p>',
        "</div>",
        "",
        '<link rel="stylesheet" href="../assets/font-index.css">',
        '<script src="../assets/font-index.js"></script>',
    ]
    (DOCS_DIR / "font-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_provenance_page(records: list[dict], summary: dict) -> None:
    families = {}
    for record in records:
        if record["license_confidence"] in {"clean", "unknown"} and record["preview_status"] == "google-css":
            continue
        existing = families.setdefault(
            record["family"],
            {
                "family": record["family"],
                "license_confidence": record["license_confidence"],
                "preview_status": record["preview_status"],
                "license_summary": record["license_summary"],
                "preview_family": record["preview_family"],
                "evidence_urls": record["evidence_urls"],
                "installed": False,
                "broad": False,
                "styles": set(),
            },
        )
        existing["installed"] = existing["installed"] or record["in_installed_inventory"]
        existing["broad"] = existing["broad"] or record["in_broad_catalog"]
        existing["styles"].add(record["style"])

    lines = [
        "# Font Provenance Notes",
        "",
        "This generated page records font families where previewing, naming, or redistribution needs extra context.",
        "",
        "The site does not redistribute questionable font software. When a family is not cleanly previewable from a public webfont source, the font index uses fallback rendering and links to source evidence.",
        "",
        "## Confidence Labels",
        "",
    ]
    for key, label in LICENSE_LABELS.items():
        lines.append(f"- `{key}`: {label}.")
    lines.extend(["", "## Families With Caveats", ""])
    for family in sorted(families):
        item = families[family]
        inventories = []
        if item["installed"]:
            inventories.append("installed runtime")
        if item["broad"]:
            inventories.append("broad catalog")
        lines.append(f"### {family}")
        lines.append("")
        lines.append(f"- Inventory: {', '.join(inventories)}")
        lines.append(f"- License confidence: `{item['license_confidence']}`")
        lines.append(f"- Preview status: `{item['preview_status']}`")
        if item["preview_family"]:
            lines.append(f"- Preview family or alias: `{item['preview_family']}`")
        lines.append(f"- Note: {item['license_summary']}")
        style_sample = sorted(item["styles"])[:12]
        lines.append(f"- Styles observed: {', '.join(f'`{style}`' for style in style_sample)}")
        if len(item["styles"]) > len(style_sample):
            lines.append(f"- Additional styles: `{len(item['styles']) - len(style_sample)}`")
        if item["evidence_urls"]:
            lines.append("- Evidence:")
            for url in item["evidence_urls"]:
                lines.append(f"  - {url}")
        lines.append("")
    lines.extend(
        [
            "## Generated Summary",
            "",
            f"- Preview statuses: `{summary['preview_status_counts']}`",
            f"- License confidence labels: `{summary['license_confidence_counts']}`",
        ]
    )
    (DOCS_DIR / "font-provenance-notes.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def preview_record(record: dict) -> dict:
    item = {
        "family": record["family"],
        "preview_status": record["preview_status"],
        "preview_family": record["preview_family"],
        "google_css_url": record["google_css_url"],
        "license_confidence": record["license_confidence"],
        "license_summary": record["license_summary"],
        "evidence_urls": record["evidence_urls"],
    }
    if record.get("font_css_url"):
        item["font_css_url"] = record["font_css_url"]
    return item


def main() -> None:
    records, summary, pmm_filter_options = build_records()
    preview_records = [preview_record(record) for record in records]

    payload = {
        "summary": summary,
        "pmm_filter_labels": PMM_FILTER_KEYS,
        "pmm_filter_options": pmm_filter_options,
        "fonts": records,
    }
    write_json(DATA_DIR / "font-index.json", payload)
    write_json(DATA_DIR / "font-preview-index.json", {"summary": summary, "previews": preview_records})
    write_json(ASSET_DIR / "font-index-data.json", payload)
    write_font_index_page(summary)
    write_provenance_page(records, summary)


if __name__ == "__main__":
    main()
