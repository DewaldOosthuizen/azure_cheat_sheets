# DewaldOosthuizen/azure_cheat_sheets

Quick-reference study notes for Azure architecture decisions, aimed primarily
at candidates preparing for AZ-305: Designing Microsoft Azure Infrastructure
Solutions. The content focuses on service selection, architectural trade-offs,
and decision reasoning — not step-by-step walkthroughs or portal labs.

## Repository Structure

```
docs/AZ-305_CheatSheet.md   — the single main cheat sheet
```

The cheat sheet is organized into ten top-level sections:

1. Networking
2. Security
3. Storage
4. Monitoring & Observability
5. Compute
6. Identity & Access
7. High Availability & Disaster Recovery
8. Governance
9. Messaging & Integration
10. Well-Architected Framework

## Exam Overlap

| Exam   | Focus         | Relevant Sections |
|--------|---------------|-------------------|
| AZ-900 | Fundamentals  | Networking (overview), Storage, Compute, Identity & Access (Entra basics) |
| AZ-104 | Administrator | All sections — administrator-level depth on RBAC, Networking, HA & DR; Messaging & Integration (partial — Service Bus, Event Hub namespace admin) |
| AZ-305 | Architect     | All sections including Messaging & Integration and Well-Architected Framework |
| AZ-500 | Security Engineer | Security (full), Identity & Access (full), Networking (partial), Monitoring & Observability (partial), Governance (partial) |
| AZ-700 | Network Engineer | Networking (full), High Availability & Disaster Recovery (partial) |

## Orientation for AI Agents

This is a documentation-only repository. There is no application code, no
build system, and no test suite. All meaningful content lives in
docs/AZ-305_CheatSheet.md.

When asked to add or update content:

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

- Do not document features or claims not already reflected in the content.

For pull requests, scope changes to one improvement area, explain what section
changed, and verify that Markdown and Mermaid blocks render cleanly on GitHub.
Run `npx markdownlint-cli2 "**/*.md"` locally before opening a PR to catch
formatting violations before CI runs them.
Run `python3 scripts/validate_mermaid.py docs/AZ-305_CheatSheet.md` to
validate Mermaid diagrams locally. Requires `mmdc` — install once with
`npm install -g @mermaid-js/mermaid-cli`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style, local
checks, content conventions, and the PR checklist.

## Mermaid Diagrams

GitHub renders Mermaid natively. For local preview, install the
"Markdown Preview Mermaid Support" extension in VS Code.

<!-- graph-tools-start -->

## Code Exploration

### understand-anything

.understand-anything/knowledge-graph.json is present.
Use it for layered architecture questions (layers, communities, entry points).

> **Regeneration note:** After any `understand-anything` run that creates or
> regenerates `.understand-anything/knowledge-graph.json`, perform a global
> find-and-replace of `AZ-204` → `AZ-305` across the entire file before
> committing it. The generator may propagate an incorrect exam code to
> `project.description`, the cheat-sheet node summary, the guided-tour
> description, and tour-step fields. A single-field patch is insufficient.

```bash
# Launch the interactive dashboard
cd ~/.understand-anything-plugin/packages/dashboard
GRAPH_DIR=$(pwd) npx vite --host 127.0.0.1
```

For prose questions load the skill:

```text
skill: understand-chat
```

### codegraph

.codegraph/ is present. Use it FIRST for any symbol lookup,
call tracing, or targeted context gathering before opening source files.

```bash
codegraph context "<task description>" -p .   # focused file+symbol context
codegraph query "<ClassName or function>" -p . # where is X defined / used
codegraph affected <changed-files> -p .        # which tests are affected
codegraph sync .                               # after any code change
```

Decision order for code tasks:

1. codegraph context       — which symbols matter?
2. understand-anything     — where in the architecture does this live?
3. Read raw source         — only the 1-2 files that actually matter.

### graphify

graphify-out/ not yet generated for this repo.

<!-- graph-tools-end -->

## License

GPL-3.0 — see LICENSE.
