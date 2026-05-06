#!/usr/bin/env python3
"""
Hermes Agent Documentation Update Checker.

Сравнивает текущую документацию на сайте с сохранёнными оригиналами.
Находит новые и изменённые страницы, помечает их для перевода.
Запускать периодически для синхронизации с upstream.

Usage:
  python3 update_check.py          # проверить и показать что нового
  python3 update_check.py --apply  # скачать новое и обновить состояние
"""

import sys
import json
import time
import re
import hashlib
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

# ============================================================
# Configuration
# ============================================================
BASE_DIR = Path("/home/immor/hermes-docs-ru")
ORIGINALS_DIR = BASE_DIR / "originals"
TRANSLATED_DIR = BASE_DIR / "translated"
STATE_FILE = BASE_DIR / "translation_state.json"
METADATA_FILE = ORIGINALS_DIR / "_metadata.json"
BATCHES_FILE = BASE_DIR / "small_batches" / "_batches.json"

SITE_BASE = "https://hermes-agent.nousresearch.com"
SITEMAP_URL = f"{SITE_BASE}/docs/sitemap.xml"

USER_AGENT = "Mozilla/5.0 (compatible; HermesDocUpdater/1.0)"

SKIP_PATTERNS = [r"/docs/search$", r"/docs/$"]

# ============================================================
# Helpers
# ============================================================

def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                # Return content + etag for change detection
                etag = resp.headers.get("ETag", "")
                return raw.decode("utf-8", errors="replace"), etag
        except Exception as e:
            if attempt == retries - 1:
                print(f"  [ERROR] {e}", file=sys.stderr)
                return None, None
            time.sleep(2 ** attempt)


def get_sitemap_urls():
    """Fetch sitemap and return list of doc URLs."""
    content, _ = fetch_url(SITEMAP_URL)
    if not content:
        return []

    urls = []
    root = ET.fromstring(content.encode("utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for url_elem in root.findall(".//sm:url/sm:loc", ns):
        url = url_elem.text.strip()
        if not any(re.search(p, url) for p in SKIP_PATTERNS):
            urls.append(url)
    return urls


def url_to_relpath(url):
    """Convert a doc URL to a relative file path under originals/."""
    path_part = url.replace(SITE_BASE, "").lstrip("/")
    path_part = re.sub(r"^docs/", "", path_part)
    if not path_part:
        path_part = "index"
    return f"{path_part}.md"


def file_hash(path):
    """SHA-256 of file contents."""
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"completed": [], "total_originals": 0, "total_completed": 0, "total_pending": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def generate_batches(files):
    """Group files into batches of 1-2 for translation."""
    # Sort for deterministic output
    files = sorted(files)
    batches = []
    i = 0
    while i < len(files):
        # Try pairs, but single files are fine too
        if i + 1 < len(files):
            batches.append([files[i], files[i + 1]])
            i += 2
        else:
            batches.append([files[i]])
            i += 1
    return batches


def merge_batches(existing_batches, new_batches):
    """Merge new batches with existing ones, avoiding duplicates."""
    existing_files = set()
    for batch in existing_batches:
        for f in batch:
            existing_files.add(f)

    merged = list(existing_batches)
    for batch in new_batches:
        # Only add batches where at least one file is new
        if any(f not in existing_files for f in batch):
            merged.append(batch)
            for f in batch:
                existing_files.add(f)

    return merged


# ============================================================
# Main check logic
# ============================================================

def check_for_updates(apply=False):
    print("=" * 60)
    print("Hermes Docs: Checking for updates...")
    print("=" * 60)

    # 1. Get current sitemap
    print("\n[1/4] Fetching sitemap...")
    urls = get_sitemap_urls()
    if not urls:
        print("  Failed to fetch sitemap! Aborting.")
        return False
    print(f"  Found {len(urls)} URLs in sitemap")

    # 2. Build index of current originals
    print("\n[2/4] Comparing with local originals...")
    current_originals = {}
    for p in sorted(ORIGINALS_DIR.rglob("*.md")):
        if p.name == "_metadata.json":
            continue
        rel = str(p.relative_to(ORIGINALS_DIR))
        current_originals[rel] = {
            "hash": file_hash(p),
            "size": p.stat().st_size,
            "mtime": p.stat().st_mtime,
        }

    # 3. Check each URL against originals
    new_files = []
    changed_files = []
    unchanged_files = []
    missing_files = []

    # Build reverse map: relpath -> url
    rel_to_url = {}
    for url in urls:
        rel = url_to_relpath(url)
        rel_to_url[rel] = url

    # Check which originals no longer exist in sitemap
    for rel in current_originals:
        if rel not in rel_to_url and rel != "_metadata.json":
            missing_files.append(rel)

    # Check each URL from sitemap
    for url in urls:
        rel = url_to_relpath(url)
        orig_path = ORIGINALS_DIR / rel

        if not orig_path.exists():
            new_files.append(rel)
        elif rel in current_originals:
            unchanged_files.append(rel)
        else:
            changed_files.append(rel)

    # Summary
    print(f"\n  Results:")
    print(f"    Unchanged: {len(unchanged_files)}")
    print(f"    New:       {len(new_files)}")
    print(f"    Changed:   {len(changed_files)}")
    print(f"    Removed:   {len(missing_files)}")

    if missing_files:
        print(f"\n  ⚠ Pages no longer in sitemap (removed upstream):")
        for rel in missing_files:
            print(f"    - {rel}")

    if not new_files and not changed_files:
        print("\n  ✅ Everything is up to date!")
        if missing_files:
            print(f"  ⚠ {len(missing_files)} page(s) were removed upstream.")
        return True

    if not apply:
        print("\n  ℹ️  Use --apply to download new/changed pages and update state.")
        return True

    # ============================================================
    # APPLY MODE: download new/changed
    # ============================================================
    print("\n" + "=" * 60)
    print("APPLY MODE: Downloading updates...")
    print("=" * 60)

    # We need the full scraper functionality; for now use simple download
    from bs4 import BeautifulSoup
    import html2text

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_emphasis = False
    converter.body_width = 0
    converter.protect_links = True
    converter.skip_internal_links = False
    converter.images_to_alt = True
    converter.unicode_snob = True
    converter.escape_snob = False
    converter.mark_code = True
    converter.single_line_break = True

    all_affected = new_files + changed_files
    downloaded = 0
    failed = 0

    for rel in all_affected:
        url = rel_to_url.get(rel)
        if not url:
            continue

        filepath = ORIGINALS_DIR / rel
        filepath.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n  [{downloaded + failed + 1}/{len(all_affected)}] {rel}")

        html, etag = fetch_url(url)
        if not html:
            failed += 1
            continue

        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all(["nav", "footer", "script", "style", "header", "aside"]):
                tag.decompose()
            main = soup.find("main") or soup.find("article") or soup
            for selector in [".sidebar", ".toc", ".breadcrumbs", ".pagination", ".edit-link"]:
                for el in main.select(selector):
                    el.decompose()

            markdown = converter.handle(str(main))
            markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
            markdown += f"\n\n<!-- Source: {url} -->\n"

            filepath.write_text(markdown)
            downloaded += 1
            print(f"    ✅ Downloaded ({len(markdown):,} chars)")

        except Exception as e:
            print(f"    ❌ Error: {e}")
            failed += 1

        time.sleep(0.3)

    print(f"\n  Downloaded: {downloaded}, Failed: {failed}")

    # 4. Update state and batches
    print("\n[3/4] Updating translation state...")
    state = load_state()

    # Add new/changed files as pending
    for rel in all_affected:
        if rel not in state["completed"]:
            state["completed"].append(rel)

    # Actually no — new/changed files need translation!
    # Remove them from completed so they'll be re-translated
    for rel in all_affected:
        if rel in state["completed"]:
            state["completed"].remove(rel)

    # Recalculate
    all_originals = set()
    for p in ORIGINALS_DIR.rglob("*.md"):
        if p.name != "_metadata.json":
            all_originals.add(str(p.relative_to(ORIGINALS_DIR)))

    state["total_originals"] = len(all_originals)
    state["total_completed"] = len([f for f in state["completed"] if f in all_originals])
    state["total_pending"] = state["total_originals"] - state["total_completed"]
    save_state(state)

    print(f"  State updated: {state['total_completed']}/{state['total_originals']} completed, {state['total_pending']} pending")

    # 5. Update batches
    print("\n[4/4] Updating batch file...")
    pending = [f for f in sorted(all_originals) if f not in state["completed"]]

    if BATCHES_FILE.exists():
        existing_batches = json.loads(BATCHES_FILE.read_text())
    else:
        existing_batches = []

    new_batches = generate_batches(pending)
    merged = merge_batches(existing_batches, new_batches)

    BATCHES_FILE.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    print(f"  Batches: {len(merged)} total ({len(new_batches)} new)")

    print(f"\n{'=' * 60}")
    print(f"✅ Update complete! {downloaded} pages downloaded.")
    print(f"   {state['total_pending']} pages need translation.")
    print(f"   Run the translate workflow to translate new/changed pages.")
    print(f"{'=' * 60}")

    return True


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    check_for_updates(apply=apply)
