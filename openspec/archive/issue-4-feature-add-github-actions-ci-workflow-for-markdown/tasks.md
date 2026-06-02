# Tasks: Issue #4

## Workflow

- [ ] Create `.github/workflows/lint.yml` with `markdownlint` job using `DavidAnson/markdownlint-cli2-action@v16` targeting `**/*.md`
- [ ] Add `mermaid-check` job to `lint.yml` using Node 20 and `@mermaid-js/mermaid-cli`
- [ ] Wire `mermaid-check` job to call `python3 scripts/validate_mermaid.py docs/Azure-CheatSheet.md`
- [ ] Set both jobs to trigger on `push` and `pull_request` events

## Configuration

- [ ] Create `.markdownlint.json` at repo root with rule overrides (disable `MD013`, `MD033`, and any rules conflicting with existing table style)
- [ ] Verify all existing `.md` files pass markdownlint with the chosen config locally before committing

## Mermaid Validation Script

- [ ] Create `scripts/validate_mermaid.py` that extracts all fenced mermaid blocks from a given Markdown file
- [ ] Script must write each block to a temp file and invoke `mmdc --input <tmp>` for validation
- [ ] Script must report diagram index and exit code 1 if any diagram fails validation
- [ ] Verify script correctly identifies all 7 diagrams in `docs/Azure-CheatSheet.md`

## README Badge

- [ ] Add GitHub Actions CI badge for `lint.yml` workflow to `README.md` below the top-level heading

## Validation

- [ ] Push workflow to `fix/issue-4-feature-add-github-actions-ci-workflow-for-markdown` branch and confirm both CI jobs pass on GitHub Actions
- [ ] Confirm all 7 Mermaid diagrams pass the validation script
- [ ] Confirm markdownlint reports no errors on `docs/Azure-CheatSheet.md` and `README.md`
