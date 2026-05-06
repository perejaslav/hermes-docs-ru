#!/usr/bin/env python3
"""
Build script: prepares the translated documentation for MkDocs and GitHub Pages.

1. Copies translated files to a staging directory
2. Renames `.md` (empty-name) files to `index.md`
3. Generates mkdocs.yml with full navigation
4. Handles special cases for the site to work correctly
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
TRANSLATED_DIR = BASE_DIR / "translated"
STAGING_DIR = BASE_DIR / "site_source"
STATE_FILE = BASE_DIR / "translation_state.json"
CONFIG_FILE = BASE_DIR / "mkdocs.yml"
SKILLS_OPTIONAL_FILE = STAGING_DIR / "docs" / "reference" / "optional-skills-catalog.md"


def clean_staging():
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)


def copy_and_rename():
    """Copy translated files, renaming .md to index.md where needed."""
    count = 0
    for src in sorted(TRANSLATED_DIR.rglob("*.md")):
        rel = src.relative_to(TRANSLATED_DIR)  # e.g. docs/integrations/.md
        parts = list(rel.parts)

        if parts[-1] == ".md":
            # Empty-name file → rename to index.md
            parts[-1] = "index.md"
        elif parts[-1].endswith(".md"):
            # Regular .md file → keep as is
            pass

        dst = STAGING_DIR / "/".join(parts)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        count += 1

    return count


def build_nav():
    """Build navigation from the staging directory structure."""

    def title_from_path(rel_path):
        """Convert a file path to a display title."""
        name = rel_path.stem
        if name == "index":
            return None  # Index pages get their parent's name

        # Remove category prefixes from skill files
        name = re.sub(r"^[\w]+-", "", name)
        name = name.replace("-", " ").replace("_", " ").title()

        # Fix common abbreviations
        name = name.replace("Mlops", "MLOps").replace("Cli", "CLI")
        name = name.replace("Ssh", "SSH").replace("Tui", "TUI")
        name = name.replace("Tts", "TTS").replace("Api", "API")
        name = name.replace("Mcp", "MCP").replace("Acp", "ACP")
        name = name.replace("Fts5", "FTS5").replace("Sqlite", "SQLite")
        name = name.replace(".md", "").strip()

        return name

    import re

    docs_dir = STAGING_DIR / "docs"
    nav = []

    # Ordered top-level categories (mirrors the original site)
    categories = [
        ("getting-started", "Начало работы"),
        ("user-guide/features", "Возможности"),
        ("user-guide/configuration", "Конфигурация"),
        ("user-guide/cli", "CLI"),
        ("user-guide/tui", "TUI"),
        ("user-guide/profiles", "Профили"),
        ("user-guide/sessions", "Сессии"),
        ("user-guide/security", "Безопасность"),
        ("user-guide/docker", "Docker"),
        ("user-guide/git-worktrees", "Git Worktrees"),
        ("user-guide/checkpoints-and-rollback", "Контрольные точки"),
        ("user-guide/messaging", "Мессенджеры"),
        ("user-guide/skills/bundled", "Навыки (встроенные)"),
        ("user-guide/skills/optional", "Навыки (опциональные)"),
        ("user-guide/skills", "Обзор навыков"),
        ("guides", "Руководства"),
        ("developer-guide", "Разработчикам"),
        ("reference", "Справочник"),
        ("integrations", "Интеграции"),
        ("user-stories", "Истории пользователей"),
    ]

    # Handle special single-page entries (files directly in docs/user-guide/)
    single_pages = {
        "user-guide/configuration": "Конфигурация",
        "user-guide/cli": "CLI",
        "user-guide/tui": "TUI",
        "user-guide/profiles": "Профили",
        "user-guide/sessions": "Сессии",
        "user-guide/security": "Безопасность",
        "user-guide/docker": "Docker",
        "user-guide/git-worktrees": "Git Worktrees",
        "user-guide/checkpoints-and-rollback": "Контрольные точки и откат",
        "user-stories": "Истории пользователей",
    }
    # Track which paths we've handled so we don't double-add
    handled_paths = set()

    for cat_path, cat_title in categories:
        cat_dir = docs_dir / cat_path

        if cat_path in single_pages:
            # Single page entry — file directly at path like docs/user-guide/configuration.md
            direct = docs_dir / f"{cat_path}.md"
            if direct.exists():
                rel = direct.relative_to(STAGING_DIR)
                nav.append({cat_title: str(rel)})
                handled_paths.add(cat_path)
                continue
            # Fallback: check if it's a directory with index.md
            if cat_dir.exists() and (cat_dir / "index.md").exists():
                nav.append({cat_title: f"docs/{cat_path}/index.md"})
                handled_paths.add(cat_path)
                continue

        if cat_path in handled_paths:
            continue

        if not cat_dir.exists():
            continue

        # Check if there's an index page for this category
        index_page = cat_dir / "index.md"
        has_index = index_page.exists()

        if cat_path in ["user-guide/skills/bundled", "user-guide/skills/optional"]:
            # These are large skill catalogs - use nested structure
            section_items = []
            for skill_dir in sorted(cat_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_name = title_from_path(skill_dir)
                # Get all skill files in this category dir
                skill_pages = []
                for skill_file in sorted(skill_dir.rglob("*.md")):
                    rel = skill_file.relative_to(STAGING_DIR)
                    skill_title = title_from_path(skill_file)
                    if skill_title:
                        skill_pages.append({skill_title: str(rel)})

                if skill_pages:
                    section_items.append({skill_name: skill_pages})

            if has_index:
                nav.append({
                    cat_title: [
                        {"Обзор": f"docs/{cat_path}/index.md"},
                        *section_items,
                    ]
                })
            elif section_items:
                nav.append({cat_title: section_items})
            continue

        # General case: collect all pages in this category and subcategories
        items = []
        if has_index:
            items.append({"Обзор": f"docs/{cat_path}/index.md"})

        # Collect subdirectories and files
        for item in sorted(cat_dir.iterdir()):
            if item.is_dir():
                sub_pages = []
                for sub_file in sorted(item.rglob("*.md")):
                    rel = sub_file.relative_to(STAGING_DIR)
                    sub_title = title_from_path(sub_file)
                    if sub_title:
                        sub_pages.append({sub_title: str(rel)})
                if sub_pages:
                    sub_title = title_from_path(item)
                    items.append({sub_title: sub_pages})
            elif item.is_file() and item.suffix == ".md" and item.name != "index.md":
                rel = item.relative_to(STAGING_DIR)
                file_title = title_from_path(item)
                items.append({file_title: str(rel)})

        nav.append({cat_title: items})

    return nav


def generate_mkdocs_config(nav):
    """Generate mkdocs.yml content."""
    config = f"""# MkDocs config — auto-generated from translated docs
site_name: Документация Hermes Agent
site_description: Полный перевод документации Hermes Agent на русский язык
site_url: https://perejaslav.github.io/hermes-docs-ru/
repo_url: https://github.com/perejaslav/hermes-docs-ru
edit_uri: blob/main/translated/
docs_dir: site_source

theme:
  name: material
  language: ru
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: Переключить на тёмную тему
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: Переключить на светлую тему
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.indexes
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy
    - content.tabs.link
  icon:
    logo: material/book-open-variant
    repo: fontawesome/brands/github

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/perejaslav/hermes-docs-ru
    - icon: fontawesome/brands/discord
      link: https://discord.gg/NousResearch
  generator: false

copyright: Copyright &copy; 2025-2026 Nous Research — перевод сообщества

plugins:
  - search:
      lang: ru

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - tables
  - toc:
      permalink: true
      title: На этой странице
  - attr_list
  - md_in_html

nav:
"""
    # Format the nav YAML
    def format_nav_item(item, indent=2, is_list=True):
        result = ""
        prefix = " " * indent + ("- " if is_list else "  ")
        for key, value in item.items():
            if isinstance(value, str):
                result += f'{prefix}"{key}": {value}\n'
            elif isinstance(value, list):
                result += f"{prefix}{key}:\n"
                for sub in value:
                    result += format_nav_item(sub, indent + 2, True)
            else:
                result += f"{prefix}{key}: {value}\n"
        return result

    for item in nav:
        config += format_nav_item(item, indent=0, is_list=True)

    return config


if __name__ == "__main__":
    print("🧹 Cleaning staging directory...")
    clean_staging()

    print("📁 Copying and renaming files...")
    count = copy_and_rename()
    print(f"   {count} files prepared")

    print("🧭 Building navigation...")
    nav = build_nav()

    print("📝 Generating mkdocs.yml...")
    config = generate_mkdocs_config(nav)

    # Save config next to the staging dir
    CONFIG_FILE.write_text(config, encoding="utf-8")

    # Also save nav as JSON for inspection
    nav_json = BASE_DIR / "nav_preview.json"
    nav_json.write_text(json.dumps(nav, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ Done!")
    print(f"   Config: mkdocs.yml")
    print(f"   Source: site_source/")
    print(f"   Nav items: {len(nav)} top-level sections")
    print(f"\n   To preview locally: mkdocs serve")
    print(f"   To build: mkdocs build")
