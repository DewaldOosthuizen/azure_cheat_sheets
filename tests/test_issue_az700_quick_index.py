"""Tests for issue #164 — FEATURE: Add AZ-700 Quick Index section to AZ-305_CheatSheet.md."""

from pathlib import Path

CHEAT_SHEET = Path("docs/cheat_sheets/AZ-305.md")


def _content():
    return CHEAT_SHEET.read_text(encoding="utf-8")


class TestAZ700QuickIndex:
    """Verify AZ-700 Quick Index section exists."""

    def test_az700_quick_index_section_exists(self):
        assert "## AZ-700 Quick Index" in _content(), (
            "Expected '## AZ-700 Quick Index' section in docs/cheat_sheets/AZ-305.md"
        )


class TestAZ700ExamTips:
    """Verify at least 3 AZ-700 exam tip callouts exist."""

    def test_at_least_three_az700_exam_tips(self):
        count = _content().count("> **Exam tip (AZ-700):**")
        assert count >= 3, (
            f"Expected at least 3 occurrences of '> **Exam tip (AZ-700):**', found {count}"
        )
