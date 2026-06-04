# Contributing to Azure Cheat Sheets

Thank you for contributing. This guide covers the full workflow for making
clean, reviewable contributions to this repository.

---

## Table of Contents

1. [Code of Conduct](#1-code-of-conduct)
2. [Getting Started](#2-getting-started)
3. [Picking Up an Issue](#3-picking-up-an-issue)
4. [Branch Naming](#4-branch-naming)
5. [Development Setup](#5-development-setup)
6. [Running Checks Locally](#6-running-checks-locally)
7. [Commit Message Style](#7-commit-message-style)
8. [Pull Request Process](#8-pull-request-process)
9. [Coding Standards](#9-coding-standards)
10. [Deprecation warnings](#10-deprecation-warnings)

---

## 1. Code of Conduct

Be respectful, constructive, and collaborative. Contributions that are
disrespectful, dismissive, or harmful will not be accepted.

---

## 2. Getting Started

1. Fork the repository.
2. Clone your fork locally.
3. Follow the [Development Setup](#5-development-setup) section below.

---

## 3. Picking Up an Issue

**Before you write a single line of content or code:**

1. Browse the [GitHub Issues](https://github.com/DewaldOosthuizen/azure-cheat-sheets/issues) tab and find an issue you want to work on.
2. **Assign the issue to yourself** before starting any work.
   Go to the issue page → Assignees (right sidebar) → assign yourself.
   This signals to all other contributors that the issue is claimed.
3. Leave a comment on the issue stating you are picking it up and your
   intended approach — especially for larger changes.
4. Only then create your branch and begin work.

> Why this matters: two contributors working on the same issue in parallel
> wastes effort and creates painful merge conflicts. A self-assignment takes
> five seconds and saves hours.

If you were assigned an issue but can no longer work on it, unassign yourself
and leave a comment so someone else can pick it up.

---

## 4. Branch Naming

| Prefix     | Pattern                         | When to use                                |
|------------|---------------------------------|--------------------------------------------|
| `feature/` | `feature/<issue-id>-<topic>`    | New cheat sheet section or capability      |
| `fix/`     | `fix/<issue-id>-<topic>`        | Correction to existing content             |
| `chore/`   | `chore/<topic>`                 | Tooling, deps, CI, config updates          |
| `docs/`    | `docs/<topic>`                  | Meta-documentation (README, CONTRIBUTING)  |

Examples:

- `feature/42-networking-private-endpoints`
- `fix/17-storage-redundancy-table`
- `docs/update-contributing-guide`

Always branch from `main`.

---

## 5. Development Setup

You need `node` and `npm` on your PATH, and **Python 3.11+** for script
validation and linting.

Install all Python dev dependencies (pytest, pytest-cov, ruff) declared in
`pyproject.toml` via the editable install:

```bash
pip install -e '.[dev]'
```

Install the Node dev dependencies declared in `package.json`:

```bash
npm ci
```

This installs `markdownlint-cli2` (linter) and `@mermaid-js/mermaid-cli` (`mmdc`).

Install the pre-commit hooks (one-time setup per clone):

```bash
pip install pre-commit
pre-commit install
```

The hooks run automatically on `git commit` and enforce the same ruff and
markdownlint checks that CI applies on push.

---

## 6. Running Checks Locally

Run these commands from the repository root before pushing, or rely on the
pre-commit hooks installed in [Section 5](#5-development-setup) to run them
automatically on each commit. CI applies the same checks and a failing PR will
not be reviewed.

Lint all Markdown files:

```bash
npx markdownlint-cli2 "**/*.md"
```

Validate all Mermaid diagram blocks:

```bash
python3 scripts/validate_mermaid.py docs/*.md
```

`validate_mermaid.py` exit codes:

| Exit code | Meaning |
|-----------|---------|
| `0` | All diagrams passed validation (or no diagrams found — see note below). |
| `1` | One or more diagrams failed validation, or a specified file was not found. |
| `2` | `mmdc` is not installed or not on `PATH`. Install with `npm install -g @mermaid-js/mermaid-cli`. |

> **Exam tip:** When no Mermaid blocks are found the script emits a WARNING to
> stderr and exits `0` — it does not treat missing diagrams as an error (exit 2).

Lint Python scripts:

```bash
ruff check scripts/ tests/
Run ruff format --check scripts/ tests/
```

Run tests:

```bash
pytest tests/ -v
```

Audit Python dependencies for known CVEs:

```bash
pip-audit
```

All commands must exit with code `0` before opening a PR.

---

## 7. Commit Message Style

- Use the **imperative mood** in the subject line: "Add", "Fix", "Remove".
- Limit the subject line to **72 characters**.
- Leave one blank line between the subject and body when a body is needed.
- Reference the related issue in the footer with `Closes #<n>`.

Example:

```
Add Azure Private Endpoint decision flowchart

Closes #42
```

---

## 8. Pull Request Process

1. Ensure all local checks pass (see [Section 6](#6-running-checks-locally)).
2. Open the PR against `main`.
3. Use a scoped, descriptive title: `fix: resolve #17 - correct storage redundancy table`.
4. In the PR body:
   - Link the issue: `Closes #<n>`
   - Describe the user-visible change.
   - Include screenshots for diagram or layout changes.
5. Request a review. Do not merge your own PR without a review.
6. Address review feedback with follow-up commits — do not force-push a reviewed branch unless asked.

---

## 9. Coding Standards

### Content Style

- Keep explanations concise and comparison-oriented.
- Section headings: top-level domain names in ALL CAPS (`# NETWORKING`).
  Sub-topics as `##`. Do not use Title Case for top-level section headings.
- Prefer tables when comparing Azure services, tiers, or design options.
  Use these column templates:

  Networking / compute services:
  `| Service | Layer | Scope | Use Case | Key Feature |`

  Data / storage services:
  `| Service | Type | Best For | Key Feature |`

  Consistency columns (always present): Service, Key Feature.
  Do not add free-form columns not in the template above.

### Python Scripts

- Follow PEP 8. Use `ruff` for linting and formatting.
- Keep scripts small and single-purpose.
- Add or update tests in `tests/` whenever script behaviour changes.

---

## 10. Deprecation warnings

Use a deprecation callout immediately after the affected table row or section heading when a service
is retired, retiring, or superseded. Format:

> **⚠️ Deprecation warning:** \<Service\> is retired / retiring \<date if known\>. Migrate to
> \<replacement\>. See: [announcement link]

Rules:

- Place the callout directly after the table that contains the deprecated service.
- Always name the recommended replacement.
- Include the retirement date when officially announced.
- Do NOT use the exam-tip format for deprecation notices — they serve different purposes.

---

## 11. Dependabot update strategy

Dependabot monitors three ecosystems on a weekly schedule:

| Ecosystem       | Scope                                      | Grouping                  |
|-----------------|--------------------------------------------|---------------------------|
| `github-actions`| CI action versions in `.github/workflows/` | Individual PRs (no group) |
| `npm`           | Node dev deps (`markdownlint-cli2`, `mmdc`) | Single grouped PR         |
| `pip`           | Python dev deps (`ruff`, `pytest`, etc.)   | Single grouped PR         |

Both `npm` and `pip` bumps are batched into a single PR via a `groups: dev-dependencies`
block with pattern `"*"` in `.github/dependabot.yml`. This prevents reviewer fatigue from
a flood of individual version-bump PRs.

The `pip` entry additionally specifies `target-branch: main` to avoid branch-mismatch
issues when the default branch resolution differs from the intended merge target.

Do not remove the `groups` or `target-branch` fields from `.github/dependabot.yml` during
maintenance — their absence would revert to ungrouped, potentially noisy Dependabot PRs.
