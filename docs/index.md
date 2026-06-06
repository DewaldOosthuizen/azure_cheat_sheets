# Tech Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/DewaldOosthuizen1)

Quick-reference study notes for technology certifications and architecture decisions.
Each sheet answers *which service, which pattern, and why* — not how to click through a portal.
Content is comparison-oriented: tables, decision flowcharts, and Mermaid diagrams side-by-side.

---

## Microsoft Azure

Organised by domain. Each section covers service selection and architectural trade-offs.

| Domain | Content |
|--------|---------|
| [Networking](azure/files/networking/networking.md) | Load balancers, APIM, VNet, DNS, NSG, DDoS, CDN |
| [Security](azure/files/security/security.md) | Defender for Cloud, Key Vault, Sentinel, Encryption |
| [Storage](azure/files/storage/storage.md) | Blob, Files, Disk, SQL, Cosmos DB, redundancy |
| [Monitoring & Observability](azure/files/monitoring/monitoring.md) | Azure Monitor, Log Analytics, Alerts, Agents |
| [Compute](azure/files/compute/compute.md) | VMs, App Service, Functions, AKS, ACI, Batch |
| [Identity & Access](azure/files/identity/identity.md) | Entra ID, RBAC, PIM, Hybrid Identity |
| [High Availability & DR](azure/files/ha-dr/ha-dr.md) | ASR, Azure Backup, Availability Zones |
| [Governance](azure/files/governance/governance.md) | Policy, Blueprints, Management Groups, Cost |
| [Messaging & Integration](azure/files/messaging/messaging.md) | Service Bus, Event Grid, Logic Apps, Functions |
| [Well-Architected Framework](azure/files/waf/waf.md) | Five pillars, trade-off navigator |

Exam coverage by domain:

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
