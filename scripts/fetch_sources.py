#!/usr/bin/env python3
"""Fetch public Discourse JSON snapshots for known PMM-relevant topics."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "sources" / "raw" / "discourse"
MAKERWORLD_RAW_DIR = REPO_ROOT / "sources" / "raw" / "makerworld"
BASE_URL = "https://forum.bambulab.com"
MAKERWORLD_BASE = "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

TOPICS = [
    74832,
    75758,
    77524,
    91853,
    100160,
    128380,
    133844,
    142549,
    144618,
    150680,
    154198,
    156334,
    172894,
    172899,
    172901,
    188591,
    203564,
    211145,
    230605,
    247687,
]

EXTRA_ENDPOINTS = [
    {
        "name": "search-parametric-model-maker",
        "url": f"{BASE_URL}/search.json?q=%22Parametric%20Model%20Maker%22",
        "notes": "Broad search seed for PMM-related topics.",
    },
    {
        "name": "search-openscad-pmm",
        "url": f"{BASE_URL}/search.json?q=%22Parametric%20Model%20Maker%22%20OpenSCAD",
        "notes": "OpenSCAD-focused search seed for PMM-related topics.",
    },
    {
        "name": "category-makerlab",
        "url": f"{BASE_URL}/c/makerworld/makerlab/163.json",
        "notes": "MakerLab category feed.",
    },
    {
        "name": "latest",
        "url": f"{BASE_URL}/latest.json",
        "notes": "Global latest feed used for discovery.",
    },
]

MAKERWORLD_ENDPOINTS = [
    {
        "name": "libraries-0.8.0",
        "url": f"{MAKERWORLD_BASE}/libraries-0.8.0.json",
        "notes": "Bundled OpenSCAD library inventory exposed by MakerWorld.",
    },
    {
        "name": "fonts-0.8.0",
        "url": f"{MAKERWORLD_BASE}/fonts-0.8.0.json",
        "notes": "Installed font inventory exposed by MakerWorld.",
    },
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unnamed"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def save_artifact(path: Path, payload: dict, metadata: dict) -> None:
    write_json(path, payload)
    write_json(path.with_suffix(path.suffix + ".meta.json"), metadata)


def fetch_topic(topic_id: int, force: bool) -> None:
    url = f"{BASE_URL}/t/{topic_id}.json"
    payload = fetch_json(url)
    slug = slugify(payload.get("slug") or payload.get("title", str(topic_id)))
    path = RAW_DIR / f"topic-{topic_id}-{slug}.json"
    if path.exists() and not force:
        return
    metadata = {
        "source_type": "discourse_json",
        "origin": "Bambu Lab Community Forum (Discourse)",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url": url,
        "capture_method": "public_json_endpoint",
        "verbatim": True,
        "notes": "Fetched from a public Discourse topic JSON endpoint.",
    }
    save_artifact(path, payload, metadata)


def fetch_extra(spec: dict, force: bool) -> None:
    path = RAW_DIR / f"{spec['name']}.json"
    if path.exists() and not force:
        return
    payload = fetch_json(spec["url"])
    metadata = {
        "source_type": "discourse_json",
        "origin": "Bambu Lab Community Forum (Discourse)",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url": spec["url"],
        "capture_method": "public_json_endpoint",
        "verbatim": True,
        "notes": spec["notes"],
    }
    save_artifact(path, payload, metadata)


def fetch_makerworld(spec: dict, force: bool) -> None:
    path = MAKERWORLD_RAW_DIR / f"{spec['name']}.json"
    if path.exists() and not force:
        return
    payload = fetch_json(spec["url"])
    metadata = {
        "source_type": "makerworld_json",
        "origin": "MakerWorld PMM app endpoint",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url": spec["url"],
        "capture_method": "public_app_json_endpoint",
        "verbatim": True,
        "notes": spec["notes"],
    }
    save_artifact(path, payload, metadata)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Re-fetch even if files already exist.")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MAKERWORLD_RAW_DIR.mkdir(parents=True, exist_ok=True)
    for topic_id in TOPICS:
        fetch_topic(topic_id, force=args.force)
        time.sleep(0.1)
    for spec in EXTRA_ENDPOINTS:
        fetch_extra(spec, force=args.force)
        time.sleep(0.1)
    for spec in MAKERWORLD_ENDPOINTS:
        fetch_makerworld(spec, force=args.force)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
