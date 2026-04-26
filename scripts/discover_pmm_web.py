#!/usr/bin/env python3
"""Discover public PMM web assets and classify browser/auth requirements."""

from __future__ import annotations

import argparse
import io
import json
import re
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from urllib.parse import urljoin, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "sources" / "raw" / "makerworld"
DATA_DIR = REPO_ROOT / "data"
DISCOVERY_PATH = DATA_DIR / "pmm-web-discovery.json"
PAGE_URL = "https://makerworld.com/en/makerlab/parametricModelMaker?pageType=generator"
MAKERWORLD_ORIGIN = "https://makerworld.com"
NEXT_STATIC_BASE = "https://makerworld.com/_next/"
DEFAULT_OPENSCAD_BASE = "https://makerworld.bblmw.com/makerworld/makerlab/content-generator/openscad/"
DEFAULT_PUBLIC_ENDPOINTS = [
    f"{DEFAULT_OPENSCAD_BASE}libraries-0.8.0.json",
    f"{DEFAULT_OPENSCAD_BASE}fonts-0.8.0.json",
]
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://makerworld.com/",
}
MAX_TEXT_ARTIFACT_BYTES = 2_000_000


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def fetch_url(url: str) -> dict:
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {
                "ok": True,
                "status": getattr(response, "status", 200),
                "headers": dict(response.headers.items()),
                "body": response.read(),
            }
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "status": exc.code,
            "headers": dict(exc.headers.items()),
            "body": exc.read(),
        }
    except Exception as exc:  # pragma: no cover - network failures are environment-dependent
        return {
            "ok": False,
            "status": None,
            "headers": {},
            "body": b"",
            "error": str(exc),
        }


def decode_text(body: bytes) -> str:
    return body.decode("utf-8", errors="replace")


def artifact_filename(url: str, kind: str | None = None) -> str:
    parsed = urlparse(url)
    if kind == "page":
        return "pmm-page.html"
    if kind == "build_manifest":
        return "pmm-build-manifest.js"
    if kind == "ssg_manifest":
        return "pmm-ssg-manifest.js"
    name = Path(parsed.path).name
    return name or "artifact.bin"


def infer_source_type(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix == ".json":
        return "makerworld_json"
    return "makerworld_web_asset"


def save_raw_artifact(url: str, body: bytes, notes: str, kind: str | None = None) -> str:
    filename = artifact_filename(url, kind=kind)
    path = RAW_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    metadata = {
        "source_type": infer_source_type(url),
        "origin": "MakerWorld PMM public web asset",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url": url,
        "capture_method": "public_web_fetch",
        "verbatim": True,
        "notes": notes,
    }
    write_json(path.with_suffix(path.suffix + ".meta.json"), metadata)
    return str(path.relative_to(REPO_ROOT))


def parse_seed_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"https://[^\s'\"<>]+", text)))


def load_previous_seed_urls() -> list[str]:
    if not DISCOVERY_PATH.exists():
        return []
    data = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))
    urls = []
    urls.extend(data.get("current_chunk_urls", []))
    build_manifest_url = data.get("build_manifest_url")
    if build_manifest_url:
        urls.append(build_manifest_url)
    return sorted(set(urls))


def extract_urls_from_html(text: str) -> set[str]:
    urls = set()
    for match in re.findall(r'(?:"|\')(\/_next\/static\/[^"\']+)(?:"|\')', text):
        urls.add(urljoin(MAKERWORLD_ORIGIN, match))
    for match in re.findall(r'(?:"|\')(https://[^"\']+)(?:"|\')', text):
        if "makerworld" in match:
            urls.add(match)
    return urls


def extract_urls_from_text(text: str) -> tuple[set[str], set[str], set[str], set[str]]:
    absolute_urls = set(re.findall(r"https://[A-Za-z0-9./?_=:%&@#~+-]+", text))
    relative_urls = set(
        re.findall(
            r"(?:/(?:_next|api|makerworld)|static/chunks)/[A-Za-z0-9._~:/?#[\]@!$&'()*+,;=%-]+",
            text,
        )
    )
    base_urls = set(
        re.findall(
            r"https://makerworld\.bblmw\.(?:com|cn)/makerworld/makerlab/content-generator/(?:openscad|stl)/",
            text,
        )
    )
    content_files = set(re.findall(r"[A-Za-z0-9_.-]+\.(?:json|zip|stl)", text))
    return absolute_urls, relative_urls, base_urls, content_files


def relevant_chunk_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    if not path.endswith(".js"):
        return False
    if parsed.netloc != "makerworld.com":
        return False
    return (
        "openscad" in path
        or "parametricmodelmaker" in path
        or "_buildmanifest.js" in path
        or "_ssgmanifest.js" in path
    )


def direct_public_asset(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc not in {"makerworld.bblmw.com", "makerworld.bblmw.cn"}:
        return False
    path = parsed.path
    return "/makerworld/makerlab/content-generator/openscad/" in path and Path(path).suffix.lower() in {
        ".json",
        ".zip",
    }


def auth_hint(url: str) -> str:
    path = urlparse(url).path
    if "/api/v1/" not in path:
        return "public"
    if "/my/" in path:
        return "login_required"
    if any(token in path for token in ["credit", "message/count", "cart/count", "totalunreadcount", "point-service"]):
        return "likely_login_required"
    return "unknown_api"


def summarize_json(body: bytes) -> dict:
    payload = json.loads(decode_text(body))
    summary = {"top_level_type": type(payload).__name__}
    if isinstance(payload, dict):
        summary["keys"] = list(payload.keys())[:20]
        if "fontNames" in payload and isinstance(payload["fontNames"], list):
            summary["font_count"] = len(payload["fontNames"])
            summary["font_sample"] = payload["fontNames"][:15]
        if "list" in payload and isinstance(payload["list"], list):
            summary["list_count"] = len(payload["list"])
    elif isinstance(payload, list):
        summary["item_count"] = len(payload)
    return summary


def summarize_zip(body: bytes) -> dict:
    zf = zipfile.ZipFile(io.BytesIO(body))
    names = zf.namelist()
    summary = {"member_count": len(names), "members": names[:20]}
    json_members = [name for name in names if name.endswith(".json")]
    if json_members:
        first = json_members[0]
        payload = json.loads(zf.read(first).decode("utf-8"))
        summary["first_json_member"] = first
        summary["first_json_type"] = type(payload).__name__
        if isinstance(payload, dict):
            keys = list(payload.keys())
            summary["first_json_key_count"] = len(keys)
            summary["first_json_key_sample"] = keys[:12]
            if keys and isinstance(payload[keys[0]], list):
                summary["first_value_count"] = len(payload[keys[0]])
                summary["first_value_sample"] = payload[keys[0]][:10]
    return summary


def summarize_fetch(url: str, response: dict) -> dict:
    content_type = response.get("headers", {}).get("Content-Type", "")
    suffix = Path(urlparse(url).path).suffix.lower()
    summary = {
        "content_type": content_type,
        "bytes": len(response.get("body", b"")),
    }
    if suffix == ".json":
        try:
            summary.update(summarize_json(response["body"]))
        except Exception as exc:  # pragma: no cover - malformed remote payloads are unlikely
            summary["parse_error"] = str(exc)
    elif suffix == ".zip":
        try:
            summary.update(summarize_zip(response["body"]))
        except Exception as exc:  # pragma: no cover - malformed remote payloads are unlikely
            summary["parse_error"] = str(exc)
    elif suffix == ".js":
        text = decode_text(response["body"][:MAX_TEXT_ARTIFACT_BYTES])
        absolute_urls, relative_urls, base_urls, content_files = extract_urls_from_text(text)
        summary["embedded_absolute_url_count"] = len(absolute_urls)
        summary["embedded_relative_url_count"] = len(relative_urls)
        summary["embedded_base_url_count"] = len(base_urls)
        summary["embedded_content_file_count"] = len(content_files)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-file", action="append", default=[], help="Optional text file containing copied PMM network URLs or curl commands.")
    parser.add_argument("--seed-url", action="append", default=[], help="Optional known PMM chunk or asset URL.")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    seed_urls = set(DEFAULT_PUBLIC_ENDPOINTS)
    seed_urls.update(load_previous_seed_urls())
    seed_urls.update(args.seed_url)
    seed_sources = []
    for seed_file in args.seed_file:
        path = Path(seed_file)
        urls = parse_seed_file(path)
        seed_urls.update(urls)
        seed_sources.append({"path": str(path), "url_count": len(urls)})

    page_response = fetch_url(PAGE_URL)
    page_status = "ok" if page_response.get("ok") else "error"
    if page_response.get("headers", {}).get("cf-mitigated") == "challenge":
        page_status = "cloudflare_challenge"
    elif page_response.get("status") == 403 and b"Just a moment" in page_response.get("body", b""):
        page_status = "cloudflare_challenge"

    if page_response.get("ok") and page_status == "ok":
        page_text = decode_text(page_response["body"])
        seed_urls.update(extract_urls_from_html(page_text))
        save_raw_artifact(PAGE_URL, page_response["body"], "Live PMM page HTML fetched without a browser session.", kind="page")

    build_manifest_url = None
    manifest_urls = [url for url in seed_urls if url.endswith("_buildManifest.js")]
    if not manifest_urls and page_response.get("ok") and page_status == "ok":
        page_text = decode_text(page_response["body"])
        matches = re.findall(r"/_next/static/[^\"']+_buildManifest\.js", page_text)
        if matches:
            manifest_urls.append(urljoin(MAKERWORLD_ORIGIN, matches[0]))

    fetched_artifacts = []
    public_fetches = []
    account_candidates = []
    discovered_bases = set()
    discovered_content_files = set()
    discovered_relative_urls = set()
    current_chunk_urls = []

    for url in sorted(seed_urls):
        hint = auth_hint(url)
        if hint != "public":
            account_candidates.append({"url": url, "auth_hint": hint, "source": "seed"})
            continue
        if not relevant_chunk_url(url) and not direct_public_asset(url):
            continue
        response = fetch_url(url)
        artifact_record = {
            "url": url,
            "status": response.get("status"),
            "ok": response.get("ok", False),
        }
        if response.get("ok"):
            notes = "Fetched from a public PMM web asset or chunk URL."
            kind = None
            if url.endswith("_buildManifest.js"):
                kind = "build_manifest"
                build_manifest_url = url
            elif url.endswith("_ssgManifest.js"):
                kind = "ssg_manifest"
            artifact_record["saved_path"] = save_raw_artifact(url, response["body"], notes, kind=kind)
            artifact_record["summary"] = summarize_fetch(url, response)
            public_fetches.append(artifact_record)
            fetched_artifacts.append(url)
            if url.endswith(".js"):
                text = decode_text(response["body"][:MAX_TEXT_ARTIFACT_BYTES])
                absolute_urls, relative_urls, base_urls, content_files = extract_urls_from_text(text)
                discovered_relative_urls.update(relative_urls)
                discovered_bases.update(base_urls)
                discovered_content_files.update(content_files)
                if relevant_chunk_url(url) and not url.endswith(("_buildManifest.js", "_ssgManifest.js")):
                    current_chunk_urls.append(url)
        else:
            artifact_record["error"] = response.get("error")
            public_fetches.append(artifact_record)

    discovered_urls = set()
    for url in discovered_relative_urls:
        if url.startswith("/_next/") or url.startswith("/api/"):
            discovered_urls.add(urljoin(MAKERWORLD_ORIGIN, url))
        elif url.startswith("static/chunks/"):
            discovered_urls.add(urljoin(NEXT_STATIC_BASE, url))
        elif url.startswith("/makerworld/makerlab/content-generator/openscad/"):
            discovered_urls.add(urljoin("https://makerworld.bblmw.com", url))
        elif url.startswith("/makerworld/makerlab/content-generator/stl/"):
            discovered_urls.add(urljoin("https://makerworld.bblmw.com", url))

    openscad_base = next((base for base in sorted(discovered_bases) if base.endswith("/openscad/") and ".com/" in base), DEFAULT_OPENSCAD_BASE)
    for filename in sorted(discovered_content_files):
        if filename.endswith((".json", ".zip")):
            discovered_urls.add(urljoin(openscad_base, filename))

    for url in sorted(discovered_urls):
        if auth_hint(url) != "public":
            account_candidates.append({"url": url, "auth_hint": auth_hint(url), "source": "chunk_string"})
            continue
        if url in fetched_artifacts or (not direct_public_asset(url) and not relevant_chunk_url(url)):
            continue
        response = fetch_url(url)
        artifact_record = {
            "url": url,
            "status": response.get("status"),
            "ok": response.get("ok", False),
            "source": "chunk_string",
        }
        if response.get("ok"):
            artifact_record["saved_path"] = save_raw_artifact(
                url,
                response["body"],
                "Discovered from public PMM chunk strings and fetched without auth.",
            )
            artifact_record["summary"] = summarize_fetch(url, response)
            public_fetches.append(artifact_record)
            fetched_artifacts.append(url)
            if url.endswith(".js"):
                text = decode_text(response["body"][:MAX_TEXT_ARTIFACT_BYTES])
                absolute_urls, relative_urls, base_urls, content_files = extract_urls_from_text(text)
                discovered_relative_urls.update(relative_urls)
                discovered_bases.update(base_urls)
                discovered_content_files.update(content_files)
                if relevant_chunk_url(url) and not url.endswith(("_buildManifest.js", "_ssgManifest.js")):
                    current_chunk_urls.append(url)
        else:
            artifact_record["error"] = response.get("error")
            public_fetches.append(artifact_record)

    openscad_base = next((base for base in sorted(discovered_bases) if base.endswith("/openscad/") and ".com/" in base), DEFAULT_OPENSCAD_BASE)
    extra_content_urls = {
        urljoin(openscad_base, filename)
        for filename in discovered_content_files
        if filename.endswith((".json", ".zip"))
    }
    for url in sorted(extra_content_urls):
        if url in fetched_artifacts or auth_hint(url) != "public" or not direct_public_asset(url):
            continue
        response = fetch_url(url)
        artifact_record = {
            "url": url,
            "status": response.get("status"),
            "ok": response.get("ok", False),
            "source": "chunk_string",
        }
        if response.get("ok"):
            artifact_record["saved_path"] = save_raw_artifact(
                url,
                response["body"],
                "Discovered from public PMM chunk strings and fetched without auth.",
            )
            artifact_record["summary"] = summarize_fetch(url, response)
            public_fetches.append(artifact_record)
            fetched_artifacts.append(url)
        else:
            artifact_record["error"] = response.get("error")
            public_fetches.append(artifact_record)

    for url in sorted(discovered_urls):
        if auth_hint(url) != "public":
            account_candidates.append({"url": url, "auth_hint": auth_hint(url), "source": "discovered"})

    notes = [
        "The top-level PMM page can be Cloudflare challenge-protected for headless or non-browser clients even when lower-level PMM assets remain directly fetchable.",
        "Public `_next/static` chunks and `makerworld.bblmw.com/makerworld/makerlab/content-generator/...` assets are the main unauthenticated discovery surface once a current chunk URL or build manifest URL is known.",
    ]
    if seed_sources:
        notes.append("A browser-exported network log or copied curl list can be used as a safe seed source after removing cookies and tokens.")

    payload = {
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "page_url": PAGE_URL,
        "page_fetch": {
            "status": page_status,
            "http_status": page_response.get("status"),
            "cf_mitigated": page_response.get("headers", {}).get("cf-mitigated"),
            "error": page_response.get("error"),
        },
        "seed_sources": seed_sources,
        "seed_url_count": len(seed_urls),
        "build_manifest_url": build_manifest_url,
        "current_chunk_urls": sorted(set(current_chunk_urls)),
        "region_base_urls": sorted(discovered_bases),
        "public_fetches": sorted(public_fetches, key=lambda item: item["url"]),
        "account_api_candidates": sorted(account_candidates, key=lambda item: item["url"]),
        "notes": notes,
    }
    write_json(DISCOVERY_PATH, payload)


if __name__ == "__main__":
    main()
