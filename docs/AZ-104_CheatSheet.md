# Administering Microsoft Azure

## AZ-104 Administrator Cheat Sheet

> **Exam Focus:** Operational decision-making — *how* to configure, manage, and
> troubleshoot Azure resources. Not architectural trade-offs.

## Table of Contents

1. [Networking](#networking)
2. [Security](#security)
3. [Storage](#storage)
4. [Monitoring & Observability](#monitoring--observability)
5. [Compute](#compute)
6. [Identity & Access](#identity--access)
7. [High Availability & Disaster Recovery](#high-availability--disaster-recovery)
8. [Governance](#governance)
9. [Messaging & Integration](#messaging--integration)
10. [Well-Architected Framework](#well-architected-framework)

---

# NETWORKING

> Core admin tasks: VNet peering, VPN Gateway, NSG/ASG rule management, and
> selecting the correct Load Balancer SKU.

## VNet Connectivity

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **VNet Peering** | L3 (IP) | Regional or Global | Low-latency VNet-to-VNet within or across regions | Non-transitive; no gateway required |
| **VPN Gateway** | L3 (IPsec/IKE) | Regional | Site-to-site, point-to-site, VNet-to-VNet over internet | Encrypted tunnel; supports BGP |
| **ExpressRoute** | L3 (private) | Global | Private on-premises to Azure; no public internet | Dedicated circuit; higher reliability |
| **Azure Bastion** | L7 (HTTPS/RDP) | Regional | Secure RDP/SSH to VMs without public IP | No public IP on VM needed |

> **Exam tip:** VNet Peering is non-transitive — if VNet A peers with VNet B and VNet B peers with VNet C, VNet A cannot reach VNet C without a direct peering or hub-spoke with gateway transit enabled.

### VNet Connectivity Decision Flow

```mermaid
--8<-- "diagrams/networking/az104-vnet-connectivity-decision-flow.mmd"
```

## NSG vs ASG

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **NSG** | L4 (TCP/UDP) | Subnet or NIC | Allow/Deny inbound and outbound traffic | Priority-based rules; default deny |
| **ASG** | L4 (TCP/UDP) | NIC grouping | Group VMs logically for NSG rules | Simplifies rules for dynamic VM sets |

> **Exam tip:** ASGs do not replace NSGs — they are used inside NSG rules as source/destination to group NICs without managing individual IP addresses.

### NSG Rule Evaluation

```mermaid
--8<-- "diagrams/networking/az104-nsg-rule-evaluation.mmd"
```

## Load Balancer SKU Selection

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Load Balancer Basic** | L4 | Regional | Dev/test, single availability set | Free; no SLA for multi-VM; no AZ support |
| **Azure Load Balancer Standard** | L4 | Regional/Zonal | Production VM load balancing | Zone-redundant; SLA 99.99%; HTTPS health probes |
| **Application Gateway** | L7 | Regional | HTTP/S web app routing | WAF, SSL offload, URL-based routing |

> **Exam tip:** Standard Load Balancer requires explicit NSG rules to allow traffic — Basic SKU allows traffic by default. Always use Standard for production workloads.

> **SLA note:** Basic Load Balancer is not designed for SLA-backed production.
> When a requirement explicitly calls for a formal load-balancing SLA, choose
> Standard Load Balancer and deploy with resilient backend instances.

### Load Balancer SKU Decision Flow

```mermaid
--8<-- "diagrams/networking/az104-load-balancer-sku-decision-flow.mmd"
```

---

# SECURITY

> Core admin tasks: Key Vault access model selection, enabling Defender for Cloud,
> and managing security posture.

## Key Vault Access Models

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Key Vault - Access Policies** | Legacy model | Simple per-principal grants | Per-object permissions; no RBAC inheritance |
| **Key Vault - Azure RBAC** | Role-based model | Consistent RBAC governance | Entra ID roles; supports PIM; audit trail |
| **Managed Identity** | Identity type | App-to-Key Vault auth | No credentials; auto-rotated by Azure |

> **⚠️ Deprecation warning:** Vault Access Policies are the legacy authorization model for
> Key Vault. Microsoft recommends migrating to **Azure RBAC** for new and existing vaults.
> RBAC provides Entra-native granularity, PIM support, and a unified audit trail.

> **Exam tip:** Microsoft recommends Key Vault Azure RBAC over Access Policies for new deployments. RBAC supports Privileged Identity Management (PIM) for just-in-time access.

### Key Vault Access Decision Flow

```mermaid
--8<-- "diagrams/security/az104-key-vault-access-decision-flow.mmd"
```

## Defender for Cloud

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Defender CSPM (Free)** | Posture | Subscription | Secure Score, recommendations | Always on; no cost |
| **Defender CSPM (Paid)** | Posture | Subscription | Advanced posture, attack paths | Governance rules, regulatory compliance |
| **Defender for Servers** | Workload | VM/Arc | Threat detection on VMs | MDE integration, vulnerability assessment |
| **Defender for Storage** | Workload | Storage Account | Malware scanning, anomaly detection | Per-storage-account enablement |

> **Exam tip:** Enabling Defender for Cloud at the subscription level automatically covers all existing and future resources. Use the "Enhanced Security" toggle per workload plan to control cost.

### Defender for Cloud Coverage

```mermaid
--8<-- "diagrams/security/az104-defender-for-cloud-coverage.mmd"
```

---

# STORAGE

> Core admin tasks: selecting managed disk types, configuring storage account
> replication, and managing access tiers.

## Managed Disk Types

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Standard HDD** | Magnetic | Dev/test, infrequent access | Lowest cost; up to 2000 IOPS/500 MBps |
| **Standard SSD** | SSD | Web servers, lightly used apps | Consistent latency vs HDD; up to 6000 IOPS |
| **Premium SSD** | SSD | Production databases, critical apps | Up to 20000 IOPS/900 MBps per disk |
| **Premium SSD v2** | SSD | High-perf workloads with tunable IOPS | Independently set IOPS, throughput, capacity |
| **Ultra Disk** | NVMe SSD | Latency-sensitive: SAP HANA, top-tier SQL | Sub-millisecond latency; up to 160000 IOPS |

> **Exam tip:** Ultra Disk requires VM series that support it (e.g., Esv3, Dsv3) and must be in the same Availability Zone as the VM. It cannot be used as OS disk.

### Managed Disk Selection

```mermaid
--8<-- "diagrams/storage/az104-managed-disk-selection.mmd"
```

## Storage Account Replication

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **LRS** | Local redundancy | Dev/test, low cost | 3 copies in one datacenter |
| **ZRS** | Zone redundancy | High availability, same region | 3 copies across 3 AZs in one region |
| **GRS** | Geo redundancy | DR; secondary read only on failover | LRS primary + async copy to secondary region |
| **RA-GRS** | Geo redundancy + read | DR with read access to secondary | GRS + read endpoint on secondary region |
| **GZRS** | Geo-zone redundancy | Max HA + DR | ZRS primary + async copy to secondary region |
| **RA-GZRS** | Geo-zone + read | Max HA + DR + read | GZRS + read endpoint on secondary region |

> **Exam tip:** RA-GRS and RA-GZRS provide a secondary read endpoint (use `-secondary` suffix in storage URL). The secondary is always read-only unless a failover is initiated.

### Storage Replication Decision Flow

```mermaid
--8<-- "diagrams/storage/az104-storage-replication-decision-flow.mmd"
```

---

# MONITORING & OBSERVABILITY

> Core admin tasks: deploying monitoring agents, configuring diagnostic settings,
> and routing logs to Log Analytics Workspace.

## Azure Monitor Agents

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Monitor Agent (AMA)** | OS-level | VM, VMSS, Arc | Recommended; replaces legacy agents | Data Collection Rules (DCR); multi-workspace |
| **MMA / OMS Agent (legacy)** | OS-level | VM | Being retired (Aug 2024) | Single workspace; no DCR support |
| **Diagnostics Extension (WAD/LAD)** | OS-level | VM | Guest OS metrics/logs to Azure Storage | XML config; not Log Analytics native |
| **Dependency Agent** | Network | VM | Service Map, VM Insights connectivity | Requires AMA or MMA; maps processes |

> **⚠️ Deprecation warning:** The MMA/OMS (Microsoft Monitoring Agent / OMS Agent) is retired
> (August 2024). Migrate all VM monitoring deployments to **Azure Monitor Agent (AMA)** with
> Data Collection Rules (DCR).

> **Exam tip:** The MMA/OMS agent is retired. For AZ-104, always choose AMA with Data Collection Rules for new deployments. DCRs allow filtering and routing to multiple destinations.

### Agent Selection Decision Flow

```mermaid
--8<-- "diagrams/monitoring/az104-agent-selection-decision-flow.mmd"
```

## Diagnostic Settings

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Log Analytics Workspace** (fed via Diagnostic Settings; contains Activity Log data, KQL engine) | Destination | Query, alerting, dashboards | Kusto (KQL) queries; retention config |
| **Azure Storage Account** | Destination | Long-term archive, compliance | Low cost; no real-time query |
| **Event Hub** | Destination | SIEM integration, streaming | Real-time export to Splunk, Sentinel |
| **Partner Solutions** | Destination | Third-party observability | Datadog, Elastic natively integrated |

> **Exam tip:** Diagnostic Settings must be configured per resource. Use Azure Policy with DeployIfNotExists effect to automatically configure diagnostic settings at scale across subscriptions.

### Diagnostic Settings Routing

```mermaid
--8<-- "diagrams/monitoring/az104-diagnostic-settings-routing.mmd"
```
> **Exam tip:** Activity Log is a sub-component of Azure Monitor, not a standalone service.
> Route it to Log Analytics Workspace via Diagnostic Settings to enable KQL querying and
> long-term retention. For AZ-104, use Azure Policy (DeployIfNotExists) to enforce
> Diagnostic Settings at scale.

---

# COMPUTE

> Core admin tasks: selecting VM size families, configuring availability options,
> and managing VM Scale Sets.

## VM Sizing Families

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **D-series (General Purpose)** | Balanced | General | Web servers, dev/test, small databases | Balanced CPU:memory ratio |
| **F-series (Compute Optimized)** | High CPU | Compute | Batch, gaming, web front-ends | High CPU:memory ratio |
| **E-series (Memory Optimized)** | High RAM | Memory | SAP, in-memory databases, caches | High memory:CPU ratio |
| **L-series (Storage Optimized)** | High throughput | Storage | Cassandra, MongoDB, big data | High local disk IOPS/throughput |
| **N-series (GPU)** | GPU | GPU | ML training, rendering, visualization | NVIDIA GPU; NC/ND/NV variants |

> **Exam tip:** For SAP HANA workloads use M-series (memory optimized, largest RAM). For high-throughput NVMe workloads use Lsv3. The "s" suffix (e.g., Dsv5) indicates Premium SSD support.

### VM Family Decision Flow

```mermaid
--8<-- "diagrams/compute/az104-vm-family-decision-flow.mmd"
```

## Availability Sets vs Availability Zones

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Availability Set** | VM grouping | Single datacenter | Protect from hardware/rack failures | Fault domains (2-3) + Update domains (up to 20) |
| **Availability Zone** | VM placement | Zonal (3 zones) | Protect from datacenter failures | Physically separate DCs with independent power |
| **VM Scale Set - Flexible** | VM grouping | Zonal or regional | Auto-scale across zones | Supports mix of manual and auto-scaled VMs |

> **Exam tip:** Availability Sets protect against hardware failures within a single datacenter. Availability Zones protect against full datacenter outages. VMs in an Availability Set get a 99.95% SLA; VMs in different AZs get 99.99% SLA.

> **SLA note:** Single-instance VM designs do not satisfy higher SLA targets.
> For guaranteed uptime questions, expect at least Availability Set or
> Availability Zone based designs.

### Availability Decision Flow

```mermaid
--8<-- "diagrams/compute/az104-availability-decision-flow.mmd"
```

---

# IDENTITY & ACCESS

> Core admin tasks: assigning RBAC roles, managing Entra ID join types,
> and configuring Conditional Access.

## RBAC Built-in Roles

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Owner** | Full control | Any | Full resource management including access | Can assign roles; includes all Contributor perms |
| **Contributor** | Resource management | Any | Create and manage resources | Cannot assign roles or manage access |
| **Reader** | Read-only | Any | View resources, audit, monitoring | No create/update/delete; no role assignments |
| **User Access Administrator** | Access management | Any | Manage role assignments only | Cannot modify resources; only access control |

> **Exam tip:** User Access Administrator can grant Owner to others — this is a powerful role. Use it carefully and prefer just-in-time elevation via PIM over permanent assignment.

### RBAC Role Assignment Decision Flow

```mermaid
--8<-- "diagrams/identity/az104-rbac-role-assignment-decision-flow.mmd"
```

## Entra ID Join Types

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Entra ID Join (AAD Join)** | Cloud-only join | New cloud-only devices | No on-prem dependency; MDM enrolled |
| **Hybrid Entra ID Join** | Hybrid join | Existing domain-joined devices | Joined to both on-prem AD and Entra ID |
| **Entra ID Registered** | Personal device | BYOD | Minimal IT control; user account registered |

> **Exam tip:** Hybrid Entra ID Join requires line-of-sight to a domain controller or Azure AD Connect for initial join. It is used for existing corporate devices that need both on-prem GPO and cloud SSO.

### Entra ID Join Type Decision Flow

```mermaid
--8<-- "diagrams/identity/az104-entra-id-join-type-decision-flow.mmd"
```

---

# HIGH AVAILABILITY & DISASTER RECOVERY

> Core admin tasks: configuring Azure Backup vaults, enabling Azure Site Recovery,
> and defining RPO/RTO targets.

## Azure Backup vs Azure Site Recovery

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Azure Backup** | Data backup | Files, VMs, databases, blobs | Point-in-time restore; policy-based scheduling |
| **Azure Site Recovery** | Replication/DR | VM failover to secondary region | Near-zero RPO; orchestrated failover/failback |
| **Backup Center** | Management | Centralized backup governance | Single pane for all vaults across subscriptions |

> **Exam tip:** Azure Backup protects against data loss (accidental deletion, corruption). Azure Site Recovery protects against VM/region failure. They are complementary — use both for full protection.

### HA & DR Decision Flow

```mermaid
--8<-- "diagrams/ha-dr/az104-ha-dr-decision-flow.mmd"
```

## Recovery Services Vault Structure

```mermaid
--8<-- "diagrams/ha-dr/az104-recovery-services-vault-structure.mmd"
```
> **⚠️ Deprecation warning:** Recovery Services Vault is the legacy backup store (VMs, SQL
> in VM, Azure Files). For new PaaS-based backup targets (Blobs, managed databases), use
> **Backup Vault** — Microsoft's current backup store model.

---

# GOVERNANCE

> Core admin tasks: creating and assigning Azure Policies, organizing resources
> in Management Groups, and applying tagging strategies.

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
--8<-- "diagrams/governance/az104-policy-assignment-scope-hierarchy.mmd"
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
--8<-- "diagrams/governance/az104-management-hierarchy-decision-flow.mmd"
```

---

# MESSAGING & INTEGRATION

> Core admin tasks: selecting Service Bus SKU, configuring namespaces,
> and choosing queue vs topic/subscription.

## Service Bus vs Storage Queues

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Storage Queue** | Simple queue | Large volume, simple FIFO | Up to 500 TB; HTTP-based; minimal features |
| **Service Bus Queue** | Broker queue | Reliable delivery, ordering | Dead-letter queue; duplicate detection; sessions |
| **Service Bus Topic** | Pub/sub | Fan-out to multiple consumers | Multiple subscriptions per topic; filters |

> **Exam tip:** Use Service Bus when you need message ordering, dead-lettering, duplicate detection, or transactions. Use Storage Queue when you need >80 GB storage, simple REST polling, or audit logs.

### Service Bus Namespace SKUs

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Basic SKU** | Namespace tier | Simple queues only | No topics, sessions, or duplicate detection |
| **Standard SKU** | Namespace tier | Variable throughput | Topics, subscriptions, shared capacity |
| **Premium SKU** | Namespace tier | Predictable performance | Dedicated capacity units; VNet integration; large messages up to 100 MB |

> **Exam tip:** Premium SKU is required for VNet service endpoints, private endpoints, and geo-disaster recovery (Geo-DR paired namespaces).

> **SLA note:** Messaging scenarios that emphasize strict reliability,
> predictable throughput, and isolation generally indicate Service Bus Premium.

### Messaging Decision Flow

```mermaid
--8<-- "diagrams/messaging/az104-messaging-decision-flow.mmd"
```
### Service Bus SKU Decision Flow

```mermaid
--8<-- "diagrams/messaging/az104-service-bus-sku-decision-flow.mmd"
```

---

# WELL-ARCHITECTED FRAMEWORK

> AZ-104 admin scope: Cost Management, tagging, budgets, and cost alerts.
> Not full WAF pillar depth — focus on operational cost controls.

## Cost Management & Tagging

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Tags** | Metadata | Cost allocation, filtering | Key-value pairs; up to 50 per resource |
| **Azure Policy - Tag Enforcement** | Governance | Require tags on resources | Deny untagged resources; inherit parent tags |
| **Cost Management Budgets** | Cost control | Spending alerts and limits | Alert at % of budget; action groups supported |
| **Cost Alerts** | Notification | Anomaly detection, budget thresholds | Credit, budget, department quota alerts |
| **Cost Analysis** | Analysis | Ad-hoc spend review | Filter by tag, resource group, subscription |

> **Exam tip:** Tags do NOT inherit from parent scopes (RG to resource) by default. Use Azure Policy with the `Inherit a tag from the resource group` initiative to enforce tag inheritance automatically.

### Tag Inheritance Architecture

```mermaid
--8<-- "diagrams/waf/az104-tag-inheritance-architecture.mmd"
```
### Cost Management Decision Flow

```mermaid
--8<-- "diagrams/waf/az104-cost-management-decision-flow.mmd"
```
