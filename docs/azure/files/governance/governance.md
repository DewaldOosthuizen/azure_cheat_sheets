# Governance

## Management Hierarchy

```mermaid
--8<-- "azure/diagrams/governance/management-hierarchy.mmd"
```

| Scope | Purpose |
| --- | --- |
| **Root Management Group** | Apply policies across entire tenant |
| **Management Group** | Group subscriptions, inherit policies |
| **Subscription** | Billing boundary, policy scope |
| **Resource Group** | Lifecycle boundary — deploy/delete together |

## Azure Blueprints vs ARM Templates vs Terraform

| Tool | Purpose | Drift Detection | State | Status |
| --- | --- | --- | --- | --- |
| **ARM Templates** | Deploy resources declaratively | No | Stateless | Active |
| **Bicep** | ARM simplified syntax | No | Stateless | Active |
| **Terraform** | Multi-cloud IaC | Yes (plan) | Stateful | Active |
| **Azure Blueprints** | Governance packages (policy + RBAC + ARM) | Partial (locking) | Artifact-tracked | **RETIRED July 2026** |

> **⚠️ Deprecation warning:** Azure Blueprints is retired (11 July 2026). Migrate to:
>
> - **ARM/Bicep Template Specs** — for reusable, versioned IaC artifacts.
> - **Azure Policy** — for compliance rules and auto-remediation.
> - **RBAC** — for role assignments and least-privilege access.
> Use all three together to replicate what a Blueprint provided as a single package.
>
> See: [Microsoft retirement announcement](https://azure.microsoft.com/en-us/updates/azure-blueprints-is-being-retired-on-11-july-2026/)

> **Exam tip:** Questions about Blueprints reference legacy or existing environments. For new governance designs always specify Template Specs + Policy + RBAC as the replacement pattern.

## Governance Enforcement Decision Flow

```mermaid
--8<-- "azure/diagrams/governance/governance-enforcement-decision-flow.mmd"
```

> **Exam tip:** When a question mentions enforcing a rule that blocks or auto-remediates
> non-compliant resources across subscriptions, the answer is Azure Policy — not Locks
> (which only prevent delete/write) and not Management Groups (which are the scope, not the
> enforcement tool).

## Cost Management

| Tool | Purpose |
| --- | --- |
| **Azure Cost Management** | View, analyze, alert on spending |
| **Budgets** | Set spend thresholds, trigger alerts/actions |
| **Azure Advisor (Cost)** | Right-sizing and reservation recommendations |
| **Reserved Instances** | 1 or 3 year commit — up to 72% savings |
| **Spot VMs** | Evictable — up to 90% savings for fault-tolerant workloads |
| **Azure Hybrid Benefit** | Use existing Windows Server / SQL licenses |

## Tags

- Applied at: Resource, Resource Group, Subscription level
- Inherited? **No** — tags don't inherit by default (use Azure Policy to enforce inheritance)
- Max: 50 tags per resource
- Use cases: cost center, environment, owner, project

## Locks

| Lock Type | Prevents |
| --- | --- |
| **ReadOnly** | All write operations (create, update, delete) — read access only |
| **CanNotDelete** | Delete only — updates still allowed |

> Locks are inherited by child resources. Applied at resource, resource group, or subscription.
>
> Source: [Azure Lock Resources — Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)

> **Exam tip (AZ-500):** Azure Policy is the primary compliance enforcement tool
> in AZ-500 — know Deny (blocks creation), Audit (flags without blocking), and
> DeployIfNotExists (auto-remediates). Resource Locks (ReadOnly / Delete) protect
> against accidental change or deletion but do not enforce configuration compliance.

## Azure Lighthouse

Azure Lighthouse enables **cross-tenant management** — a service provider (MSP) or central IT
team can manage customer or subsidiary tenant resources from their own tenant without switching
directories or maintaining guest accounts.

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Azure Lighthouse** | Cross-tenant delegation | MSP managing multiple customer tenants; enterprise hub managing subsidiaries | Azure Resource Manager delegation; no credential sharing; full Azure RBAC applies |

> **Exam tip:** Choose Azure Lighthouse when the requirement mentions an MSP or central IT team
> managing resources across multiple Azure tenants without separate logins. Lighthouse uses
> Azure Delegated Resource Management — the customer retains ownership; the provider sees and
> acts on customer resources from their own tenant. Distinguish from Azure B2B guest access,
> which is per-user and not suited for at-scale managed service operations.

## Azure Policy Assignment Scopes

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Policy at Management Group** | Governance | All subscriptions below | Org-wide standards | Inherits down to all child subscriptions/RGs |
| **Policy at Subscription** | Governance | All RGs in subscription | Subscription-level compliance | Overrides MG exclusions for that subscription |
| **Policy at Resource Group** | Governance | RG only | Scoped enforcement | Most granular assignment scope |
| **Initiative (Policy Set)** | Governance | Any scope | Group related policies | Single assignment; compliance aggregated |

> **Exam tip:** Policy effects in priority order: Disabled > Audit > Deny > Modify > DeployIfNotExists > AuditIfNotExists. DeployIfNotExists requires a managed identity on the assignment to remediate.

### Policy Assignment Scope Hierarchy

```mermaid
--8<-- "azure/diagrams/governance/policy-assignment-scope-hierarchy.mmd"
```

## Management Groups & Subscriptions

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Management Group** | Org hierarchy | Policy and RBAC at scale | Up to 6 levels deep; root MG always present |
| **Subscription** | Billing + access | Resource isolation, billing boundary | RBAC root; limits apply per subscription |
| **Resource Group** | Logical grouping | Lifecycle management | All resources must belong to one RG |

> **Exam tip:** You can move a subscription between Management Groups but you cannot move a Management Group into another tenant. RBAC assigned at MG level is inherited by all subscriptions below it.

### Management Hierarchy Decision Flow

```mermaid
--8<-- "azure/diagrams/governance/management-hierarchy-decision-flow.mmd"
```
