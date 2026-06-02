# Proposal: Issue #2 — Add Messaging & Integration Section

## Overview

The `docs/Azure-CheatSheet.md` currently covers eight domains (Networking, Security, Storage,
Monitoring, Compute, Identity, HA/DR, Governance) but is entirely silent on the Messaging &
Integration domain, which is explicitly tested in AZ-305. Candidates designing event-driven,
message-queuing, or hybrid integration architectures have no guidance in the document. The fix
is to append a new top-level `# MESSAGING & INTEGRATION` section to the cheat sheet covering
Service Bus, Event Grid, Event Hub, Storage Queues, Logic Apps, Azure Functions, and Durable
Functions — including a service-comparison table, a Mermaid decision flowchart, a Logic Apps
vs Functions comparison, and key exam-tip callouts. The Table of Contents entry for the new
section will also be added.

---

## Issues

### Issue 1

**File:** `docs/Azure-CheatSheet.md`

**Problem:** The file has no Messaging & Integration section. The Table of Contents (lines 8–18)
lists eight sections; the document body ends at line 568 with a footer note. AZ-305 exam topics
covering Service Bus, Event Grid, Event Hub, Logic Apps, and hybrid integration patterns are
entirely absent.

**Fix:**

1. Add a 9th entry to the Table of Contents block (after line 17, before the closing `---`):

Before (lines 8–18):
```markdown
## Table of Contents

1. [Networking](#networking)
2. [Security](#security)
3. [Storage](#storage)
4. [Monitoring & Observability](#monitoring--observability)
5. [Compute](#compute)
6. [Identity & Access](#identity--access)
7. [High Availability & Disaster Recovery](#high-availability--disaster-recovery)
8. [Governance](#governance)
```

After:
```markdown
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
```

2. Append a new `# MESSAGING & INTEGRATION` section before the footer note (after line 566,
   before line 568). The section must contain:

   a) **Service comparison table** — columns: Service | Pattern | Ordering | Replay | Use Case.
      Rows: Service Bus Queue, Service Bus Topic, Event Grid, Event Hub, Storage Queue.

   Example:
   ```markdown
   | Service | Pattern | Ordering | Replay | Use Case |
   |---|---|---|---|---|
   | **Service Bus Queue** | Message (P2P) | FIFO optional | No | Reliable command delivery |
   | **Service Bus Topic** | Message (pub/sub) | FIFO optional | No | Fan-out with filters |
   | **Event Grid** | Event (reactive) | No | No | Resource change reactions |
   | **Event Hub** | Stream (telemetry) | Per-partition | Yes (retention) | IoT, log ingestion |
   | **Storage Queue** | Message (P2P) | Best-effort | No | Simple, cheap async |
   ```

   b) **Mermaid decision flowchart** — guides readers through: events vs messages, ordering
      requirements, fan-out needs, leading to the correct service choice.

   Example skeleton:
   ```mermaid
   flowchart TD
       A[Need async communication?] --> B{Events or Messages?}
       B -- Events --> C{Fan-out to multiple subscribers?}
       B -- Messages --> D{Ordering required?}
       C -- Yes --> E[Event Grid]
       C -- No / High-volume stream --> F[Event Hub]
       D -- Yes --> G[Service Bus Queue - FIFO sessions]
       D -- No --> H{Volume very high / simple?}
       H -- Yes --> I[Storage Queue]
       H -- No --> J[Service Bus Queue]
   ```

   c) **Logic Apps vs Azure Functions vs Durable Functions** comparison table — columns:
      Service | Best For | Trigger Model | State | Pricing Model.

   d) **Exam-tip callouts** (minimum 3):
      - Dead-letter queues: what triggers them, how to monitor.
      - Sessions & partitioning: session-enabled queues for ordered processing; partitioning
        for throughput scaling.
      - Consumer groups & retention: Event Hub consumer groups allow independent readers;
        retention window (1–90 days) enables replay.

### Issue 2

**File:** `README.md`

**Problem:** If `README.md` contains a Table of Contents or section list referencing the cheat
sheet domains, it does not include Messaging & Integration.

**Fix:** Inspect `README.md` and, if a domain list is present, add "Messaging & Integration"
to it so the README accurately reflects the document's coverage. If no such list exists, no
change is needed.
