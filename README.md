# verse-mcp

MCP server for [Verse language](https://verselang.github.io/book/) documentation and the UEFN API reference. Built for use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Tools provided

| Tool | Description |
|------|-------------|
| `list_chapters` | List all chapters in the Verse language book |
| `get_chapter` | Read a specific chapter |
| `search_verse_docs` | Search across all chapters |
| `get_verse_home` | Get the book introduction page |
| `cache_all_chapters` | Pre-download all chapters for faster searches |
| `search_verse_api` | Search the UEFN Verse API digest |
| `get_verse_api_module` | Get full API reference for a module/class |
| `list_verse_api_modules` | List all modules in the API digest |

## Install

### Claude Code (recommended)

```bash
claude mcp add verse-docs -- uvx --from git+https://github.com/BurgersJackson/verse-mcp verse-mcp
```

Replace `BurgersJackson` with the GitHub username or org where the repo is hosted.

### pip

```bash
pip install git+https://github.com/BurgersJackson/verse-mcp.git
verse-mcp
```

### Local development

```bash
git clone https://github.com/BurgersJackson/verse-mcp.git
cd verse-mcp
pip install -e .
verse-mcp
```

## Configuration

- **`VERSE_DIGEST_PATH`** — Override the bundled API digest with a custom file path:
  ```bash
  VERSE_DIGEST_PATH=/path/to/my/verse_digest.md verse-mcp
  ```

- **`VERSE_MCP_CACHE_DIR`** — Override the default cache directory for fetched docs:
  ```bash
  VERSE_MCP_CACHE_DIR=/tmp/verse-cache verse-mcp
  ```

## CLAUDE.md snippet

Add this to your project's `CLAUDE.md` to instruct Claude to use the Verse docs tools:

```markdown
## Verse Language Support

When working with Verse code (.verse files, UEFN projects):

1. Always use the `verse-docs` MCP tools before writing non-trivial Verse code.
   - `search_verse_docs` for language syntax and patterns
   - `get_chapter` for specific language features
   - `search_verse_api` for UEFN API classes, methods, and types
   - `get_verse_api_module` for full module/class definitions
2. On first use in a session, run `cache_all_chapters` to pre-download docs.
3. When using UEFN APIs, always verify class names and method signatures with `search_verse_api`.
```
