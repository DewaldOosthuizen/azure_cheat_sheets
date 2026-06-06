"""Tests for issue #134 - FEATURE: Expand cheat sheet with AZ-500 Security Engineer content."""

from pathlib import Path

from conftest import expand_snippets

CHEAT_SHEET = Path("docs/cheat_sheets/AZ-305.md")


def _content():
    return expand_snippets(CHEAT_SHEET.read_text(encoding="utf-8"))


class TestAZ500QuickIndex:
    """Verify AZ-500 Quick Index section exists."""

    def test_az500_quick_index_section_exists(self):
        assert "## AZ-500 Quick Index" in _content(), (
            "Expected '## AZ-500 Quick Index' section in docs/cheat_sheets/AZ-305.md"
        )


class TestAZ500ExamTips:
    """Verify at least 5 AZ-500 exam tip callouts exist."""

    def test_at_least_five_az500_exam_tips(self):
        count = _content().count("> **Exam tip (AZ-500):**")
        assert count >= 5, (
            f"Expected at least 5 occurrences of '> **Exam tip (AZ-500):**', found {count}"
        )
