#!/usr/bin/env python3
"""Extract section content from AZ-305.md and AZ-104.md into snippet files.

Run once from repo root:
    python scripts/extract_sections.py

Note: outputs to docs/azure/files/<domain>/<domain>.md
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS = REPO_ROOT / "docs"

# Rename mapping for diagram references (old -> new, without diagrams/ prefix)
DIAGRAM_RENAMES: dict[str, str] = {
    # networking
    "networking/az305-decision-flow.mmd": "networking/decision-flow.mmd",
    "networking/az305-decision-flow-api-gateway-selection.mmd": "networking/decision-flow-api-gateway-selection.mmd",
    "networking/az305-virtual-networks-vnet.mmd": "networking/virtual-networks-vnet.mmd",
    "networking/az305-decision-flow-network-security-selection.mmd": "networking/decision-flow-network-security-selection.mmd",
    "networking/az305-connectivity-patterns.mmd": "networking/connectivity-patterns.mmd",
    "networking/az104-vnet-connectivity-decision-flow.mmd": "networking/vnet-connectivity-decision-flow.mmd",
    "networking/az104-nsg-rule-evaluation.mmd": "networking/nsg-rule-evaluation.mmd",
    "networking/az104-load-balancer-sku-decision-flow.mmd": "networking/load-balancer-sku-decision-flow.mmd",
    # security
    "security/az104-key-vault-access-decision-flow.mmd": "security/key-vault-access-decision-flow.mmd",
    "security/az104-defender-for-cloud-coverage.mmd": "security/defender-for-cloud-coverage.mmd",
    # storage
    "storage/az305-blob-storage-access-tiers.mmd": "storage/blob-storage-access-tiers.mmd",
    "storage/az305-storage-redundancy.mmd": "storage/storage-redundancy.mmd",
    "storage/az104-managed-disk-selection.mmd": "storage/managed-disk-selection.mmd",
    "storage/az104-storage-replication-decision-flow.mmd": "storage/storage-replication-decision-flow.mmd",
    # monitoring
    "monitoring/az305-azure-monitor-ecosystem.mmd": "monitoring/azure-monitor-ecosystem.mmd",
    "monitoring/az104-agent-selection-decision-flow.mmd": "monitoring/agent-selection-decision-flow.mmd",
    "monitoring/az104-diagnostic-settings-routing.mmd": "monitoring/diagnostic-settings-routing.mmd",
    # compute
    "compute/az305-compute-decision-flow.mmd": "compute/compute-decision-flow.mmd",
    "compute/az305-runtime-language-fit-functions-vs-logic-apps-vs-app-service.mmd": "compute/runtime-language-fit-functions-vs-logic-apps-vs-app-service.mmd",
    "compute/az305-serverless-event-driven-selection.mmd": "compute/serverless-event-driven-selection.mmd",
    "compute/az305-azure-container-apps-vs-aks-vs-aci.mmd": "compute/azure-container-apps-vs-aks-vs-aci.mmd",
    "compute/az305-aks-scaling-mechanisms.mmd": "compute/aks-scaling-mechanisms.mmd",
    "compute/az305-azure-cache-for-redis.mmd": "compute/azure-cache-for-redis.mmd",
    "compute/az104-vm-family-decision-flow.mmd": "compute/vm-family-decision-flow.mmd",
    "compute/az104-availability-decision-flow.mmd": "compute/availability-decision-flow.mmd",
    # identity
    "identity/az305-system-identity-type-decision-flow.mmd": "identity/system-identity-type-decision-flow.mmd",
    "identity/az305-entra-identity-scenario-decision-flow.mmd": "identity/entra-identity-scenario-decision-flow.mmd",
    "identity/az104-rbac-role-assignment-decision-flow.mmd": "identity/rbac-role-assignment-decision-flow.mmd",
    "identity/az104-entra-id-join-type-decision-flow.mmd": "identity/entra-id-join-type-decision-flow.mmd",
    # ha-dr
    "ha-dr/az305-key-concepts.mmd": "ha-dr/key-concepts.mmd",
    "ha-dr/az104-ha-dr-decision-flow.mmd": "ha-dr/ha-dr-decision-flow.mmd",
    "ha-dr/az104-recovery-services-vault-structure.mmd": "ha-dr/recovery-services-vault-structure.mmd",
    # governance
    "governance/az305-management-hierarchy.mmd": "governance/management-hierarchy.mmd",
    "governance/az305-governance-enforcement-decision-flow.mmd": "governance/governance-enforcement-decision-flow.mmd",
    "governance/az104-policy-assignment-scope-hierarchy.mmd": "governance/policy-assignment-scope-hierarchy.mmd",
    "governance/az104-management-hierarchy-decision-flow.mmd": "governance/management-hierarchy-decision-flow.mmd",
    # messaging
    "messaging/az305-decision-flowchart.mmd": "messaging/decision-flowchart.mmd",
    "messaging/az305-logic-apps-vs-azure-functions-vs-durable-functions.mmd": "messaging/logic-apps-vs-azure-functions-vs-durable-functions.mmd",
    "messaging/az104-messaging-decision-flow.mmd": "messaging/messaging-decision-flow.mmd",
    "messaging/az104-service-bus-sku-decision-flow.mmd": "messaging/service-bus-sku-decision-flow.mmd",
    # waf
    "waf/az305-five-pillar-summary.mmd": "waf/five-pillar-summary.mmd",
    "waf/az305-decision-flow-pillar-trade-off-navigator.mmd": "waf/decision-flow-pillar-trade-off-navigator.mmd",
    "waf/az104-tag-inheritance-architecture.mmd": "waf/tag-inheritance-architecture.mmd",
    "waf/az104-cost-management-decision-flow.mmd": "waf/cost-management-decision-flow.mmd",
}


def fix_diagram_refs(text: str) -> str:
    """Replace old exam-prefixed diagram paths with new agnostic paths."""
    for old, new in DIAGRAM_RENAMES.items():
        text = text.replace(f"diagrams/{old}", f"azure/diagrams/{new}")
    return text


def remove_also_relevant_for(lines: list[str]) -> list[str]:
    """Remove consecutive '> Also relevant for:' blockquote lines (and trailing blank)."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is an 'Also relevant for' callout
        if line.strip().startswith("> Also relevant for:") or line.strip().startswith(
            ">Also relevant for:"
        ):
            # Skip this line and all following '> ' lines that are part of same blockquote
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                i += 1
            # Skip one trailing blank line if present
            if i < len(lines) and lines[i].strip() == "":
                i += 1
        else:
            result.append(line)
            i += 1
    return result


def extract_section(file_lines: list[str], heading_line: int, sep_line: int | None) -> str:
    """Extract section body between heading and separator (1-indexed).

    heading_line: the line number of the '# SECTION' heading (excluded from snippet)
    sep_line: the line number of the '---' separator (excluded), or None for end-of-file
    """
    # Convert to 0-indexed
    start = heading_line  # line after heading (0-indexed = heading_line)
    end = (sep_line - 1) if sep_line is not None else len(file_lines)  # exclude sep line

    section_lines = file_lines[start:end]

    # Remove leading blank line(s) right after heading
    while section_lines and section_lines[0].strip() == "":
        section_lines = section_lines[1:]

    # Remove "Also relevant for:" callouts
    section_lines = remove_also_relevant_for(section_lines)

    # Remove trailing blank lines
    while section_lines and section_lines[-1].strip() == "":
        section_lines = section_lines[:-1]

    content = "".join(section_lines)
    return fix_diagram_refs(content)


def main() -> None:
    az305_lines = (
        (DOCS / "azure/cheat_sheets/AZ-305.md").read_text(encoding="utf-8").splitlines(keepends=True)
    )
    az104_lines = (
        (DOCS / "azure/cheat_sheets/AZ-104.md").read_text(encoding="utf-8").splitlines(keepends=True)
    )

    # AZ-305 section boundaries (1-indexed line numbers)
    # heading_line is where # SECTION is, sep_line is where --- is
    az305_sections = {
        "networking": (87, 273),
        "security": (275, 391),
        "storage": (393, 522),
        "monitoring": (524, 589),
        "compute": (591, 784),
        "identity": (786, 876),
        "ha-dr": (878, 922),
        "governance": (924, 1023),
        "messaging": (1025, 1080),
        "waf": (1082, None),
    }

    # AZ-104 section boundaries (1-indexed line numbers)
    az104_sections = {
        "networking": (23, 80),
        "security": (82, 124),
        "storage": (126, 168),
        "monitoring": (170, 218),
        "compute": (220, 263),
        "identity": (265, 303),
        "ha-dr": (305, 336),
        "governance": (338, 376),
        "messaging": (378, 418),
        "waf": (420, None),
    }

    for domain, (h305, s305) in az305_sections.items():
        az305_content = extract_section(az305_lines, h305, s305)  # h305 is 1-indexed
        az104_h, az104_s = az104_sections[domain]
        az104_content = extract_section(az104_lines, az104_h, az104_s)

        # Merge: AZ-305 as base, append AZ-104 content if it adds unique info
        # For simplicity, check if az104_content contains unique subsections
        merged = merge_content(domain, az305_content, az104_content)

        # Write snippet file
        snippet_dir = DOCS / "azure" / "files" / domain
        snippet_dir.mkdir(exist_ok=True)
        snippet_file = snippet_dir / f"{domain}.md"
        snippet_file.write_text(merged, encoding="utf-8")
        print(f"Written: {snippet_file}")


def merge_content(domain: str, az305: str, az104: str) -> str:
    """Merge AZ-305 and AZ-104 section content into a single snippet.

    Strategy:
    - AZ-305 content is the architectural base (more depth)
    - AZ-104 content has operational/admin detail (different tables, different subsections)
    - Include both, deduplicating subsections that appear in both
    """
    # Find headings in each
    az305_headings = set(re.findall(r"^## .+", az305, re.MULTILINE))
    az104_headings = set(re.findall(r"^## .+", az104, re.MULTILINE))

    # Find AZ-104 subsections NOT in AZ-305 (headings unique to AZ-104)
    unique_az104_headings = az104_headings - az305_headings

    if not unique_az104_headings:
        # AZ-104 content is fully covered by AZ-305 or nearly so
        return az305.rstrip() + "\n"

    # Extract unique AZ-104 subsections
    az104_unique_parts = []
    for heading in sorted(unique_az104_headings):
        # Extract the subsection
        pattern = re.escape(heading) + r"(.*?)(?=\n## |\Z)"
        m = re.search(pattern, az104, re.DOTALL)
        if m:
            section_text = heading + m.group(1)
            az104_unique_parts.append(section_text.rstrip())

    if az104_unique_parts:
        merged = az305.rstrip() + "\n\n" + "\n\n".join(az104_unique_parts) + "\n"
    else:
        merged = az305.rstrip() + "\n"

    return merged


if __name__ == "__main__":
    main()
