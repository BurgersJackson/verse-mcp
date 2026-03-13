"""MCP Server for Verse Language Documentation (https://verselang.github.io/book/)"""

import importlib.resources
import os
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("verse-docs")

BASE_URL = "https://verselang.github.io/book/"

# Cache dir: env override > platform cache dir
CACHE_DIR = Path(
    os.environ.get(
        "VERSE_MCP_CACHE_DIR",
        Path(os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
        / "verse-mcp",
    )
)

# Digest path: env override > bundled package data
_DIGEST_OVERRIDE = os.environ.get("VERSE_DIGEST_PATH")


def _get_digest_path() -> Path:
    if _DIGEST_OVERRIDE:
        return Path(_DIGEST_OVERRIDE)
    # Use importlib.resources to find the bundled file
    return Path(str(importlib.resources.files("verse_mcp") / "data" / "verse_digest.md"))


def _load_digest() -> str:
    """Load the verse_digest.md file."""
    return _get_digest_path().read_text(encoding="utf-8")


def _parse_digest_sections() -> dict[str, str]:
    """Parse the digest into sections by ## headings."""
    content = _load_digest()
    sections: dict[str, str] = {}
    current_heading = "header"
    current_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_lines:
                sections[current_heading] = "\n".join(current_lines)
            current_heading = line[3:].strip()
            current_lines = [line]
        elif line.startswith("### "):
            sub_heading = line[4:].strip()
            if current_lines:
                sections[current_heading] = "\n".join(current_lines)
            current_heading = sub_heading
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_heading] = "\n".join(current_lines)

    return sections


CHAPTERS = {
    "overview": "00_overview/",
    "expressions": "01_expressions/",
    "primitives": "02_primitives/",
    "containers": "03_containers/",
    "operators": "04_operators/",
    "mutability": "05_mutability/",
    "functions": "06_functions/",
    "control-flow": "07_control/",
    "failure": "08_failure/",
    "structs-enums": "09_structs_enums/",
    "classes-interfaces": "10_classes_interfaces/",
    "types": "11_types/",
    "access-specifiers": "12_access/",
    "effects": "13_effects/",
    "concurrency": "14_concurrency/",
    "live-variables": "15_live_variables/",
    "modules": "16_modules/",
    "persistable": "17_persistable/",
    "code-evolution": "18_evolution/",
    "concept-index": "concept_index/",
}


async def fetch_page(path: str) -> str:
    """Fetch a page and convert to markdown-like text."""
    cache_file = CACHE_DIR / (path.replace("/", "_").strip("_") or "index")
    cache_file = cache_file.with_suffix(".md")

    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    url = BASE_URL + path
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    main = soup.find("main") or soup.find("article") or soup.find("body")
    if not main:
        return "Could not parse page content."

    for tag in main.find_all(["nav", "script", "style"]):
        tag.decompose()

    text = html_to_markdown(main)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(text, encoding="utf-8")
    return text


def html_to_markdown(element) -> str:
    """Convert HTML element to readable markdown."""
    lines = []
    for child in element.children:
        if isinstance(child, str):
            stripped = child.strip()
            if stripped:
                lines.append(stripped)
            continue

        tag = child.name
        if tag is None:
            continue

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            text = child.get_text(strip=True)
            if text:
                lines.append(f"\n{'#' * level} {text}\n")

        elif tag == "pre":
            code = child.get_text()
            lines.append(f"\n```verse\n{code.strip()}\n```\n")

        elif tag == "code" and child.parent and child.parent.name != "pre":
            lines.append(f"`{child.get_text()}`")

        elif tag in ("ul", "ol"):
            for i, li in enumerate(child.find_all("li", recursive=False)):
                prefix = f"{i+1}." if tag == "ol" else "-"
                lines.append(f"{prefix} {li.get_text(strip=True)}")
            lines.append("")

        elif tag == "p":
            text = child.get_text(strip=True)
            if text:
                lines.append(f"\n{text}\n")

        elif tag == "blockquote":
            text = child.get_text(strip=True)
            if text:
                quoted = "\n".join(f"> {line}" for line in text.split("\n"))
                lines.append(f"\n{quoted}\n")

        elif tag == "table":
            lines.append(html_table_to_markdown(child))

        elif tag in ("div", "section", "article", "main", "details", "summary"):
            lines.append(html_to_markdown(child))

        else:
            text = child.get_text(strip=True)
            if text:
                lines.append(text)

    return "\n".join(lines)


def html_table_to_markdown(table) -> str:
    """Convert an HTML table to markdown."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
        rows.append("| " + " | ".join(cells) + " |")
        if tr.find("th"):
            rows.append("| " + " | ".join("---" for _ in cells) + " |")
    return "\n" + "\n".join(rows) + "\n"


@mcp.tool()
async def list_chapters() -> str:
    """List all available chapters in the Verse language book."""
    result = ["Available chapters in the Verse Language Book:"]
    result.append("=" * 50)
    for name, path in CHAPTERS.items():
        result.append(f"  {name:25s} -> {path}")
    result.append("")
    result.append("Use get_chapter(chapter_name) to read a specific chapter.")
    result.append("Use search_verse_docs(query) to search across all chapters.")
    return "\n".join(result)


@mcp.tool()
async def get_chapter(chapter_name: str) -> str:
    """Get the full content of a Verse book chapter.

    Args:
        chapter_name: The chapter name (e.g. 'failure', 'concurrency', 'classes-interfaces').
                      Use list_chapters() to see all available names.
    """
    chapter_name = chapter_name.lower().strip()

    if chapter_name in CHAPTERS:
        return await fetch_page(CHAPTERS[chapter_name])

    matches = [k for k in CHAPTERS if chapter_name in k or k in chapter_name]
    if len(matches) == 1:
        return await fetch_page(CHAPTERS[matches[0]])
    if matches:
        return f"Multiple matches: {', '.join(matches)}. Please be more specific."

    return f"Chapter '{chapter_name}' not found. Use list_chapters() to see available chapters."


@mcp.tool()
async def search_verse_docs(query: str) -> str:
    """Search across all Verse documentation chapters for a keyword or phrase.

    Args:
        query: The search term (e.g. 'decides', 'option type', 'transacts', 'spawn')
    """
    query_lower = query.lower()
    results = []

    tasks = {name: fetch_page(path) for name, path in CHAPTERS.items()}
    contents = {}
    for name, coro in tasks.items():
        try:
            contents[name] = await coro
        except Exception:
            continue

    for name, content in contents.items():
        content_lower = content.lower()
        if query_lower not in content_lower:
            continue

        lines = content.split("\n")
        matches = []
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                snippet = "\n".join(lines[start:end]).strip()
                if snippet and len(matches) < 5:
                    matches.append(snippet)

        if matches:
            results.append(f"\n## Chapter: {name}\n")
            for m in matches:
                results.append(f"  {m}\n")

    if not results:
        return f"No results found for '{query}' across the Verse documentation."

    header = f"Search results for '{query}':\n{'=' * 50}"
    return header + "\n".join(results)


@mcp.tool()
async def get_verse_home() -> str:
    """Get the home/introduction page of the Verse language book."""
    return await fetch_page("")


@mcp.tool()
async def cache_all_chapters() -> str:
    """Pre-download and cache all chapters for faster future searches.
    Run this once to speed up subsequent searches."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cached = 0
    errors = []

    for name, path in CHAPTERS.items():
        try:
            await fetch_page(path)
            cached += 1
        except Exception as e:
            errors.append(f"{name}: {e}")

    try:
        await fetch_page("")
        cached += 1
    except Exception:
        pass

    result = f"Cached {cached}/{len(CHAPTERS) + 1} pages."
    if errors:
        result += f"\nErrors: {'; '.join(errors)}"
    return result


@mcp.tool()
async def search_verse_api(query: str) -> str:
    """Search the Verse API digest for classes, functions, types, or modules.

    This searches the UEFN Verse API reference (verse_digest.md) which contains
    all module definitions, class signatures, function signatures, and type definitions.

    Args:
        query: The search term (e.g. 'inventory_component', 'fort_character',
               'creative_device', 'Subscribable', 'GetPlayspace')
    """
    query_lower = query.lower()
    content = _load_digest()
    lines = content.split("\n")
    results = []

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - 2)
            end = min(len(lines), i + 10)
            snippet = "\n".join(lines[start:end]).strip()
            if snippet and len(results) < 10:
                results.append(snippet)

    if not results:
        return f"No API results found for '{query}' in the Verse digest."

    header = f"Verse API results for '{query}':\n{'=' * 50}\n"
    return header + "\n\n---\n\n".join(results)


@mcp.tool()
async def get_verse_api_module(module_name: str) -> str:
    """Get the full API reference for a specific module or class from the Verse digest.

    Args:
        module_name: The module or section name (e.g. 'Itemization Module',
                     'SceneGraph Module', 'fort_character', 'creative_device').
                     Use list_verse_api_modules() to see all available sections.
    """
    sections = _parse_digest_sections()
    name_lower = module_name.lower().strip()

    for key, content in sections.items():
        if key.lower() == name_lower:
            return content

    matches = {k: v for k, v in sections.items() if name_lower in k.lower()}
    if len(matches) == 1:
        key = next(iter(matches))
        return matches[key]
    if matches:
        return (
            f"Multiple matches for '{module_name}':\n"
            + "\n".join(f"  - {k}" for k in matches)
            + "\n\nPlease be more specific."
        )

    return f"Section '{module_name}' not found. Use list_verse_api_modules() to see available sections."


@mcp.tool()
async def list_verse_api_modules() -> str:
    """List all modules and sections available in the Verse API digest."""
    sections = _parse_digest_sections()
    result = ["Verse API Digest - Available sections:", "=" * 50]
    for key in sections:
        if key == "header" or key == "Table of Contents":
            continue
        line_count = len(sections[key].split("\n"))
        result.append(f"  {key} ({line_count} lines)")
    result.append("")
    result.append("Use get_verse_api_module(name) to read a specific section.")
    result.append("Use search_verse_api(query) to search across the entire API.")
    return "\n".join(result)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
