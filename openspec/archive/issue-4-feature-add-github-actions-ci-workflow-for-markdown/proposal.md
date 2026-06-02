# Proposal: Issue #4 — Add GitHub Actions CI Workflow for Markdown Linting

## Overview

The repository has no CI pipeline, which means broken Markdown tables, invalid
heading hierarchies, and malformed Mermaid diagram syntax can be merged silently.
The fix is a lightweight GitHub Actions workflow that runs markdownlint across
all `.md` files and validates all 7 Mermaid diagram blocks in
`docs/Azure-CheatSheet.md` on every push and pull request, accompanied by a
`.markdownlint.json` config that suppresses rules conflicting with the existing
table style, a `scripts/validate_mermaid.py` helper that extracts and validates
each diagram block, and a CI status badge in `README.md`.

## Issues

### Issue 1

**File:** `.github/workflows/lint.yml` (new file)
**Problem:** No CI workflow exists. Markdown formatting errors and malformed
Mermaid diagrams are not caught automatically.
**Fix:** Create the workflow with two jobs: `markdownlint` (using
`DavidAnson/markdownlint-cli2-action@v16` against `**/*.md`) and
`mermaid-check` (Node 20, `@mermaid-js/mermaid-cli`, driven by
`scripts/validate_mermaid.py`). Both jobs trigger on `push` and
`pull_request`.

### Issue 2

**File:** `.markdownlint.json` (new file)
**Problem:** Running markdownlint without configuration will raise false
positives for the existing GFM table style and heading conventions already
present in the cheat sheet.
**Fix:** Add a `.markdownlint.json` at the repo root with targeted rule
overrides (e.g. `MD013` line-length off, `MD033` inline-HTML off) so only
genuine formatting errors fail CI.

### Issue 3

**File:** `scripts/validate_mermaid.py` (new file)
**Problem:** The proposed workflow needs a script to extract each fenced
` ```mermaid ` block from `docs/Azure-CheatSheet.md` and invoke `mmdc` to
validate syntax, exiting non-zero if any diagram fails.
**Fix:** Write a Python 3 script that parses the Markdown file, writes each
diagram block to a temp file, calls `mmdc --input <tmp>`, and aggregates
failures. The script must report which diagram number failed and exit 1 if
any validation fails.

### Issue 4

**File:** `README.md`
**Problem:** No CI status badge exists, so readers and contributors cannot
see whether the main branch is passing lint.
**Fix:** Add a GitHub Actions badge for the `lint.yml` workflow immediately
below the first `# Azure Cheat Sheets` heading on line 1.

Before:

```markdown
# Azure Cheat Sheets

Quick-reference study notes for Azure architecture decisions...
```

After:

```markdown
# Azure Cheat Sheets

![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)

Quick-reference study notes for Azure architecture decisions...
```
