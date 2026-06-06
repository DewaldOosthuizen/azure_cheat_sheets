# Tech Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/DewaldOosthuizen1)

Quick-reference study notes for technology certifications and architecture decisions.
Each sheet answers *which service, which pattern, and why* — not how to click through a portal.
Content is comparison-oriented: tables, decision flowcharts, and Mermaid diagrams side-by-side.

---

## Microsoft Azure

Organised by domain. Each section covers service selection and architectural trade-offs across
multiple Azure exams.

| Exam | Focus | Cheat Sheet |
|------|-------|-------------|
| AZ-305 | Architect — infrastructure design decisions | [AZ-305](azure/cheat_sheets/AZ-305.md) |
| AZ-104 | Administrator — operational depth | [AZ-104](azure/cheat_sheets/AZ-104.md) |

Both cheat sheets share the same domain sections, each with relevant overlap noted inline:

- Networking
- Security
- Storage
- Monitoring & Observability
- Compute
- Identity & Access
- High Availability & Disaster Recovery
- Governance
- Messaging & Integration
- Well-Architected Framework

Exam coverage per section:

| Section | AZ-900 | AZ-104 | AZ-305 | AZ-500 | AZ-700 |
|---------|--------|--------|--------|--------|--------|
| Networking | Partial | Full | Full | Partial | Full |
| Security | — | Partial | Full | Full | — |
| Storage | Partial | Full | Full | — | — |
| Monitoring & Observability | — | Partial | Full | Partial | — |
| Compute | Partial | Full | Full | — | — |
| Identity & Access | Partial | Full | Full | Full | — |
| High Availability & DR | — | Full | Full | — | Partial |
| Governance | — | Partial | Full | Partial | — |
| Messaging & Integration | — | — | Full | — | — |
| Well-Architected Framework | — | — | Full | — | — |

---

## How to Use These Sheets

The cheat sheets are not meant to be read cover-to-cover. Jump to the section relevant to what
you are studying. Each section contains:

- A comparison table of services in that domain
- Exam-tip callouts that highlight common decision points in exam questions
- One or more Mermaid decision flowcharts for branching "which service?" scenarios
- Deprecation notices where a service has been retired or superseded

The live site renders all diagrams inline. To browse locally, run `make docs-serve`.

---

## Contributing

See [CONTRIBUTING.md](https://github.com/DewaldOosthuizen/azure_cheat_sheets/blob/main/CONTRIBUTING.md)
for the full contributor workflow.

## License

This project is licensed under the [`GPL-3.0`](LICENSE).
