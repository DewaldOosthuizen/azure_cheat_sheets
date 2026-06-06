# Tech Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/DewaldOosthuizen1)

You can view the live site at [![Live Site](https://img.shields.io/badge/Live%20Site-tech--cheat--sheets.vercel.app-black?logo=vercel&logoColor=white)](https://tech-cheat-sheets.vercel.app)

Quick-reference study notes for Azure architecture decisions, with tables and
Mermaid diagrams that compare services by tradeoff, scope, and common exam
scenarios.

## Purpose

This repository is an exam-prep reference, not a step-by-step tutorial. The
documents focus on choosing the right Azure service for a requirement and
understanding why that choice fits.

## Repository Structure

```
docs/
  azure/
    cheat_sheets/
      AZ-305.md                 — AZ-305 architect-focused cheat sheet
      AZ-104.md                 — AZ-104 administrator-focused cheat sheet
    diagrams/<section>/         — standalone Mermaid diagram sources (one per file)
      <slug>.mmd                — exam-agnostic slug
    files/<section>/            — shared section snippet files
      <section>.md              — e.g. networking/networking.md
  index.md                      — MkDocs site home page
mkdocs.yml                      — MkDocs Material site configuration
```

Section directories under `docs/azure/diagrams/` and `docs/azure/files/`:
`networking`, `security`, `storage`, `monitoring`, `compute`, `identity`,
`ha-dr`, `governance`, `messaging`, `waf`

## Viewing the Documentation Site

The recommended way to read the cheat sheets is through the MkDocs Material
site, which renders all Mermaid diagrams inline in the browser.

Serve it locally (hot-reload on save):

```bash
make docs-serve   # opens http://127.0.0.1:8000
```

Build a static copy:

```bash
make docs-build   # output in site/
```

GitHub also renders Mermaid natively in Markdown files. VS Code users can
install `Markdown Preview Mermaid Support` to render diagrams in the editor
preview.

When editing or adding material:

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
  Do not add free-form columns not in the template above. If an other type of
  comparison is needed, consider whether a Mermaid diagram would be more effective.
  Otherwise document the table structure below the table section above, and apply
  it consistently across the cheat sheet where a similar comparison is needed.

- Use short exam-tip callouts only when they clarify a likely decision point.
  Format: place the callout immediately after the relevant table, using:

  > **Exam tip:** Choose Azure Front Door when the requirement mentions
  > global HTTP load balancing, WAF, or SSL offload at the edge.

  Do not use plain blockquotes, bold sentences, or note/warning admonitions
  for exam tips.

- For retired, retiring, or superseded services, use a deprecation callout
  instead of an exam-tip. See the [Deprecation warnings](CONTRIBUTING.md#10-deprecation-warnings)
  section in CONTRIBUTING.md for the required format.

- Use Mermaid diagrams for branching decision flows where a visual aid is more
  useful than prose alone. Each diagram lives in its own
  `docs/azure/diagrams/<section>/<slug>.mmd` file and is referenced from the
  cheat sheet via a PyMdown Snippets directive:

  ```text
  ```mermaid
  --8<-- "azure/diagrams/<section>/<slug>.mmd"
  ``` (closing backticks)
  ```

  The `.mmd` file is the single source of truth — the same file can be
  referenced from multiple cheat sheets. Run `make mermaid-check` after adding
  or editing any `.mmd` file. Choose the directive by purpose:

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

For pull requests:

- Keep changes scoped to one improvement area where possible.
- Explain what section changed and why it improves the cheat sheet for readers.
- Run `make install` once after cloning to create the `.venv` and install
  all Python and Node dev dependencies.
- Run `make ci` locally before opening a PR — it replicates the full CI
  pipeline (markdownlint, Mermaid validation, ruff lint + format check,
  pytest with coverage, MkDocs strict build).
- Verify that Markdown formatting and Mermaid diagrams render correctly via
  `make docs-serve` before submitting.
  
## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for
the full workflow, including how to pick up an issue, branch naming conventions,
local validation steps, and the pull request process.

## License

This project is licensed under the [`GPL-3.0`](LICENSE).
