# Proposal: Issue #1 — Fix Incorrect ReadOnly Lock Description

## Overview

The Locks table in `docs/Azure-CheatSheet.md` contains a factually incorrect description for the **ReadOnly** lock type. It currently states the lock prevents "Create and delete operations (modifications)", which implies update operations are still permitted. In reality, a ReadOnly lock blocks all write operations — create, update, and delete — leaving only read access. This fix corrects the ReadOnly row, verifies the CanNotDelete row, and adds a reference link to the official Azure documentation.

## Issues

### Issue 1
**File:** `docs/Azure-CheatSheet.md`
**Problem:** Line 561 — the ReadOnly lock description reads "Create and delete operations (modifications)", incorrectly omitting update operations and misleading exam candidates about what a ReadOnly lock actually blocks.
**Fix:** Update the ReadOnly row to "All write operations (create, update, delete) — read access only". Verify the CanNotDelete row (line 562) is accurate ("Delete only — updates still allowed" is correct). Add a footnote or inline source link to the official Microsoft Learn Azure Locks documentation.
