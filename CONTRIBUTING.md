# Contributing

Thank you for contributing to the Azure Cheat Sheets repository. This guide
covers everything you need to make a clean, reviewable contribution.

## Prerequisites

You need `node` and `npm` on your PATH. No Python, ruff, or pytest is required
— this is a documentation-only repository.

## Local Setup

Install the dev dependencies declared in `package.json`:

```bash
npm ci
```

This installs `markdownlint-cli2` (linter) and `@mermaid-js/mermaid-cli` (`mmdc`).

## Running Checks Locally

Run these commands from the repository root before opening a PR.

Lint all Markdown files:

```bash
npx markdownlint-cli2 "**/*.md"
```

Validate a Mermaid diagram block (replace the input path as needed):

```bash
mmdc -i docs/AZ-305_CheatSheet.md -o /dev/null
```

Both commands must exit cleanly (exit code 0) before pushing.

## Branch Naming

| Prefix | Pattern | When to use |
|--------|---------|-------------|
| `feature/` | `feature/<section>-<topic>` | New content or new capability |
| `fix/` | `fix/<section>-<topic>` | Correction to existing content |
| `docs/` | `docs/<topic>` | Meta-documentation (README, CONTRIBUTING, etc.) |

Examples: `feature/networking-private-endpoints`, `fix/storage-redundancy-table`,
`docs/update-contributing-guide`.

## Commit Message Style

- Use the **imperative mood** in the subject line ("Add", "Fix", "Remove").
- Limit the subject line to **72 characters**.
- Leave one blank line between the subject and the body (if a body is needed).
- Reference the related issue in the footer with `#<n>`.

Example:

```
Add Azure Private Endpoint decision flowchart

Closes #42
```

## Content Style Rules

The rules below apply to all content in `docs/`.

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
  Format: place the callout immediately after the relevant table, using:

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

  Example decision flow:

  ```mermaid
  flowchart TD
      A[Need load balancing?] -->|Global HTTP| B[Azure Front Door]
      A -->|Regional TCP/UDP| C[Azure Load Balancer]
  ```

- Avoid documenting features or claims that are not yet reflected in the
  repository content.

## PR Checklist

Before requesting review, confirm each item:

- [ ] `npx markdownlint-cli2 "**/*.md"` passes with no violations.
- [ ] All Mermaid diagrams render correctly on GitHub.
- [ ] Change is scoped to one improvement area.
- [ ] README or CONTRIBUTING updated if any conventions changed.
