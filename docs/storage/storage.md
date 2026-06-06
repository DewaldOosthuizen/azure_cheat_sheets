## Storage Account Types

| Type | Supported Services | Use Case |
| --- | --- | --- |
| **Standard GPv2** | Blob, File, Queue, Table | General purpose, most scenarios |
| **Premium Block Blobs** | Block Blob only | Low-latency blob I/O, analytics |
| **Premium File Shares** | Azure Files only | High-performance SMB/NFS shares |
| **Premium Page Blobs** | Page Blob only | Unmanaged VM disks |

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
--8<-- "diagrams/storage/blob-storage-access-tiers.mmd"
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
--8<-- "diagrams/storage/storage-redundancy.mmd"
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
| **Azure Data Lake Storage Gen2** | Hierarchical Blob | Analytics at scale | POSIX ACL, Spark-optimized |

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
--8<-- "diagrams/storage/managed-disk-selection.mmd"
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
--8<-- "diagrams/storage/storage-replication-decision-flow.mmd"
```
