"""Smoke tests for the one-shot migration scripts introduced in issue #213.

These scripts (extract_sections.py, update_cheat_sheets.py) are excluded from
coverage measurement (see pyproject.toml [tool.coverage.run] omit list) because
they are one-time utilities that will not be re-run. These tests document their
expected behaviour on synthetic input and guard against accidental breakage if
the scripts are re-used or adapted in future.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add scripts/ to import path so we can import the migration modules directly.
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import extract_sections  # noqa: E402
import update_cheat_sheets  # noqa: E402

# ---------------------------------------------------------------------------
# extract_sections.fix_diagram_refs
# ---------------------------------------------------------------------------


class TestFixDiagramRefs:
    """fix_diagram_refs rewrites old az104-/az305- diagram paths to exam-agnostic slugs."""

    def test_renames_az305_prefix(self) -> None:
        text = '--8<-- "diagrams/networking/az305-decision-flow.mmd"'
        result = extract_sections.fix_diagram_refs(text)
        assert "networking/decision-flow.mmd" in result
        assert "az305-" not in result

    def test_renames_az104_prefix(self) -> None:
        text = '--8<-- "diagrams/compute/az104-availability-decision-flow.mmd"'
        result = extract_sections.fix_diagram_refs(text)
        assert "compute/availability-decision-flow.mmd" in result
        assert "az104-" not in result

    def test_unknown_path_unchanged(self) -> None:
        text = '--8<-- "diagrams/networking/decision-flow.mmd"'
        result = extract_sections.fix_diagram_refs(text)
        assert result == text

    def test_multiple_refs_in_one_block(self) -> None:
        text = (
            '--8<-- "diagrams/networking/az305-decision-flow.mmd"\n'
            '--8<-- "diagrams/networking/az104-nsg-rule-evaluation.mmd"\n'
        )
        result = extract_sections.fix_diagram_refs(text)
        assert "az305-" not in result
        assert "az104-" not in result
        assert "networking/decision-flow.mmd" in result
        assert "networking/nsg-rule-evaluation.mmd" in result


# ---------------------------------------------------------------------------
# extract_sections.remove_also_relevant_for
# ---------------------------------------------------------------------------


class TestRemoveAlsoRelevantFor:
    """remove_also_relevant_for strips '> Also relevant for:' callout blocks."""

    def test_removes_single_line_callout(self) -> None:
        lines = [
            "# NETWORKING\n",
            "\n",
            "> Also relevant for: **AZ-900**\n",
            "\n",
            "## Load Balancers\n",
        ]
        result = extract_sections.remove_also_relevant_for(lines)
        assert all("> Also relevant for:" not in line for line in result)
        assert any("## Load Balancers" in line for line in result)

    def test_removes_multiline_callout(self) -> None:
        lines = [
            "> Also relevant for: **AZ-900**\n",
            "> and **AZ-104**\n",
            "\n",
            "## Compute\n",
        ]
        result = extract_sections.remove_also_relevant_for(lines)
        assert all("Also relevant for" not in line for line in result)
        assert any("## Compute" in line for line in result)

    def test_no_callout_unchanged(self) -> None:
        lines = [
            "# NETWORKING\n",
            "\n",
            "## Load Balancers\n",
        ]
        result = extract_sections.remove_also_relevant_for(lines)
        assert result == lines


# ---------------------------------------------------------------------------
# update_cheat_sheets.remove_also_relevant_for_lines
# ---------------------------------------------------------------------------


class TestRemoveAlsoRelevantForLines:
    """update_cheat_sheets has its own variant of the callout-removal helper."""

    def test_removes_callout_and_trailing_blank(self) -> None:
        lines = [
            "# SECURITY\n",
            "\n",
            "> Also relevant for: **AZ-500**\n",
            "\n",
            "## Defender\n",
        ]
        result = update_cheat_sheets.remove_also_relevant_for_lines(lines)
        assert all("Also relevant for" not in line for line in result)
        assert any("## Defender" in line for line in result)

    def test_preserves_non_callout_blockquotes(self) -> None:
        lines = [
            "> **Exam tip:** Use RBAC over Access Policies.\n",
            "\n",
        ]
        result = update_cheat_sheets.remove_also_relevant_for_lines(lines)
        assert result == lines

    def test_empty_input(self) -> None:
        assert update_cheat_sheets.remove_also_relevant_for_lines([]) == []
