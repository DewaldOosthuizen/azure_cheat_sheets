# Azure Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)

Quick-reference study notes for Azure architecture decisions, with tables and
Mermaid diagrams that compare services by tradeoff, scope, and common exam
scenarios.

## Purpose

This repository is an exam-prep reference, not a step-by-step tutorial. The
documents focus on choosing the right Azure service for a requirement and
understanding why that choice fits.

## Target Audience and Scope

The current content is aimed primarily at candidates preparing for
`AZ-305: Designing Microsoft Azure Infrastructure Solutions`.

Coverage is strongest where the exam expects architectural comparison and
decision-making. Configuration walkthroughs, portal screenshots, and hands-on
labs are intentionally out of scope. Other Azure exams may overlap with parts
of this material, but the repository is not yet organized around those tracks.

## Repository Structure

- [`docs/Azure-CheatSheet.md`](docs/Azure-CheatSheet.md) - the main cheat sheet
  for Azure infrastructure design topics.

The current cheat sheet is organized into these top-level sections:

1. Networking
2. Security
3. Storage
4. Monitoring & Observability
5. Compute
6. Identity & Access
7. High Availability & Disaster Recovery
8. Governance

## Viewing Mermaid Diagrams

The cheat sheet includes Mermaid flowcharts for service-selection patterns.

- GitHub renders Mermaid diagrams natively in Markdown files.
- VS Code users can install
  `Markdown Preview Mermaid Support` to render diagrams in the editor preview.
- Other local Markdown viewers may show the code block only unless Mermaid
  rendering is enabled.

## Contributing

Contributions should keep the repository useful as a quick study and
decision-reference tool.

When editing or adding material:

- Keep explanations concise and comparison-oriented.
- Prefer tables when comparing Azure services, tiers, or design options.
- Use short exam-tip callouts only when they clarify a likely decision point.
- Use Mermaid diagrams for branching decision flows where a visual aid is more
  useful than prose alone.
- Avoid documenting features or claims that are not yet reflected in the
  repository content.

For pull requests:

- Keep changes scoped to one improvement area where possible.
- Explain what section changed and why it improves the cheat sheet for readers.
- Verify that Markdown formatting and Mermaid blocks still render cleanly on
  GitHub.

## License

This project is licensed under the [`GPL-3.0`](LICENSE).
