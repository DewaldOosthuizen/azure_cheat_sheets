# Azure Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=RVJC5VUM5ZEW8&source=url)

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

### Exam Overlap

| Exam | Focus | Relevant Sections |
|------|-------|-------------------|
| AZ-900 | Fundamentals | Networking (overview), Storage, Compute, Identity & Access (Entra basics) |
| AZ-104 | Administrator | All sections — administrator-level depth on RBAC, Networking, HA & DR; Messaging & Integration (partial — Service Bus, Event Hub namespace admin) |
| AZ-305 | Architect | All sections including Messaging & Integration and Well-Architected Framework |

## Repository Structure

- [`docs/AZ-305_CheatSheet.md`](docs/AZ-305_CheatSheet.md) - the main cheat sheet
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style, local
checks, content conventions, and the PR checklist.

## License

This project is licensed under the [`GPL-3.0`](LICENSE).
