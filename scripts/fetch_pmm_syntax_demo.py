#!/usr/bin/env python3
"""Extract PMM's default OpenSCAD syntax demo from public web chunks."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = REPO_ROOT / "sources" / "raw" / "makerworld"
PATTERNS_DIR = REPO_ROOT / "patterns"
DISCOVERY_PATH = DATA_DIR / "pmm-web-discovery.json"
STATUS_PATH = DATA_DIR / "pmm-syntax-demo.json"
RAW_SCAD_PATH = RAW_DIR / "pmm-syntax-demo.scad"
PATTERN_SCAD_PATH = PATTERNS_DIR / "pmm-syntax-demo.scad"
PAGE_URL = "https://makerworld.com/en/makerlab/parametricModelMaker?pageType=generator"
MAKERWORLD_ORIGIN = "https://makerworld.com"
NEXT_BASE = "https://makerworld.com/_next/"
ENGLISH_MARKER = "// We will demonstrate most of the syntax supported by Parametric Model Maker here."
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://makerworld.com/",
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def fetch_text(url: str) -> tuple[bool, int | None, str]:
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read()
            return True, getattr(response, "status", 200), body.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return False, exc.code, body
    except Exception:
        return False, None, ""


def parse_seed_file(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"https://[^\s'\"<>);]+", text))


def load_previous_seed_urls() -> set[str]:
    if not DISCOVERY_PATH.exists():
        return set()
    data = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))
    urls = set(data.get("current_chunk_urls", []))
    if data.get("build_manifest_url"):
        urls.add(data["build_manifest_url"])
    for record in data.get("public_fetches", []):
        url = record.get("url")
        if url and "/_next/static/" in url:
            urls.add(url)
    return urls


def extract_static_urls(text: str) -> set[str]:
    urls = set()
    for match in re.findall(r'(?:"|\')(\/_next\/static\/[^"\']+?\.js)(?:"|\')', text):
        urls.add(urljoin(MAKERWORLD_ORIGIN, match))
    for match in re.findall(r"https://makerworld\.com/_next/static/[^\"'<> )]+?\.js", text):
        urls.add(match)
    return urls


def chunk_url_from_runtime_path(path: str) -> str:
    return urljoin(NEXT_BASE, path)


def extract_parametric_route_chunk_urls(text: str) -> set[str]:
    urls = set()
    for match in re.findall(r"static/chunks/pages/makerlab/parametricModelMaker-[A-Za-z0-9]+\.js", text):
        urls.add(chunk_url_from_runtime_path(match))
    return urls


def parse_chunk_id_maps(runtime_texts: list[str]) -> dict[int, str]:
    chunk_paths: dict[int, str] = {}
    for text in runtime_texts:
        for chunk_id, path in re.findall(r"(\d+)===e\?\"(static/chunks/[^\"]+?\.js)\"", text):
            chunk_paths[int(chunk_id)] = path

        dynamic_match = re.search(
            r'"static/chunks/"\+\(\(\{(?P<prefix>[^{}]+)\}\)\[e\]\|\|e\)\+"\."\+\(\{(?P<hash>[^{}]+)\}\)\[e\]\+"\.js"',
            text,
        )
        if not dynamic_match:
            continue

        prefix_map = {
            int(chunk_id): name
            for chunk_id, name in re.findall(r"(\d+):\"([^\"]+)\"", dynamic_match.group("prefix"))
        }
        hash_map = {
            int(chunk_id): name
            for chunk_id, name in re.findall(r"(\d+):\"([^\"]+)\"", dynamic_match.group("hash"))
        }
        for chunk_id, content_hash in hash_map.items():
            stem = prefix_map.get(chunk_id, str(chunk_id))
            chunk_paths[chunk_id] = f"static/chunks/{stem}.{content_hash}.js"
    return chunk_paths


def parse_dynamic_chunk_ids(text: str) -> set[int]:
    return {int(match) for match in re.findall(r"\b[A-Za-z_$][\w$]*\.e\((\d+)\)", text)}


def decode_js_string_at(text: str, marker_index: int) -> str | None:
    start = marker_index
    while start >= 0:
        char = text[start]
        if char in {"'", '"'}:
            slash_count = 0
            pos = start - 1
            while pos >= 0 and text[pos] == "\\":
                slash_count += 1
                pos -= 1
            if slash_count % 2 == 0:
                break
        start -= 1
    else:
        return None

    quote = text[start]
    end = start + 1
    while end < len(text):
        char = text[end]
        if char == quote:
            slash_count = 0
            pos = end - 1
            while pos > start and text[pos] == "\\":
                slash_count += 1
                pos -= 1
            if slash_count % 2 == 0:
                raw = text[start : end + 1]
                try:
                    return ast.literal_eval(raw)
                except Exception:
                    return None
        end += 1
    return None


def extract_demo_source(chunks: dict[str, str]) -> tuple[str, str] | None:
    for url, text in chunks.items():
        marker_index = text.find(ENGLISH_MARKER)
        if marker_index == -1:
            continue
        decoded = decode_js_string_at(text, marker_index)
        if decoded and ENGLISH_MARKER in decoded and "module mw_assembly_view()" in decoded:
            return url, decoded.strip() + "\n"
    return None


def save_chunk_artifact(source_url: str, text: str, captured_at: str) -> str:
    name = Path(urlparse(source_url).path).name
    path = RAW_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    write_json(
        path.with_suffix(path.suffix + ".meta.json"),
        {
            "source_type": "makerworld_web_asset",
            "origin": "MakerWorld PMM public web asset",
            "captured_at": captured_at,
            "url": source_url,
            "capture_method": "public_web_fetch",
            "verbatim": True,
            "notes": "Generator lazy chunk containing PMM's default OpenSCAD syntax demo.",
        },
    )
    return str(path.relative_to(REPO_ROOT))


def save_demo(source_url: str, chunk_path: str, source: str, captured_at: str, stats: dict) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    RAW_SCAD_PATH.write_text(source, encoding="utf-8")
    PATTERN_SCAD_PATH.write_text(source, encoding="utf-8")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    metadata = {
        "source_type": "makerworld_web_asset",
        "origin": "MakerWorld PMM default OpenSCAD syntax demo embedded in a public generator chunk",
        "captured_at": captured_at,
        "url": source_url,
        "capture_method": "public_web_chunk_extraction",
        "verbatim": True,
        "notes": "Extracted from the English JS string literal used as PMM's default editor source.",
        "extracted_from": chunk_path,
        "content_sha256": digest,
    }
    write_json(RAW_SCAD_PATH.with_suffix(RAW_SCAD_PATH.suffix + ".meta.json"), metadata)
    write_json(
        STATUS_PATH,
        {
            "status": "ok",
            "captured_at": captured_at,
            "source_url": source_url,
            "raw_path": str(RAW_SCAD_PATH.relative_to(REPO_ROOT)),
            "pattern_path": str(PATTERN_SCAD_PATH.relative_to(REPO_ROOT)),
            "chunk_raw_path": chunk_path,
            "content_sha256": digest,
            "line_count": len(source.splitlines()),
            "stats": stats,
        },
    )


def write_stale_status(stats: dict) -> bool:
    if not RAW_SCAD_PATH.exists():
        return False
    source = RAW_SCAD_PATH.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
    PATTERN_SCAD_PATH.write_text(source, encoding="utf-8")
    write_json(
        STATUS_PATH,
        {
            "status": "stale",
            "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "raw_path": str(RAW_SCAD_PATH.relative_to(REPO_ROOT)),
            "pattern_path": str(PATTERN_SCAD_PATH.relative_to(REPO_ROOT)),
            "content_sha256": digest,
            "line_count": len(source.splitlines()),
            "stats": stats,
            "notes": "Current fetch did not find the syntax demo; kept the previous extracted source.",
        },
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-file", action="append", default=[], help="Optional cleaned browser network export containing PMM chunk URLs.")
    parser.add_argument("--seed-url", action="append", default=[], help="Optional public PMM JS chunk URL.")
    args = parser.parse_args()

    captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    seed_urls = set(args.seed_url)
    seed_urls.update(load_previous_seed_urls())
    for seed_file in args.seed_file:
        seed_urls.update(parse_seed_file(Path(seed_file)))

    page_ok, page_status, page_text = fetch_text(PAGE_URL)
    if page_ok:
        seed_urls.update(extract_static_urls(page_text))

    fetched: dict[str, str] = {}
    initial_urls = [url for url in seed_urls if url.endswith(".js") and "makerworld.com/_next/static/" in url]
    for url in sorted(set(initial_urls)):
        ok, _, text = fetch_text(url)
        if ok:
            fetched[url] = text

    route_chunk_urls = set()
    for text in fetched.values():
        route_chunk_urls.update(extract_parametric_route_chunk_urls(text))
    for url in sorted(route_chunk_urls):
        if url in fetched:
            continue
        ok, _, text = fetch_text(url)
        if ok:
            fetched[url] = text

    runtime_texts = [text for url, text in fetched.items() if "/webpack-" in url or url.endswith("_buildManifest.js")]
    chunk_id_paths = parse_chunk_id_maps(runtime_texts)
    dynamic_ids = set()
    for text in fetched.values():
        dynamic_ids.update(parse_dynamic_chunk_ids(text))
    for chunk_id in sorted(dynamic_ids):
        path = chunk_id_paths.get(chunk_id)
        if not path:
            continue
        url = chunk_url_from_runtime_path(path)
        if url in fetched:
            continue
        ok, _, text = fetch_text(url)
        if ok:
            fetched[url] = text

    stats = {
        "page_fetch_ok": page_ok,
        "page_http_status": page_status,
        "seed_url_count": len(seed_urls),
        "fetched_js_count": len(fetched),
        "dynamic_chunk_id_count": len(dynamic_ids),
        "dynamic_chunk_ids": sorted(dynamic_ids),
    }
    extracted = extract_demo_source(fetched)
    if not extracted:
        if write_stale_status(stats):
            return
        print("Could not find PMM syntax demo in fetched chunks.", file=sys.stderr)
        sys.exit(1)

    source_url, source = extracted
    chunk_path = save_chunk_artifact(source_url, fetched[source_url], captured_at)
    save_demo(source_url, chunk_path, source, captured_at, stats)


if __name__ == "__main__":
    main()
