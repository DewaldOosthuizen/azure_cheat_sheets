# GitHub Copilot Instructions — azure_cheat_sheets

## Project Overview

This repository contains quick-reference study notes for Azure architecture
decisions. It is aimed at candidates preparing for AZ-305: Designing Microsoft
Azure Infrastructure Solutions. The focus is service selection, architectural
trade-offs, and decision reasoning — not step-by-step walkthroughs, portal
screenshots, or hands-on labs.

There is no application code, no build system, and no test suite. All
meaningful content lives in a single Markdown file.

## Repository Structure

    docs/Azure-CheatSheet.md   — the single main cheat sheet

The cheat sheet is organized into eight top-level sections:

1. Networking
2. Security
3. Storage
4. Monitoring & Observability
5. Compute
6. Identity & Access
7. High Availability & Disaster Recovery
8. Governance

Supporting files:

    scripts/validate_mermaid.py   — CI script that validates Mermaid code blocks
    config/orchestrator.yml       — workspace-orchestrator pipeline config

## Content Guidelines

When adding or editing content, follow these rules:

- Keep explanations concise and comparison-oriented.
- Prefer tables when comparing Azure services, tiers, or design options.
- Use Mermaid diagrams for branching decision flows where a visual aid is more
  useful than prose alone.
- Use short exam-tip callouts only when they clarify a likely decision point.
- Do not document features or claims not already reflected in the content.
- Scope pull requests to one improvement area where possible.
- Verify that Markdown formatting and Mermaid blocks render cleanly on GitHub.

## Mermaid Diagrams

GitHub renders Mermaid natively. For local preview, install the
"Markdown Preview Mermaid Support" extension in VS Code.

The CI lint workflow runs `scripts/validate_mermaid.py` to catch broken
Mermaid blocks before merge.

## Code Exploration

Two analysis tool artifacts are present. Use them before opening raw source.

### codegraph

    codegraph context "<task description>" -p .   # focused file+symbol context
    codegraph query "<symbol>" -p .               # where is X defined / used
    codegraph sync .                              # after any content change

### understand-anything

    # Interactive dashboard
    cd ~/.understand-anything-plugin/packages/dashboard
    GRAPH_DIR=$(pwd) npx vite --host 127.0.0.1

Knowledge graph: `.understand-anything/knowledge-graph.json`
Use for layered architecture questions (layers, communities, entry points).

Decision order for content tasks:

1. codegraph context  — which symbols or sections matter?
2. understand-anything — where in the structure does this live?
3. Read raw source — only the file(s) that actually matter.

## License

GPL-3.0 — see LICENSE.
