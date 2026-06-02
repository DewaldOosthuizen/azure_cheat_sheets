# Tasks: Issue #2

## Documentation — docs/Azure-CheatSheet.md

- [ ] Add entry `9. [Messaging & Integration](#messaging--integration)` to the Table of Contents block (after the Governance entry, before the closing `---`).
- [ ] Append `# MESSAGING & INTEGRATION` top-level heading before the footer note at line 568.
- [ ] Add service comparison table with columns: Service | Pattern | Ordering | Replay | Use Case — covering Service Bus Queue, Service Bus Topic, Event Grid, Event Hub, Storage Queue.
- [ ] Add Mermaid `flowchart TD` decision diagram routing: events vs messages → ordering → fan-out → correct service.
- [ ] Verify Mermaid diagram renders without syntax errors (open in a Mermaid live editor or GitHub preview).
- [ ] Add Logic Apps vs Azure Functions vs Durable Functions comparison table with columns: Service | Best For | Trigger Model | State | Pricing Model.
- [ ] Add exam-tip callout for dead-letter queues: triggers (TTL expiry, max delivery count exceeded), monitoring via Azure Monitor / Service Bus Explorer.
- [ ] Add exam-tip callout for sessions and partitioning: session-enabled queues guarantee ordered processing per session key; partitioning scales throughput across message brokers.
- [ ] Add exam-tip callout for consumer groups and retention: Event Hub consumer groups isolate read positions per downstream system; configure retention (1–90 days) to enable event replay.

## Documentation — README.md

- [ ] Inspect README.md for any domain/section list and add "Messaging & Integration" if one is present; skip if no such list exists.

## Validation

- [ ] Confirm the new section header `# MESSAGING & INTEGRATION` appears in the rendered document's table of contents anchor (`#messaging--integration`).
- [ ] Confirm all acceptance criteria in GitHub issue #2 are met: comparison table, Mermaid flowchart, Logic Apps comparison, 3+ exam tips.
