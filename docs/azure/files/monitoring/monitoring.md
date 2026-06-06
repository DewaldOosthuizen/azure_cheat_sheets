# Monitoring & Observability

## Azure Monitor Ecosystem

```mermaid
--8<-- "azure/diagrams/monitoring/azure-monitor-ecosystem.mmd"
```

## Key Services

| Service | Purpose | Key Concepts |
| --- | --- | --- |
| **Azure Monitor** (umbrella: Activity Log, Metrics, Alerts, Diagnostic Settings, Insights family) | Central telemetry platform | Metrics, Logs, Alerts, Workbooks |
| **Log Analytics Workspace** (contains: KQL engine, retention tiers; fed via Diagnostic Settings) | Store and query logs (KQL) | Retention (30–730 days), data export |
| **Application Insights** (contains: Live Metrics, Availability Tests, Dependency Tracking, Smart Detection) | APM for apps | Live metrics, dependency tracking, availability tests |
| **VM Insights** | Perf + map for VMs | Relies on Log Analytics agent/AMA |
| **Container Insights** | AKS monitoring | Pod/node metrics, log collection |
| **Network Watcher** | Network diagnostics | Packet capture, flow logs, connection monitor |
| **Azure Advisor** | Best practice recommendations | Cost, security, reliability, performance |
| **Service Health** | Azure platform health | Planned maintenance, incidents |
| **Resource Health** | Your resource health | Is *your* resource healthy right now |

## Alerts

| Type | Trigger | Use Case |
| --- | --- | --- |
| **Metric Alert** | Threshold on metric value | CPU > 80%, response time > 2s |
| **Log Alert** | KQL query result count/value | Error count in last 5 min > 10 |
| **Activity Log Alert** | Azure control-plane events | Who deleted a resource, policy assignment (Activity Log is a sub-component of Azure Monitor, routed to Log Analytics via Diagnostic Settings) |
| **Smart Detection** | AI-based anomaly in App Insights | Failure rate spikes, perf degradation |

> **Action Groups** decouple alert routing from alert rules. One action group → multiple rules.

> **Exam tip:** When an answer option names a specific sub-component (e.g. Activity Log,
> Live Metrics, Smart Detection), prefer it over the umbrella service (e.g. Azure Monitor,
> Application Insights). Select the umbrella only when the sub-component is absent from
> the options.

## Diagnostic Settings

- Send to: **Log Analytics Workspace**, **Storage Account**, **Event Hub**, **Partner solution**
- Configure per resource (or via Azure Policy at scale)
- Categories: AllMetrics, Audit, Operational, **Activity Log** (control-plane events), etc.
- Activity Log is a sub-component of Azure Monitor routed to Log Analytics Workspace via Diagnostic Settings — not a standalone service.

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Log Analytics Workspace** (fed via Diagnostic Settings; contains Activity Log data, KQL engine) | Destination | Query, alerting, dashboards | Kusto (KQL) queries; retention config |
| **Azure Storage Account** | Destination | Long-term archive, compliance | Low cost; no real-time query |
| **Event Hub** | Destination | SIEM integration, streaming | Real-time export to Splunk, Sentinel |
| **Partner Solutions** | Destination | Third-party observability | Datadog, Elastic natively integrated |

> **Exam tip:** Diagnostic Settings must be configured per resource. Use Azure Policy with DeployIfNotExists effect to automatically configure diagnostic settings at scale across subscriptions.

> **Exam tip (AZ-500):** Diagnostic Settings are the bridge between Azure
> resources and Microsoft Sentinel. Route Activity Logs, Entra audit logs, and
> resource diagnostic logs to a Log Analytics Workspace that Sentinel reads from.
> Without Diagnostic Settings configured, Sentinel data connectors receive no data.

### Diagnostic Settings Routing

```mermaid
--8<-- "azure/diagrams/monitoring/diagnostic-settings-routing.mmd"
```

> **Exam tip:** Activity Log is a sub-component of Azure Monitor, not a standalone service.
> Route it to Log Analytics Workspace via Diagnostic Settings to enable KQL querying and
> long-term retention. For AZ-104, use Azure Policy (DeployIfNotExists) to enforce
> Diagnostic Settings at scale.

## Log Analytics Retention & Cost Tiers

| Tier | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Analytics** | Interactive (30–730 days) | Active investigation, alerting | Full KQL, per-GB ingestion cost |
| **Basic** | Interactive (8 days) | High-volume, low-value logs | Limited KQL, lower per-GB cost |
| **Archive** | Cold (up to 12 years) | Compliance, audit, cold storage | Search jobs only, lowest per-GB cost |

> **Exam tip:** Choose Basic tier for noisy, rarely queried logs (e.g. verbose diagnostics)
> to reduce cost. Use Archive when retention beyond 730 days is required for compliance;
> queries against archived data run as Search Jobs, not interactive KQL.

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
--8<-- "azure/diagrams/monitoring/agent-selection-decision-flow.mmd"
```
