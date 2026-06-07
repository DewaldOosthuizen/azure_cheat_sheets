# Storage

## Storage Account Types

| Type | Supported Services | Supported Replication | Use Case |
| --- | --- | --- | --- |
| **Standard GPv2** | Blob, File, Queue, Table | LRS, ZRS, GRS, RA-GRS, GZRS, RA-GZRS | General purpose, most scenarios |
| **Premium Block Blobs** | Block Blob only | LRS, ZRS | Low-latency blob I/O, analytics |
| **Premium File Shares** | Azure Files only | LRS, ZRS | High-performance SMB/NFS shares |
| **Premium Page Blobs** | Page Blob only | LRS only | Unmanaged VM disks |

> **Exam tip:** Premium storage accounts support LRS and ZRS only — geo-redundancy
> (GRS / GZRS) is not available. Standard GPv2 supports all six replication tiers.

## Blob Storage Access Tiers

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Hot** | Blob access tier | Frequently accessed data; no minimum retention | Lowest access cost; highest storage cost |
| **Cool** | Blob access tier | Infrequently accessed data; min 30-day retention | Lower storage cost; higher per-operation cost |
| **Cold** | Blob access tier | Rarely accessed data; min 90-day retention | Lower storage cost than Cool; higher access cost |
| **Archive** | Blob access tier | Long-term archival; min 180-day retention | Lowest storage cost; requires rehydration (hours) before read |

> **Exam tip:** Use Lifecycle Management policies to auto-transition blobs
> through tiers. Archive blobs must be rehydrated to Hot or Cool before access;
> plan for rehydration latency in recovery scenarios.

```mermaid
--8<-- "azure/diagrams/storage/blob-storage-access-tiers.mmd"
```

## Storage Redundancy

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **LRS** | Storage redundancy | Dev/test; lowest cost; no zone/regional DR requirement | 3 copies in one datacenter; 99.9999999% durability |
| **ZRS** | Storage redundancy | Regional HA; zone-failure tolerance; no cross-region DR | 3 copies across 3 AZs in one region; no data loss on zone outage |
| **GRS** | Storage redundancy | Cross-region DR; secondary readable only after failover | 6 copies (3 primary + 3 secondary region); RPO < 15 min |
| **RA-GRS** | Storage redundancy | Cross-region DR with continuous read access to secondary | GRS + secondary endpoint always readable; 99.99% read SLA |
| **GZRS** | Storage redundancy | HA + cross-region DR without secondary read requirement | 3 AZs primary + geo-replicated secondary; highest resilience |
| **RA-GZRS** | Storage redundancy | Maximum durability with continuous secondary read access | GZRS + secondary endpoint always readable; 99.99% read SLA |

```mermaid
--8<-- "azure/diagrams/storage/storage-redundancy.mmd"
```

> **Exam tip:** Choose RA-GRS when zone resilience in the primary region is
> not required but continuous read access to the secondary is. Choose GZRS
> (or RA-GZRS) when you need both zone-level resilience in the primary region
> and geo-redundancy — GZRS is strictly more resilient than RA-GRS for the
> same read-availability requirement.

## Azure Files vs Blob vs Disk vs NetApp

| Service | Protocol | Use Case |
| --- | --- | --- |
| **Azure Blob** | REST/HTTP | Unstructured data, backups, media, data lake |
| **Azure Files** | SMB 3.0 / NFS 4.1 | Lift-and-shift file shares, shared app config |
| **Azure NetApp Files** | NFS / SMB | High-perf enterprise workloads, SAP HANA |
| **Azure Managed Disks** | iSCSI (internal) | VM OS and data disks |
| **Azure Queue Storage** | REST | Decoupled async messaging (simple) |
| **Azure Table Storage** | REST | NoSQL key-value, schema-less |

## Data Integration & Movement

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Azure Data Factory** | Cloud ETL / orchestration | Batch data pipelines between cloud and on-prem stores | 90+ connectors, pipeline scheduling, data flows |
| **Azure Databricks** | Lakehouse analytics | Large-scale Spark engineering, Delta Lake, ML pipelines | Managed Apache Spark with collaborative notebooks and autoscaling clusters |
| **Azure-SSIS Integration Runtime** | Lift-and-shift ETL | Running existing SSIS packages in ADF without rewrite | Managed SSIS runtime inside ADF; supports Azure SQL MI as SSISDB host |
| **Azure Data Box** | Offline bulk transfer | Initial migration of large datasets (TB–PB) to Azure when bandwidth is constrained | Physical device shipped by Microsoft; encrypted, tamper-evident |
| **Azure Data Box Gateway** | Edge ingestion | Continuous data upload from on-prem to Azure Blob/Files | Virtual appliance; no physical device needed |
| **Azure Data Box Edge** | Edge compute + transfer | Data processing and inference at the edge before upload | Runs Azure IoT Edge modules and FPGA-accelerated ML inference |

> **Exam tip:** Choose Azure Data Factory when the requirement mentions pipeline orchestration,
> scheduled data movement, or running SSIS packages in the cloud (via Azure-SSIS IR). Choose
> Data Box (physical) for offline migrations where internet transfer would take weeks. Choose
> Data Box Gateway for ongoing edge-to-cloud ingestion without a physical device.

> **Exam tip:** Choose Azure Databricks when the requirement emphasizes Spark-native
> data engineering, Delta Lake, collaborative notebooks, or large-scale ML data
> processing. Choose Synapse when a unified SQL + Spark analytics workspace is the
> stronger requirement.

## Database Storage Options

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Azure SQL Database** | Relational PaaS | Cloud-native OLTP | Serverless, elastic pool, hyperscale |
| **Azure SQL Managed Instance** | Relational PaaS | SQL Server lift-and-shift | Near 100% SQL Server compat, VNet inject |
| **Cosmos DB** | NoSQL multi-model | Global distributed, low-latency | Multi-region writes, 5 APIs |
| **Azure Database for PostgreSQL** | Relational PaaS | OSS PostgreSQL | Flexible server, HA, read replicas |
| **Azure Database for MySQL** | Relational PaaS | OSS MySQL | Flexible server |
| **Azure Synapse Analytics** | Analytics DW | OLAP, big data | Spark + SQL pool |
| **Azure Data Lake Storage Gen2** | Hierarchical Blob | Analytics at scale | POSIX ACL, Hierarchical Namespace, Spark-optimized |

### Azure SQL Database Service Tiers

Azure SQL Database supports two purchasing models with different tier sets.

**DTU model** (bundled compute + storage + IO):

| Tier | Max Storage | Use Case |
| --- | --- | --- |
| **Basic** | 2 GB | Dev/test, small low-traffic databases |
| **Standard** | 1 TB | Web applications, departmental workloads |
| **Premium** | 4 TB | Mission-critical OLTP, low latency, OLTP in-memory |

**vCore model** (compute and storage billed independently):

| Tier | Use Case | Key Feature |
| --- | --- | --- |
| **General Purpose** | Standard production OLTP | Remote SSD storage; cost-balanced; supports Serverless auto-pause |
| **Business Critical** | High I/O, in-memory OLTP, low latency | Local SSD; built-in Always On replicas; one free read replica |
| **Hyperscale** | Very large databases (up to 100 TB) | Distributed page server architecture; near-instant backup and restore |

> **Exam tip:** Hyperscale is only available on Azure SQL Database (not SQL MI). Serverless
> (auto-pause/auto-resume) is only available within the General Purpose vCore tier.
> Business Critical includes a free read-scale replica — no extra licensing required.

### Azure SQL Managed Instance Service Tiers

SQL Managed Instance uses the vCore model only (DTU is not supported).

| Tier | Use Case | Key Feature |
| --- | --- | --- |
| **General Purpose** | Typical performance and standard I/O latency requirements | Remote SSD storage; budget-friendly; suitable for most lift-and-shift workloads |
| **Business Critical** | Low I/O latency and minimal impact from maintenance operations | Local SSD; built-in Always On availability group; one free readable secondary replica |

> **Exam tip:** SQL MI Business Critical provides a built-in read replica at no additional
> cost — use it for read-scale-out or as a reporting endpoint. General Purpose is the
> default tier and covers the majority of lift-and-shift scenarios.

### Cosmos DB Capacity Modes

Cosmos DB does not have service tiers in the traditional sense. Capacity is selected
per container at creation time.

| Mode | Use Case | Key Feature |
| --- | --- | --- |
| **Provisioned Throughput (Manual)** | Predictable, steady-state workloads | Fixed RU/s ceiling; best price per RU at sustained utilisation |
| **Provisioned Throughput (Autoscale)** | Variable workloads with bounded peaks | Scales 10–100% of configured max RU/s; you pay for peak consumed |
| **Serverless** | Sporadic or dev/test workloads | No pre-provisioned capacity; billed per RU consumed per operation |

### Azure Database for PostgreSQL and MySQL — Flexible Server Compute Tiers

Both PostgreSQL and MySQL Flexible Server share the same three compute tiers.

| Tier | Use Case | Key Feature |
| --- | --- | --- |
| **Burstable** | Dev/test, low-traffic applications | Variable CPU (B-series); lowest cost; not for sustained CPU-intensive workloads |
| **General Purpose** | Most production workloads | Balanced CPU/memory ratio; 2–96 vCores |
| **Memory Optimized** | High-concurrency, in-memory analytics, large caches | Higher memory-to-vCore ratio; 2–64 vCores; suited for PostgreSQL connection-heavy workloads |

> **Exam tip:** Burstable tier does not support high-availability (zone-redundant standby)
> or read replicas — choose General Purpose or Memory Optimized when the requirement
> mentions HA, read replicas, or geo-redundancy.

### Azure Synapse Analytics Pool Types

Synapse is not a single database with tiers — it is a workspace containing multiple
pool types that you provision independently.

| Pool Type | Billing Unit | Use Case | Key Feature |
| --- | --- | --- | --- |
| **Serverless SQL Pool** | Per TB of data processed | Ad-hoc T-SQL queries directly over ADLS Gen2 | No infrastructure to provision; always-on; pay-per-query |
| **Dedicated SQL Pool** | Data Warehouse Units (DWU) | Predictable BI/DW workloads with known query patterns | Massively parallel processing; scale DWU up/down without data loss |
| **Apache Spark Pool** | Node-hours (auto-pause supported) | Big data engineering, Delta Lake, ML data pipelines | Managed Spark clusters; auto-scale and auto-pause; integrated notebooks |

> **Exam tip:** Serverless SQL Pool queries ADLS data directly using OPENROWSET — no
> data is loaded or moved. Dedicated SQL Pool requires data to be loaded (COPY INTO or
> PolyBase). When a scenario mentions "query data in place" or "no ETL", the answer is
> Serverless SQL Pool.

## Azure File Sync

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **Azure File Sync Agent** | Hybrid tiering | On-prem Windows Server local cache for an Azure Files share | Cloud tiering stubs cold files locally and retrieves them on access; multiple server endpoints per sync group |

> **Exam tip:** Choose Azure File Sync when the requirement mentions keeping on-prem Windows
> file server access while centralising storage in Azure Files. Cloud tiering frees local disk
> by replacing infrequently accessed files with stubs that are transparently fetched from Azure.

## Azure SQL Purchasing Models

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| **vCore model** | Provisioned or Serverless | New deployments, Azure Hybrid Benefit, Managed Instance | Decouples compute and storage; supports Serverless tier; required for SQL MI |
| **DTU model** | Bundled compute+storage | Legacy workloads, simple cost predictability | Fixed ratio of CPU/memory/IO; Basic/Standard/Premium tiers; not available on SQL MI |

> **Exam tip:** Prefer vCore when you need Azure Hybrid Benefit (bring your own SQL Server
> licence), Serverless auto-pause, or are deploying SQL Managed Instance (DTU not supported).
> DTU is simpler but less flexible — expect AZ-305 questions to favour vCore for new
> cloud-native designs.

## Cosmos DB Consistency Levels (strong → weak)

| Level | Guarantee | Latency | Use Case |
| --- | --- | --- | --- |
| **Strong** | Linearizable reads | Higher | Financial transactions |
| **Bounded Staleness** | Lag bounded by ops/time | Moderate | Global apps, bounded lag OK |
| **Session** | Consistent within session | Low | Per-user data (default) |
| **Consistent Prefix** | No out-of-order reads | Low | Social media feeds |
| **Eventual** | No ordering guarantee | Lowest | High availability, non-critical |

## Cosmos DB — Developer Focus (AZ-204)

**Partition key design rules:**

- Choose a high-cardinality key (many distinct values) to distribute RUs and storage uniformly across logical partitions.
- Avoid hot partitions — a key that concentrates most reads/writes on one partition causes throttling (429 errors).
- The partition key must be immutable — it cannot be changed after the item is created.
- Include the partition key in all queries; without it, Cosmos DB performs a cross-partition fan-out, increasing RU cost and latency.

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| Cosmos DB Provisioned Throughput | RU Model | Predictable, steady-state workloads with defined peak load | Fixed RU/s ceiling; most cost-effective when utilisation is consistently high |
| Cosmos DB Autoscale | RU Model | Variable workloads with bounded but unpredictable peaks | Scales between 10% and 100% of the configured max RU/s; you pay for peak consumed |
| Cosmos DB Serverless | RU Model | Intermittent or unpredictable workloads; development/test | Billed per RU consumed per operation; no pre-provisioned capacity; no SLA for throughput |

> **Exam tip:** Choose serverless for sporadic or unpredictable access patterns where pre-provisioning RUs would be wasteful. Choose autoscale when the workload is variable but has a defined maximum. Choose provisioned (manual) throughput when the load is predictable and steady — it gives a hard cost ceiling and the best price per RU at sustained utilisation.

SDK access pattern (Python — azure-cosmos v4):

```python
from azure.cosmos import CosmosClient, PartitionKey

client = CosmosClient(url=COSMOS_ENDPOINT, credential=COSMOS_KEY)
database = client.create_database_if_not_exists(id="MyDatabase")
container = database.create_container_if_not_exists(
    id="MyContainer",
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400,
)
container.create_item(body={"id": "item1", "category": "gear", "name": "Helmet"})
```

## Blob Storage SAS Tokens

| Service | Type | Best For | Key Feature |
| --- | --- | --- | --- |
| Service SAS | SAS Token | Delegating access to a specific Blob, Queue, Table, or File resource | Signed with the storage account key; scoped to one service type |
| Account SAS | SAS Token | Delegating access across multiple storage services in one token | Signed with the storage account key; broadest scope — use with caution |
| User Delegation SAS | SAS Token | Delegated external access without exposing the account key | Signed with Entra ID (Azure AD) credentials; requires Storage Blob Delegator RBAC role |

> **Exam tip:** User Delegation SAS is the most secure option — it is signed with Entra credentials, not the storage account key. The caller must hold the Storage Blob Delegator role on the storage account. Use it whenever you need to grant time-limited external access without distributing account keys.

SDK pattern (Python — azure-storage-blob v12):

```python
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta, timezone

sas_token = generate_blob_sas(
    account_name=ACCOUNT_NAME,
    container_name="mycontainer",
    blob_name="report.pdf",
    account_key=ACCOUNT_KEY,          # omit and pass user_delegation_key for User Delegation SAS
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1),
)
```

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
--8<-- "azure/diagrams/storage/managed-disk-selection.mmd"
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
--8<-- "azure/diagrams/storage/storage-replication-decision-flow.mmd"
```
