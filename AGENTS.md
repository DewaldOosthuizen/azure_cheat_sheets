# DewaldOosthuizen/azure_cheat_sheets

Quick-reference study notes for Azure architecture decisions, aimed primarily
at candidates preparing for AZ-305: Designing Microsoft Azure Infrastructure
Solutions. The content focuses on service selection, architectural trade-offs,
and decision reasoning — not step-by-step walkthroughs or portal labs.

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

## Orientation for AI Agents

This is a documentation-only repository. There is no application code, no
build system, and no test suite. All meaningful content lives in
docs/Azure-CheatSheet.md.

When asked to add or update content:

- Keep explanations concise and comparison-oriented.
- Prefer tables when comparing Azure services, tiers, or design options.
- Use Mermaid diagrams for branching decision flows.
- Use short exam-tip callouts only when they clarify a likely decision point.
- Do not document features or claims not already reflected in the content.

For pull requests, scope changes to one improvement area, explain what section
changed, and verify that Markdown and Mermaid blocks render cleanly on GitHub.

## Mermaid Diagrams

GitHub renders Mermaid natively. For local preview, install the
"Markdown Preview Mermaid Support" extension in VS Code.

<!-- graph-tools-start -->

## Code Exploration

### understand-anything

.understand-anything/knowledge-graph.json is present.
Use it for layered architecture questions (layers, communities, entry points).

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
