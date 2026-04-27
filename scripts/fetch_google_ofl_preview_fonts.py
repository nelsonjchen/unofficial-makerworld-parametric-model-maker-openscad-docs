#!/usr/bin/env python3
"""Fetch clean Google Fonts repo files used for self-hosted PMM previews."""

from __future__ import annotations

import urllib.request
from pathlib import Path
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / "docs" / "assets" / "vendor-fonts" / "google-ofl"
RAW_ROOT = "https://raw.githubusercontent.com/google/fonts/main/ofl"


FONT_SOURCES = {
    "aksarabaligalang": {
        "family": "Aksara Bali Galang",
        "files": [("AksaraBaliGalang-Regular.ttf", 400, "normal")],
    },
    "alumnisanscollegiateonesc": {
        "family": "Alumni Sans Collegiate One SC",
        "files": [
            ("AlumniSansCollegiateOneSC-Regular.ttf", 400, "normal"),
            ("AlumniSansCollegiateOneSC-Italic.ttf", 400, "italic"),
        ],
    },
    "amstelvaralpha": {
        "family": "AmstelvarAlpha",
        "files": [("AmstelvarAlpha-VF.ttf", "100 900", "normal")],
    },
    "bhavuka": {
        "family": "Bhavuka",
        "files": [("Bhavuka-Regular.ttf", 400, "normal")],
    },
    "bigshouldersdisplaysc": {
        "family": "Big Shoulders Display SC",
        "files": [("BigShouldersDisplaySC[wght].ttf", "100 900", "normal")],
    },
    "bigshouldersinlinedisplaysc": {
        "family": "Big Shoulders Inline Display SC",
        "files": [("BigShouldersInlineDisplaySC[wght].ttf", "100 900", "normal")],
    },
    "bigshouldersinlinetextsc": {
        "family": "Big Shoulders Inline Text SC",
        "files": [("BigShouldersInlineTextSC[wght].ttf", "100 900", "normal")],
    },
    "bigshouldersstencildisplaysc": {
        "family": "Big Shoulders Stencil Display SC",
        "files": [("BigShouldersStencilDisplaySC[wght].ttf", "100 900", "normal")],
    },
    "bigshouldersstenciltextsc": {
        "family": "Big Shoulders Stencil Text SC",
        "files": [("BigShouldersStencilTextSC[wght].ttf", "100 900", "normal")],
    },
    "bigshoulderstextsc": {
        "family": "Big Shoulders Text SC",
        "files": [("BigShouldersTextSC[wght].ttf", "100 900", "normal")],
    },
    "bungeecolor": {
        "family": "Bungee Color",
        "files": [("BungeeColor-Regular.ttf", 400, "normal")],
    },
    "decovaralpha": {
        "family": "Decovar Alpha",
        "files": [("DecovarAlpha-VF.ttf", "100 900", "normal")],
    },
    "fragmentmonosc": {
        "family": "Fragment Mono SC",
        "files": [
            ("FragmentMonoSC-Regular.ttf", 400, "normal"),
            ("FragmentMonoSC-Italic.ttf", 400, "italic"),
        ],
    },
    "hanna": {
        "family": "Hanna",
        "files": [("BM-HANNA.ttf", 400, "normal")],
    },
    "hannari": {
        "family": "Hannari",
        "files": [("Hannari-Regular.ttf", 400, "normal")],
    },
    "hermeneusone": {
        "family": "Hermeneus One",
        "files": [("HermeneusOne-Regular.ttf", 400, "normal")],
    },
    "hindcolombo": {
        "family": "Hind Colombo",
        "files": [
            ("HindColombo-Light.ttf", 300, "normal"),
            ("HindColombo-Regular.ttf", 400, "normal"),
            ("HindColombo-Medium.ttf", 500, "normal"),
            ("HindColombo-SemiBold.ttf", 600, "normal"),
            ("HindColombo-Bold.ttf", 700, "normal"),
        ],
    },
    "hindjalandhar": {
        "family": "Hind Jalandhar",
        "files": [
            ("HindJalandhar-Light.ttf", 300, "normal"),
            ("HindJalandhar-Regular.ttf", 400, "normal"),
            ("HindJalandhar-Medium.ttf", 500, "normal"),
            ("HindJalandhar-SemiBold.ttf", 600, "normal"),
            ("HindJalandhar-Bold.ttf", 700, "normal"),
        ],
    },
    "hindkochi": {
        "family": "Hind Kochi",
        "files": [
            ("HindKochi-Light.ttf", 300, "normal"),
            ("HindKochi-Regular.ttf", 400, "normal"),
            ("HindKochi-Medium.ttf", 500, "normal"),
            ("HindKochi-SemiBold.ttf", 600, "normal"),
            ("HindKochi-Bold.ttf", 700, "normal"),
        ],
    },
    "kokoro": {
        "family": "Kokoro",
        "files": [("Kokoro-Regular.ttf", 400, "normal")],
    },
    "molle": {
        "family": "Molle",
        "files": [("Molle-Regular.ttf", 400, "normal")],
    },
    "nicomoji": {
        "family": "Nico Moji",
        "files": [("NicoMoji-Regular.ttf", 400, "normal")],
    },
    "nikukyu": {
        "family": "Nikukyu",
        "files": [("Nikukyu-Regular.ttf", 400, "normal")],
    },
    "signikanegativesc": {
        "family": "Signika Negative SC",
        "files": [
            ("SignikaNegativeSC-Light.ttf", 300, "normal"),
            ("SignikaNegativeSC-Regular.ttf", 400, "normal"),
            ("SignikaNegativeSC-SemiBold.ttf", 600, "normal"),
            ("SignikaNegativeSC-Bold.ttf", 700, "normal"),
        ],
    },
    "signikasc": {
        "family": "Signika SC",
        "files": [("SignikaSC[wght].ttf", "300 700", "normal")],
    },
    "sunflower": {
        "family": "Sunflower",
        "files": [
            ("Sunflower-Light.ttf", 300, "normal"),
            ("Sunflower-Medium.ttf", 500, "normal"),
            ("Sunflower-Bold.ttf", 700, "normal"),
        ],
    },
    "tharlon": {
        "family": "TharLon",
        "files": [("Tharlon-Regular.ttf", 400, "normal")],
    },
}


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size:
        return
    with urllib.request.urlopen(url, timeout=45) as response:
        path.write_bytes(response.read())


def css_for(slug: str, config: dict) -> str:
    blocks = [
        "/* Google Fonts repo preview files. Source font files are SIL OFL; see OFL.txt in this directory. */"
    ]
    family = config["family"]
    for filename, weight, style in config["files"]:
        blocks.append(
            "\n".join(
                [
                    "@font-face {",
                    f'  font-family: "{family}";',
                    f'  src: url("{filename}") format("truetype");',
                    f"  font-weight: {weight};",
                    f"  font-style: {style};",
                    "  font-display: swap;",
                    "}",
                ]
            )
        )
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    for slug, config in FONT_SOURCES.items():
        out_dir = OUT_ROOT / slug
        for filename, _weight, _style in config["files"]:
            url = f"{RAW_ROOT}/{slug}/{quote(filename)}"
            download(url, out_dir / filename)
        download(f"{RAW_ROOT}/{slug}/OFL.txt", out_dir / "OFL.txt")
        (out_dir / f"{slug}.css").write_text(css_for(slug, config), encoding="utf-8")


if __name__ == "__main__":
    main()
