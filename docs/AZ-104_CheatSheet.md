# Administering Microsoft Azure

## AZ-104 Administrator Cheat Sheet

> **Exam Focus:** Operational decision-making — *how* to configure, manage, and
> troubleshoot Azure resources. Not architectural trade-offs.

---

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
flowchart TD
    A[Connect two networks?] --> B{Same or different subscription/region?}
    B -- Same region --> C[VNet Peering - Regional]
    B -- Different region --> D[VNet Peering - Global]
    A --> E{On-premises to Azure?}
    E -- Low cost, variable --> F[VPN Gateway Site-to-Site]
    E -- High bandwidth, private --> G[ExpressRoute]
```

---

## NSG vs ASG

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **NSG** | L4 (TCP/UDP) | Subnet or NIC | Allow/Deny inbound and outbound traffic | Priority-based rules; default deny |
| **ASG** | L4 (TCP/UDP) | NIC grouping | Group VMs logically for NSG rules | Simplifies rules for dynamic VM sets |

> **Exam tip:** ASGs do not replace NSGs — they are used inside NSG rules as source/destination to group NICs without managing individual IP addresses.

### NSG Rule Evaluation

```mermaid
flowchart TD
    A[Inbound packet arrives] --> B[Check subnet NSG]
    B --> C{Rule match?}
    C -- Allow --> D[Check NIC NSG]
    C -- Deny --> E[Drop packet]
    D --> F{Rule match?}
    F -- Allow --> G[Packet reaches VM]
    F -- Deny --> H[Drop packet]
```

---

## Load Balancer SKU Selection

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Azure Load Balancer Basic** | L4 | Regional | Dev/test, single availability set | Free; no SLA for multi-VM; no AZ support |
| **Azure Load Balancer Standard** | L4 | Regional/Zonal | Production VM load balancing | Zone-redundant; SLA 99.99%; HTTPS health probes |
| **Application Gateway** | L7 | Regional | HTTP/S web app routing | WAF, SSL offload, URL-based routing |

> **Exam tip:** Standard Load Balancer requires explicit NSG rules to allow traffic — Basic SKU allows traffic by default. Always use Standard for production workloads.

### Load Balancer SKU Decision Flow

```mermaid
flowchart TD
    A[Need load balancing?] --> B{HTTP or HTTPS traffic?}
    B -- No --> C{Production workload?}
    B -- Yes --> D[Application Gateway]
    C -- No --> E[Load Balancer Basic]
    C -- Yes --> F[Load Balancer Standard]
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
flowchart TD
    A[App needs secret/key/cert?] --> B{Use managed identity?}
    B -- Yes --> C[Assign Key Vault role via RBAC to managed identity]
    B -- No --> D{RBAC or Access Policy?}
    D -- RBAC --> E[Assign Key Vault Secrets Officer / Reader role]
    D -- Access Policy --> F[Set Get/List/Set permissions per principal]
```

---

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
graph TD
    A[Defender for Cloud] --> B[CSPM - Posture Management]
    A --> C[Workload Protection Plans]
    B --> D[Secure Score]
    B --> E[Regulatory Compliance]
    C --> F[Defender for Servers]
    C --> G[Defender for Storage]
    C --> H[Defender for Databases]
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
flowchart TD
    A[Choose managed disk] --> B{Production workload?}
    B -- No --> C[Standard HDD or Standard SSD]
    B -- Yes --> D{Latency-sensitive?}
    D -- Extreme sub-ms --> E[Ultra Disk]
    D -- High but not extreme --> F{Tunable IOPS needed?}
    F -- Yes --> G[Premium SSD v2]
    F -- No --> H[Premium SSD]
```

---

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
flowchart TD
    A[Choose replication] --> B{Need geo-redundancy?}
    B -- No --> C{Need zone redundancy?}
    C -- No --> D[LRS]
    C -- Yes --> E[ZRS]
    B -- Yes --> F{Need read access to secondary?}
    F -- No --> G{Need zone redundancy at primary?}
    G -- No --> H[GRS]
    G -- Yes --> I[GZRS]
    F -- Yes --> J{Zone redundancy at primary?}
    J -- No --> K[RA-GRS]
    J -- Yes --> L[RA-GZRS]
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
flowchart TD
    A[Need VM monitoring?] --> B{New or existing deployment?}
    B -- New --> C[Azure Monitor Agent + DCR]
    B -- Existing with MMA --> D{Migrate before retirement?}
    D -- Yes --> C
    D -- No yet --> E[Keep MMA - plan migration]
    C --> F{Need process/network map?}
    F -- Yes --> G[Add Dependency Agent]
    F -- No --> H[AMA only]
```

---

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
graph LR
    A[Azure Resource] --> B[Diagnostic Settings]
    B --> C[Log Analytics Workspace]
    B --> D[Storage Account]
    B --> E[Event Hub]
    E --> F[Sentinel / SIEM]
    C --> G[Alerts / Dashboards]
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
flowchart TD
    A[Choose VM size] --> B{GPU required?}
    B -- Yes --> C[N-series]
    B -- No --> D{Primary constraint?}
    D -- Balanced --> E[D-series General Purpose]
    D -- High CPU --> F[F-series Compute Optimized]
    D -- High Memory --> G[E or M-series Memory Optimized]
    D -- High Disk Throughput --> H[L-series Storage Optimized]
```

---

## Availability Sets vs Availability Zones

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Availability Set** | VM grouping | Single datacenter | Protect from hardware/rack failures | Fault domains (2-3) + Update domains (up to 20) |
| **Availability Zone** | VM placement | Zonal (3 zones) | Protect from datacenter failures | Physically separate DCs with independent power |
| **VM Scale Set - Flexible** | VM grouping | Zonal or regional | Auto-scale across zones | Supports mix of manual and auto-scaled VMs |

> **Exam tip:** Availability Sets protect against hardware failures within a single datacenter. Availability Zones protect against full datacenter outages. VMs in an Availability Set get a 99.95% SLA; VMs in different AZs get 99.99% SLA.

### Availability Decision Flow

```mermaid
flowchart TD
    A[Need VM HA?] --> B{Multiple datacenters?}
    B -- No --> C[Availability Set]
    B -- Yes --> D{Auto-scale needed?}
    D -- No --> E[Place VMs across Availability Zones manually]
    D -- Yes --> F[VM Scale Set - Flexible orchestration across zones]
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
flowchart TD
    A[Assign role?] --> B{Need to manage resources?}
    B -- No --> C{Need to manage access only?}
    B -- Yes --> D{Need to assign roles too?}
    C -- Yes --> E[User Access Administrator]
    C -- No --> F[Reader]
    D -- No --> G[Contributor]
    D -- Yes --> H[Owner]
```

---

## Entra ID Join Types

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Entra ID Join (AAD Join)** | Cloud-only join | New cloud-only devices | No on-prem dependency; MDM enrolled |
| **Hybrid Entra ID Join** | Hybrid join | Existing domain-joined devices | Joined to both on-prem AD and Entra ID |
| **Entra ID Registered** | Personal device | BYOD | Minimal IT control; user account registered |

> **Exam tip:** Hybrid Entra ID Join requires line-of-sight to a domain controller or Azure AD Connect for initial join. It is used for existing corporate devices that need both on-prem GPO and cloud SSO.

### Entra ID Join Type Decision Flow

```mermaid
flowchart TD
    A[Device registration?] --> B{Corporate or personal device?}
    B -- Personal/BYOD --> C[Entra ID Registered]
    B -- Corporate --> D{Existing on-prem AD domain?}
    D -- No --> E[Entra ID Join - cloud only]
    D -- Yes --> F{Keep GPO/on-prem dependency?}
    F -- Yes --> G[Hybrid Entra ID Join]
    F -- No --> E
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
flowchart TD
    A[Protect workload?] --> B{Protect against data loss?}
    B -- Yes --> C[Azure Backup - configure policy + vault]
    A --> D{Protect against region failure?}
    D -- Yes --> E[Azure Site Recovery - replicate VM to secondary region]
    C --> F[Set retention and backup frequency]
    E --> G[Test failover regularly]
```

---

## Recovery Services Vault Structure

```mermaid
graph TD
    A[Recovery Services Vault] --> B[Backup Items]
    A --> C[Replication Items - ASR]
    B --> D[Azure VMs]
    B --> E[SQL in VM]
    B --> F[Azure Files]
    C --> G[Replicated VMs - failover ready]
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
graph TD
    A[Root Management Group] --> B[Child Management Group]
    B --> C[Subscription A]
    B --> D[Subscription B]
    C --> E[Resource Group 1]
    C --> F[Resource Group 2]
    D --> G[Resource Group 3]
```

---

## Management Groups & Subscriptions

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Management Group** | Org hierarchy | Policy and RBAC at scale | Up to 6 levels deep; root MG always present |
| **Subscription** | Billing + access | Resource isolation, billing boundary | RBAC root; limits apply per subscription |
| **Resource Group** | Logical grouping | Lifecycle management | All resources must belong to one RG |

> **Exam tip:** You can move a subscription between Management Groups but you cannot move a Management Group into another tenant. RBAC assigned at MG level is inherited by all subscriptions below it.

### Management Hierarchy Decision Flow

```mermaid
flowchart TD
    A[Organize Azure resources] --> B{Multiple subscriptions?}
    B -- No --> C[Use Resource Groups within subscription]
    B -- Yes --> D{Apply policies across subscriptions?}
    D -- No --> E[Assign policy per subscription]
    D -- Yes --> F[Create Management Group and assign policy there]
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

### Messaging Decision Flow

```mermaid
flowchart TD
    A[Choose messaging service] --> B{Multiple consumers for same message?}
    B -- Yes --> C[Service Bus Topic with subscriptions]
    B -- No --> D{Need dead-letter or ordering?}
    D -- Yes --> E[Service Bus Queue]
    D -- No --> F{Large volume simple queue?}
    F -- Yes --> G[Storage Queue]
    F -- No --> E
```

### Service Bus SKU Decision Flow

```mermaid
flowchart TD
    A[Choose Service Bus SKU] --> B{Need topics?}
    B -- No --> C[Basic SKU]
    B -- Yes --> D{Need VNet / private endpoint?}
    D -- No --> E[Standard SKU]
    D -- Yes --> F[Premium SKU]
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
graph TD
    A[Management Group] --> B[Subscription]
    B --> C[Resource Group]
    C --> D[Resource]
    A -. "No auto-inherit" .-> D
    C -. "Policy: Inherit tag from RG" .-> D
```

### Cost Management Decision Flow

```mermaid
flowchart TD
    A[Control Azure costs?] --> B{Track by team/project?}
    B -- Yes --> C[Apply tags - Environment, CostCenter, Owner]
    C --> D{Enforce tagging?}
    D -- Yes --> E[Azure Policy - Require tag or Inherit from RG]
    A --> F{Alert on overspend?}
    F -- Yes --> G[Create Budget with alert thresholds]
    G --> H[Attach Action Group for email/webhook notification]
```

---
