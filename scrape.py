#!/usr/bin/env python3
"""
Hermes Agent Documentation Scraper
Downloads all documentation pages from sitemap.xml, extracts content,
converts to markdown, saves to organized directory structure.
"""

import os
import re
import sys
import time
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

OUTPUT_DIR = Path("/home/immor/hermes-docs-ru/originals")
SITE_BASE = "https://hermes-agent.nousresearch.com"
SITEMAP_URL = f"{SITE_BASE}/docs/sitemap.xml"
METADATA_FILE = OUTPUT_DIR / "_metadata.json"

# Pages to skip (non-content pages)
SKIP_PATTERNS = [
    r"/docs/search$",
    r"/docs/$",
]

USER_AGENT = "Mozilla/5.0 (compatible; HermesDocScraper/1.0; +https://hermes-agent.nousresearch.com)"

converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.ignore_emphasis = False
converter.body_width = 0  # no line wrapping
converter.protect_links = True
converter.skip_internal_links = False
converter.images_to_alt = True
converter.unicode_snob = True  # utf-8 only
converter.escape_snob = False
converter.mark_code = True
converter.single_line_break = True


def fetch_url(url):
    """Fetch a URL with retries."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt == 2:
                print(f"  [ERROR] Failed to fetch {url}: {e}", file=sys.stderr)
                return None
            time.sleep(2 ** attempt)


def url_to_filepath(url):
    """Convert a documentation URL to a local file path."""
    path_part = url.replace(SITE_BASE, "").lstrip("/")
    if not path_part:
        path_part = "index"
    path_part = re.sub(r"/docs/", "", path_part, count=1)
    if not path_part:
        path_part = "index"
    # Special case: docs/ -> index
    if path_part == "index":
        return OUTPUT_DIR / "index.md"
    return OUTPUT_DIR / f"{path_part}.md"


def get_sitemap_urls():
    """Fetch and parse sitemap.xml, return list of URLs."""
    print("Fetching sitemap...")
    content = fetch_url(SITEMAP_URL)
    if not content:
        print("Failed to fetch sitemap!", file=sys.stderr)
        return []

    urls = []
    root = ET.fromstring(content.encode("utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for url_elem in root.findall(".//sm:url/sm:loc", ns):
        url = url_elem.text.strip()
        # Skip non-content pages
        should_skip = any(re.search(p, url) for p in SKIP_PATTERNS)
        if not should_skip:
            urls.append(url)

    print(f"Found {len(urls)} content URLs in sitemap")
    return urls


def clean_html_content(html):
    """Extract meaningful content from the documentation HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove nav, footer, scripts, styles
    for tag in soup.find_all(["nav", "footer", "script", "style", "header", "aside"]):
        tag.decompose()

    # Try to find main content
    main = soup.find("main")
    if main:
        content = main
    else:
        article = soup.find("article")
        content = article if article else soup

    # Remove remaining boilerplate
    for selector in [".sidebar", ".toc", ".breadcrumbs", ".pagination", ".edit-link"]:
        for el in content.select(selector):
            el.decompose()

    # Get the page title from <h1> or <title>
    title_tag = content.find("h1")
    if not title_tag:
        title_tag = soup.find("title")

    title = title_tag.get_text(strip=True) if title_tag else ""

    return str(content), title


def html_to_markdown(html_content, url):
    """Convert cleaned HTML to Markdown."""
    # Clean up excess whitespace in HTML
    text = converter.handle(html_content)

    # Post-processing: clean up excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # Add source URL as comment at the end
    text += f"\n\n<!-- Source: {url} -->\n"

    return text


def get_nav_title(url):
    """Extract a readable nav-style title from the URL."""
    path = url.replace(SITE_BASE + "/docs/", "").rstrip("/")
    if not path:
        return "Home"

    # Handle skills paths
    if "skills/" in path:
        parts = path.split("/")
        if len(parts) >= 3:
            if "bundled" in parts:
                idx = parts.index("bundled")
                if idx + 2 < len(parts):
                    cat = parts[idx + 1]
                    name = parts[idx + 2]
                    # Strip category prefix from name
                    for prefix in ["software-development-", "productivity-", "research-", "creative-", "devops-", "data-science-", "mlops-", "gaming-", "github-", "apple-", "note-taking-", "smart-home-", "social-media-", "red-teaming-", "email-", "dogfood-", "mcp-", "media-", "yuanbao-", "autonomous-ai-agents-"]:
                        if name.startswith(prefix):
                            name = name[len(prefix):]
                            break
                    name = name.replace("-", " ").title()
                    return f"[Skills] {cat.title()} / {name}"
            if "optional" in parts:
                idx = parts.index("optional")
                if idx + 2 < len(parts):
                    cat = parts[idx + 1]
                    name = parts[idx + 2]
                    for prefix in ["mlops-", "productivity-", "creative-", "research-", "security-", "blockchain-", "autonomous-ai-agents-", "health-", "devops-", "communication-", "mcp-", "migration-", "dogfood-", "email-", "web-development-"]:
                        if name.startswith(prefix):
                            name = name[len(prefix):]
                            break
                    name = name.replace("-", " ").title()
                    return f"[Optional] {cat.title()} / {name}"

    # Handle messaging paths
    if "messaging/" in path:
        platform = path.split("/")[-1]
        if platform == "":
            return "Messaging Overview"
        return f"Messaging / {platform.title()}"

    # Handle features paths
    if "features/" in path:
        feature = path.split("/")[-1]
        return f"Features / {feature.replace('-', ' ').title()}"

    # Handle user-guide paths
    if "user-guide/" in path:
        section = path.replace("user-guide/", "")
        if "/" not in section:
            return section.replace("-", " ").title()
        return section.replace("-", " ").title()

    # Handle reference
    if "reference/" in path:
        ref = path.replace("reference/", "")
        return f"Reference / {ref.replace('-', ' ').title()}"

    # Handle guides
    if "guides/" in path:
        guide = path.replace("guides/", "")
        return f"Guide / {guide.replace('-', ' ').title()}"

    # Handle developer-guide
    if "developer-guide/" in path:
        guide = path.replace("developer-guide/", "")
        return f"Dev Guide / {guide.replace('-', ' ').title()}"

    # Handle getting-started
    if "getting-started/" in path:
        guide = path.replace("getting-started/", "")
        return f"Getting Started / {guide.replace('-', ' ').title()}"

    # Handle integrations
    if "integrations/" in path:
        part = path.replace("integrations/", "")
        return f"Integrations / {part.replace('-', ' ').title()}"

    return path.replace("-", " ").title()


def scrape_all():
    """Main scraping function."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    urls = get_sitemap_urls()
    if not urls:
        print("No URLs found, aborting.", file=sys.stderr)
        sys.exit(1)

    metadata = {}
    success = 0
    failed = 0
    total = len(urls)

    for i, url in enumerate(urls, 1):
        nav_title = get_nav_title(url)
        filepath = url_to_filepath(url)

        # Create subdirectories as needed
        filepath.parent.mkdir(parents=True, exist_ok=True)

        print(f"[{i}/{total}] {nav_title}")

        html = fetch_url(url)
        if not html:
            failed += 1
            metadata[url] = {"title": nav_title, "status": "failed"}
            continue

        try:
            clean_html, page_title = clean_html_content(html)
            markdown = html_to_markdown(clean_html, url)

            # Use page title from HTML if available, else nav title
            display_title = page_title if page_title else nav_title

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown)

            # Verify write
            if filepath.exists() and filepath.stat().st_size > 0:
                success += 1
                metadata[url] = {
                    "title": display_title,
                    "nav_title": nav_title,
                    "file": str(filepath.relative_to(OUTPUT_DIR)),
                    "size": filepath.stat().st_size,
                    "status": "ok",
                }
            else:
                failed += 1
                metadata[url] = {"title": nav_title, "status": "empty"}
        except Exception as e:
            failed += 1
            metadata[url] = {"title": nav_title, "status": f"error: {e}"}
            print(f"  [ERROR] Processing {url}: {e}", file=sys.stderr)

        # Be polite to the server
        time.sleep(0.3)

    # Save metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Scraping complete!")
    print(f"  Total URLs: {total}")
    print(f"  Success:    {success}")
    print(f"  Failed:     {failed}")
    print(f"  Output:     {OUTPUT_DIR}")
    print(f"  Metadata:   {METADATA_FILE}")

    # Summary by category
    print(f"\nFiles by category:")
    cats = {}
    for p in sorted(OUTPUT_DIR.rglob("*.md")):
        if p.name == "_metadata.json":
            continue
        rel = str(p.relative_to(OUTPUT_DIR))
        cat = rel.split("/")[0] if "/" in rel else "root"
        cats.setdefault(cat, []).append(rel)
    for cat, files in sorted(cats.items()):
        total_size = sum((OUTPUT_DIR / f).stat().st_size for f in files)
        print(f"  {cat}/: {len(files)} files, {total_size:,} bytes")


if __name__ == "__main__":
    scrape_all()
