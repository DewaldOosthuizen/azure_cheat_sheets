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

```
docs/AZ-305_CheatSheet.md   — the single main cheat sheet
scripts/validate_mermaid.py — CI script that validates Mermaid code blocks
config/orchestrator.yml     — workspace-orchestrator pipeline config
openspec/                   — openspec change workflow artefacts (proposals,
                              specs, impls, archive)
```

The cheat sheet is organized into eight top-level sections:

1. Networking
2. Security
3. Storage
4. Monitoring & Observability
5. Compute
6. Identity & Access
7. High Availability & Disaster Recovery
8. Governance

## Content Guidelines

When adding or editing content, follow these rules precisely:

- Keep explanations concise and comparison-oriented.
- Section headings: top-level domain names in ALL CAPS (`# NETWORKING`).
  Sub-topics as `##`. Do not use Title Case for top-level section headings.
- Prefer tables when comparing Azure services, tiers, or design options.
  Use these column templates:

  Networking / compute services:
  | Service | Layer | Scope | Use Case | Key Feature |

  Data / storage services:
  | Service | Type | Best For | Key Feature |

  Consistency columns (always present): Service, Key Feature.
  Do not add free-form columns not in the template above.

- Use short exam-tip callouts only when they clarify a likely decision point.
  Place the callout immediately after the relevant table, using this format:

  > **Exam tip:** Choose Azure Front Door when the requirement mentions
  > global HTTP load balancing, WAF, or SSL offload at the edge.

  Do not use plain blockquotes, bold sentences, or note/warning admonitions
  for exam tips.

- Use Mermaid diagrams for branching decision flows. Choose the directive by
  purpose:

  | Purpose                        | Directive       |
  |--------------------------------|-----------------|
  | Decision flows (if/else trees) | flowchart TD    |
  | Hierarchy / ecosystem maps     | graph TD        |
  | Connectivity / network paths   | graph LR        |

  Example:

  ```mermaid
  flowchart TD
      A[Need load balancing?] -->|Global HTTP| B[Azure Front Door]
      A -->|Regional TCP/UDP| C[Azure Load Balancer]
  ```

- Do not document features or claims not already reflected in the content.
- Scope pull requests to one improvement area where possible.
- Run `npx markdownlint-cli2 "**/*.md"` locally before opening a PR.
- Run `python3 scripts/validate_mermaid.py docs/AZ-305_CheatSheet.md` to
  validate Mermaid diagrams locally. Requires `mmdc` — install once with
  `npm install -g @mermaid-js/mermaid-cli`.
- Verify that Markdown formatting and Mermaid blocks render cleanly on GitHub.

## Mermaid Diagrams

GitHub renders Mermaid natively. For local preview, install the
"Markdown Preview Mermaid Support" extension in VS Code.

The CI lint workflow runs `scripts/validate_mermaid.py` to catch broken
Mermaid blocks before merge.

## Code Exploration

Two analysis tool artefacts are present. Use them before opening raw source.

### codegraph

```bash
codegraph context "<task description>" -p .   # focused file+symbol context
codegraph query "<symbol>" -p .               # where is X defined / used
codegraph sync .                              # after any content change
```

### understand-anything

```bash
# Interactive dashboard
cd ~/.understand-anything-plugin/packages/dashboard
GRAPH_DIR=$(pwd) npx vite --host 127.0.0.1
```

Knowledge graph: `.understand-anything/knowledge-graph.json`
Use for layered architecture questions (layers, communities, entry points).

**Regeneration note:** After any `understand-anything` run that creates or
regenerates `.understand-anything/knowledge-graph.json`, perform a global
find-and-replace of `AZ-204` → `AZ-305` across the entire file before
committing. The generator may propagate an incorrect exam code to
`project.description`, the cheat-sheet node summary, the guided-tour
description, and tour-step fields. A single-field patch is insufficient.

Decision order for content tasks:

1. codegraph context       — which symbols or sections matter?
2. understand-anything     — where in the structure does this live?
3. Read raw source         — only the file(s) that actually matter.

## License

GPL-3.0 — see LICENSE.
