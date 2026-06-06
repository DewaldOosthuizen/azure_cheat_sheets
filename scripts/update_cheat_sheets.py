#!/usr/bin/env python3
"""Update cheat sheets to replace inline sections with --8<-- directives.

Run once from repo root:
    python scripts/update_cheat_sheets.py
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS = REPO_ROOT / "docs"


def remove_also_relevant_for_lines(lines: list[str]) -> list[str]:
    """Remove consecutive '> Also relevant for:' blockquote lines (and following blank)."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("> Also relevant for:"):
            # Skip this and continuation '> ' lines
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                i += 1
            # Skip trailing blank line
            if i < len(lines) and lines[i].strip() == "":
                i += 1
        else:
            result.append(line)
            i += 1
    return result


def update_az305() -> None:
    """Rewrite AZ-305.md so each section body is replaced with a snippet directive."""
    src = DOCS / "cheat_sheets/AZ-305.md"
    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)

    # First, handle the "Also relevant for:" callouts - remove them from AZ-305
    lines = remove_also_relevant_for_lines(lines)

    # Parse by section headings to replace each section body with a snippet directive.
    current_lines = "".join(lines).splitlines(keepends=True)

    # Find section heading positions in the current (already cleaned) text
    section_headings = {
        "networking": "# NETWORKING",
        "security": "# SECURITY",
        "storage": "# STORAGE",
        "monitoring": "# MONITORING & OBSERVABILITY",
        "compute": "# COMPUTE",
        "identity": "# IDENTITY & ACCESS",
        "ha-dr": "# HIGH AVAILABILITY & DISASTER RECOVERY",
        "governance": "# GOVERNANCE",
        "messaging": "# MESSAGING & INTEGRATION",
        "waf": "# WELL-ARCHITECTED FRAMEWORK",
    }

    section_order = [
        "networking",
        "security",
        "storage",
        "monitoring",
        "compute",
        "identity",
        "ha-dr",
        "governance",
        "messaging",
        "waf",
    ]

    # Find heading line indices in current_lines
    heading_positions = {}
    for i, line in enumerate(current_lines):
        stripped = line.strip()
        for domain, heading in section_headings.items():
            if stripped == heading:
                heading_positions[domain] = i

    # Build replacement: for each section, keep heading + snippet + ---
    # For sections between two sections, keep everything from heading to next heading
    # Collect "pre-section" content (before first section heading)
    first_heading_pos = heading_positions["networking"]
    pre_section = current_lines[:first_heading_pos]

    new_lines = list(pre_section)

    for _idx, domain in enumerate(section_order):
        heading_pos = heading_positions[domain]
        heading_line = current_lines[heading_pos]

        # Find the --- separator after this heading
        # Look for '---\n' after heading_pos
        sep_pos = None
        for j in range(heading_pos + 1, len(current_lines)):
            if current_lines[j].strip() == "---":
                sep_pos = j
                break

        # Add heading
        new_lines.append(heading_line)
        new_lines.append("\n")
        # Add snippet directive
        new_lines.append(f'--8<-- "{domain}/{domain}.md"\n')
        new_lines.append("\n")

        if sep_pos is not None:
            # Add separator
            new_lines.append("---\n")
            new_lines.append("\n")
        # (last section has no separator)

    # Write
    result = "".join(new_lines)
    src.write_text(result, encoding="utf-8")
    print(f"Updated: {src}")


def update_az104() -> None:
    """Rewrite AZ-104.md so each section body is replaced with a snippet directive."""
    src = DOCS / "cheat_sheets/AZ-104.md"
    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)

    section_headings = {
        "networking": "# NETWORKING",
        "security": "# SECURITY",
        "storage": "# STORAGE",
        "monitoring": "# MONITORING & OBSERVABILITY",
        "compute": "# COMPUTE",
        "identity": "# IDENTITY & ACCESS",
        "ha-dr": "# HIGH AVAILABILITY & DISASTER RECOVERY",
        "governance": "# GOVERNANCE",
        "messaging": "# MESSAGING & INTEGRATION",
        "waf": "# WELL-ARCHITECTED FRAMEWORK",
    }

    section_order = [
        "networking",
        "security",
        "storage",
        "monitoring",
        "compute",
        "identity",
        "ha-dr",
        "governance",
        "messaging",
        "waf",
    ]

    # Find heading positions
    heading_positions = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        for domain, heading in section_headings.items():
            if stripped == heading:
                heading_positions[domain] = i

    # Build pre-section content (up to first section)
    first_heading_pos = heading_positions["networking"]
    pre_section = lines[:first_heading_pos]

    new_lines = list(pre_section)

    for domain in section_order:
        heading_pos = heading_positions[domain]
        heading_line = lines[heading_pos]

        # Find the --- separator after heading
        sep_pos = None
        for j in range(heading_pos + 1, len(lines)):
            if lines[j].strip() == "---":
                sep_pos = j
                break

        # Add heading
        new_lines.append(heading_line)
        new_lines.append("\n")
        new_lines.append(f'--8<-- "{domain}/{domain}.md"\n')
        new_lines.append("\n")

        if sep_pos is not None:
            new_lines.append("---\n")
            new_lines.append("\n")

    result = "".join(new_lines)
    src.write_text(result, encoding="utf-8")
    print(f"Updated: {src}")


if __name__ == "__main__":
    update_az305()
    update_az104()
