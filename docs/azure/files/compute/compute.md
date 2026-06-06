## Compute Options

| Service | Type | Use Case |
| --- | --- | --- |
| **Azure Virtual Machines** | IaaS | Full OS control, lift-and-shift |
| **VM Scale Sets (VMSS)** | IaaS autoscale | Stateless workloads needing horizontal scale |
| **Azure App Service** | PaaS | Web apps, APIs, mobile backends |
| **Azure Functions** | Serverless | Event-driven, short-duration tasks |
| **Azure Container Instances (ACI)** | Container | Quick burst containers, no orchestration |
| **Azure Kubernetes Service (AKS)** | Container orchestration | Microservices, complex container workloads |
| **Azure Container Apps** | Serverless containers | Microservices without K8s complexity |
| **Azure Batch** | HPC jobs | Large parallel compute jobs |
| **Azure Spring Apps** | PaaS Java | Spring Boot microservices |

> **Exam tip:** SLA guarantee requirements usually eliminate dev/test tiers or
> single-instance designs. When the scenario says "guaranteed uptime", choose
> a production tier and design for redundancy (multiple instances/zones/regions).

## Compute Decision Flow

```mermaid
--8<-- "azure/diagrams/compute/compute-decision-flow.mmd"
```

> **Exam tip:** Start with OS control (VM), then container vs. code, then
> serverless vs. always-on. ACA is the default for containerised
> microservices when you do not need full Kubernetes API access.

## App Service Plans (Tiers)

| Tier | Category | Features |
| --- | --- | --- |
| **Free / Shared (F1/D1)** | Dev/Test | No SLA, shared infra, no custom domain SSL |
| **Basic (B1–B3)** | Dev/Test | Dedicated VMs, manual scale (up to 3 instances) |
| **Standard (S1–S3)** | Production | Auto-scale, custom domain, SSL, deployment slots (5) |
| **Premium (P1v3–P3v3)** | Production | More RAM/CPU, VNet integration, 20 deployment slots |
| **Isolated (I1v2–I3v2)** | Mission-critical | Dedicated ASE, VNet isolated, 100 instances |

> Deployment slots only available on **Standard** tier and above.

> **SLA note:** Free/Shared tiers are not SLA-backed production tiers. Questions
> that require a formal uptime guarantee should point to paid production tiers
> with redundant instances.

## Azure Functions Hosting Plans

| Plan | Scale | Cold Start | Use Case |
| --- | --- | --- | --- |
| **Consumption** | Auto (0 to N) | Yes | Sporadic, unpredictable traffic |
| **Premium** | Pre-warmed instances | No | No cold start, VNet, longer execution |
| **Dedicated (App Service)** | Manual / autoscale | No | Predictable load, reuse existing plan |

> **SLA note:** Consumption is optimized for elastic execution and can include
> cold starts. For strict uptime or latency guarantees, exam scenarios typically
> favour Premium or Dedicated hosting with warm capacity.

## Runtime & Language Fit (Functions vs Logic Apps vs App Service)

| Service | Code Model | Common Languages / Runtime Options | Best Fit |
| --- | --- | --- | --- |
| **Azure Functions** | Code-first serverless functions with triggers/bindings | C#, JavaScript/TypeScript, Python, Java, PowerShell, custom handlers (for other runtimes) | Event-driven workloads and short units of compute |
| **Logic Apps** | Low-code workflow orchestration with connectors | No primary app-language requirement; optional inline code for small transforms; can call Functions for full custom code | Integration workflows, B2B, SaaS orchestration |
| **Azure App Service** | Always-on web/API hosting (code or container) | .NET, Node.js, Java, Python, PHP, Ruby, or custom container images | Web apps and APIs with full framework/runtime control |

```mermaid
--8<-- "azure/diagrams/compute/runtime-language-fit-functions-vs-logic-apps-vs-app-service.mmd"
```

> **Exam tip:** If the requirement starts with "which language can I run?",
> Functions and App Service are runtime-first choices; Logic Apps is primarily
> workflow-first and typically uses connectors plus optional inline code or
> Function calls for custom logic.

## Serverless / Event-Driven Selection

```mermaid
--8<-- "azure/diagrams/compute/serverless-event-driven-selection.mmd"
```

> **Exam tip:** Use Azure Functions (Consumption) for short-lived, stateless, code-first triggers.
> Use Durable Functions (Premium/Dedicated) for stateful orchestration or fan-out patterns.
> Use Logic Apps Consumption for simple enterprise/B2B workflows with low-code connectors.
> Use Logic Apps Standard when you need ISE-like VNet isolation or single-tenant deployment.
> Use Azure Container Apps when execution duration exceeds Functions limits or you need a custom runtime.

## Azure Container Apps vs AKS vs ACI

| Dimension | ACI | ACA | AKS |
| --- | --- | --- | --- |
| **Control plane** | None — single container group | Managed (Envoy/KEDA/Dapr hidden) | Full K8s API access |
| **Scale trigger** | Manual / ARM template | KEDA (HTTP, queue, cron, custom) | HPA / KEDA (self-managed) |
| **Dapr integration** | No | Native sidecar injection | Manual Dapr install |
| **Revision management** | No | Yes — traffic split across revisions | Rolling deploy via K8s |
| **VNet integration** | Yes (inject into subnet) | Yes (environment-level) | Yes (CNI plugin) |
| **Cost model** | Per second, vCPU + memory | Per vCPU-s + memory-s (scale to zero) | Node pool VMs (always on) |
| **Ops overhead** | Minimal | Low | High (cluster upgrades, node pools) |

```mermaid
--8<-- "azure/diagrams/compute/azure-container-apps-vs-aks-vs-aci.mmd"
```

> **Exam tip:** ACA uses KEDA under the hood and supports **scale-to-zero** for HTTP and
> queue-based triggers — similar to Consumption plan Functions but for containerised workloads.
> Choose ACA over Functions when you need a custom runtime, Dapr service invocation, or
> revision-based traffic splitting. Choose AKS when the scenario requires direct Kubernetes
> API access, custom admission webhooks, or specific CNI configuration.
> Choose App Service Containers for simple, single-container web apps that benefit from
> built-in deployment slots and App Service features without microservice overhead.
> Use ACI for one-off batch jobs or CI/CD pipeline steps that need an isolated container burst.

## AKS Scaling Mechanisms

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Horizontal Pod Autoscaler (HPA)** | Pod | Namespace | Scale pod replicas based on CPU/memory or custom metrics | Built-in K8s controller; works with KEDA for custom metrics |
| **Cluster Autoscaler** | Node | Node pool | Add or remove VM nodes when pods cannot be scheduled | Integrated with AKS node pools; respects PodDisruptionBudgets |
| **Virtual Nodes (Virtual Kubelet)** | Node (virtual) | Cluster | Burst overflow pods to Azure Container Instances instantly | No node provisioning delay; serverless burst; ACI pricing |

```mermaid
--8<-- "azure/diagrams/compute/aks-scaling-mechanisms.mmd"
```

> **Exam tip:** HPA scales pods; Cluster Autoscaler scales nodes. Virtual Nodes
> (Virtual Kubelet) burst workloads to ACI with no node-provisioning delay — choose
> this when the requirement mentions instant scale-out or cost-optimised spikes.

## Virtual Machine SKU Families

| Family | Purpose |
| --- | --- |
| **D-series** | General purpose — balanced CPU/memory |
| **E-series** | Memory optimized — databases, caches |
| **F-series** | Compute optimized — batch, game servers |
| **N-series** | GPU — AI/ML, rendering |
| **L-series** | Storage optimized — NoSQL, data warehousing |
| **M-series** | Large memory — SAP HANA |
| **B-series** | Burstable — dev/test, low-sustained CPU |

## HPC Networking — RDMA

Remote Direct Memory Access (RDMA) enables VM-to-VM communication that bypasses the OS kernel,
delivering microsecond latency and high throughput for tightly coupled HPC and AI training
workloads. RDMA-capable VM sizes (H-series, HB-series, HC-series, ND-series) must be deployed
in an **InfiniBand-enabled** cluster via a Placement Group or proximity placement group.

> **Exam tip:** Choose RDMA-capable VM sizes (H, HB, HC, ND series) when the requirement
> mentions MPI workloads, tightly coupled HPC, or GPU-to-GPU training that cannot tolerate
> standard Ethernet latency. RDMA is not available on general-purpose D/E-series VMs.

## CI/CD — Azure Pipelines Agent

| Service | Layer | Scope | Use Case | Key Feature |
| --- | --- | --- | --- | --- |
| **Microsoft-hosted agent** | Managed PaaS | Public internet | Standard builds with no VNet or private resource access | Fresh VM per job; no maintenance; limited to public endpoints |
| **Self-hosted agent** | IaaS / container | Customer VNet | Builds needing private registry, on-prem artifact feeds, or VNet-isolated resources | Agent runs as a service on a VM or container; persists between jobs |

> **Exam tip:** Choose a self-hosted Azure Pipelines agent when the build must access resources
> inside a private VNet (e.g. Azure Container Registry with private endpoint, on-prem NuGet feed,
> or private AKS API server). Microsoft-hosted agents run outside your VNet and cannot reach
> private endpoints without additional networking configuration.

## Caching

### Azure Cache for Redis

| Tier | Replication | Clustering | Use Case | Key Feature |
|---|---|---|---|---|
| Basic | No | No | Dev/test only | Single node, no SLA |
| Standard | Yes (primary + replica) | No | Production general | 99.9% SLA, failover |
| Premium | Yes | Yes (up to 10 shards) | High throughput, persistence | VNet, geo-replication, RDB/AOF |
| Enterprise | Yes | Yes (OSS Redis cluster) | Ultra-low latency, RediSearch | Active geo-replication, 99.999% SLA |
| Enterprise Flash | Yes | Yes | Large datasets, cost optimisation | NVMe + DRAM tiering |

> **Exam tip:** Choose Premium when VNet injection or geo-replication is required.
> Choose Enterprise when active-active multi-region or RediSearch/RedisBloom modules are needed.

**Eviction policies (exam-relevant):**

- `volatile-lru` — evict least-recently-used keys that have a TTL set (default safe choice)
- `allkeys-lru` — evict any LRU key (use when all keys are equally expendable)
- `noeviction` — return errors when memory is full (use for session stores where data loss is unacceptable)

#### Tier Selection Decision Flow

```mermaid
--8<-- "azure/diagrams/compute/azure-cache-for-redis.mmd"
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
--8<-- "azure/diagrams/compute/availability-decision-flow.mmd"
```

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
--8<-- "azure/diagrams/compute/vm-family-decision-flow.mmd"
```
