## Overview

The Governance section of the Azure cheat sheet contains an outdated and ambiguous reference to Azure Blueprints as "being deprecated". Azure Blueprints is now formally retired as of July 11, 2026. The current wording fails AZ-305 candidates who need to understand the concrete replacement strategy (Template Specs + Policy + RBAC) and must distinguish legacy Blueprint scenarios from new governance designs. This proposal updates the table row, replaces the vague callout with a precise migration guide, and adds an exam tip to contextualise when Blueprints questions will appear.

## Issues

### Issue 1

**File:** `docs/Azure-CheatSheet.md`

**Problem:** Line 530 — the Azure Blueprints table row has no retirement status or date. It reads as an active product:
```
| **Azure Blueprints** | Governance packages (policy + RBAC + ARM) | Partial (locking) | Artifact-tracked |
```

**Fix:** Update the row to surface RETIRED status and the retirement date:
```
| **Azure Blueprints** | Governance packages (policy + RBAC + ARM) | Partial (locking) | Artifact-tracked | **RETIRED July 2026** |
```
Note: the table header at line 525 must gain a fifth column header (e.g. `| Status |`) to keep the table valid markdown.

### Issue 2

**File:** `docs/Azure-CheatSheet.md`

**Problem:** Line 532 — the callout is vague and actionable only at a high level:
```
> Blueprints are being deprecated — Microsoft is moving toward **Template Specs + Policy + RBAC** separately.
```
"Being deprecated" is present-progressive; the retirement has already occurred. There is no concrete migration path.

**Fix:** Replace the callout block with a precise, migration-focused notice that links to the official Microsoft announcement:
```markdown
> **Azure Blueprints is retired (July 2026).** Migrate to:
> - **ARM/Bicep Template Specs** — for reusable, versioned IaC artifacts.
> - **Azure Policy** — for compliance rules and auto-remediation.
> - **RBAC** — for role assignments and least-privilege access.
> Use all three together to replicate what a Blueprint provided as a single package.
>
> See: [Microsoft retirement announcement](https://azure.microsoft.com/en-us/updates/azure-blueprints-is-being-retired-on-11-july-2026/)
```

### Issue 3

**File:** `docs/Azure-CheatSheet.md`

**Problem:** No exam tip exists to help AZ-305 candidates contextualise when Blueprint questions appear (legacy environments vs new designs). Without this, candidates may misapply the retirement status when answering scenario questions about existing Blueprint deployments.

**Fix:** Add an exam tip immediately after the updated callout block (after line 532):
```markdown
> **Exam tip:** Questions about Blueprints reference legacy or existing environments. For new governance designs always specify Template Specs + Policy + RBAC as the replacement pattern.
```
