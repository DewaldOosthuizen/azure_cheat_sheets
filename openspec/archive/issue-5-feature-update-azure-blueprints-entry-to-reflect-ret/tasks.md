# Tasks: Issue #5

## Documentation — Table Update

- [ ] Add a fifth column `| Status |` to the table header at line 525 in `docs/Azure-CheatSheet.md` to accommodate the retirement status column.
- [ ] Update the Azure Blueprints row (line 530) to append `| **RETIRED July 2026** |` as the fifth column value.
- [ ] Verify all other rows in the table (`ARM Templates`, `Bicep`, `Terraform`) have a consistent fifth column (e.g. `| Active |` or left blank with `|  |`) so the table remains valid markdown.

## Documentation — Callout Replacement

- [ ] Replace the vague deprecation callout at line 532 with the three-component migration-path block (Template Specs, Azure Policy, RBAC).
- [ ] Include the official Microsoft retirement announcement URL as an inline reference within the callout block.

## Documentation — Exam Tip

- [ ] Add a new exam tip blockquote immediately after the updated callout, distinguishing legacy Blueprint scenarios from new governance design guidance.

## Quality Check

- [ ] Render the markdown locally (or via GitHub preview) to confirm the updated table displays correctly with five columns.
- [ ] Confirm the Microsoft retirement announcement link resolves to a live page.
- [ ] Cross-check AZ-305 study area alignment: the updated content must correctly map to the "Design governance" domain of the exam.
