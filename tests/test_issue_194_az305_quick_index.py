"""Tests for issue #194 - FEATURE: Add AZ-305 Quick Index section to AZ-305_CheatSheet.md."""

from pathlib import Path

CHEAT_SHEET = Path("docs/AZ-305_CheatSheet.md")


def _content():
    return CHEAT_SHEET.read_text(encoding="utf-8")


class TestAZ305QuickIndexExists:
    """Verify ## AZ-305 Quick Index section is present."""

    def test_az305_quick_index_heading_exists(self):
        assert "## AZ-305 Quick Index" in _content(), (
            "Expected '## AZ-305 Quick Index' section in docs/AZ-305_CheatSheet.md"
        )


class TestAZ305QuickIndexPlacement:
    """Verify placement: after ## Exam Track Index, before ## AZ-500 Quick Index, before # NETWORKING."""

    def test_az305_quick_index_before_az500_quick_index(self):
        content = _content()
        pos_305 = content.index("## AZ-305 Quick Index")
        pos_500 = content.index("## AZ-500 Quick Index")
        assert pos_305 < pos_500, (
            "## AZ-305 Quick Index must appear before ## AZ-500 Quick Index"
        )

    def test_az305_quick_index_after_exam_track_index(self):
        content = _content()
        pos_exam = content.index("## Exam Track Index")
        pos_305 = content.index("## AZ-305 Quick Index")
        assert pos_exam < pos_305, (
            "## AZ-305 Quick Index must appear after ## Exam Track Index"
        )

    def test_az305_quick_index_before_networking_heading(self):
        content = _content()
        pos_305 = content.index("## AZ-305 Quick Index")
        pos_net = content.index("\n# NETWORKING")
        assert pos_305 < pos_net, (
            "## AZ-305 Quick Index must appear before # NETWORKING"
        )


class TestAZ305QuickIndexContent:
    """Verify all ten domain rows with correct GitHub anchor links."""

    EXPECTED_ROWS = [
        ("[NETWORKING](#networking)", "Networking"),
        ("[SECURITY](#security)", "Security"),
        ("[STORAGE](#storage)", "Storage"),
        ("[MONITORING & OBSERVABILITY](#monitoring--observability)", "Monitoring & Observability"),
        ("[COMPUTE](#compute)", "Compute"),
        ("[IDENTITY & ACCESS](#identity--access)", "Identity & Access"),
        ("[HIGH AVAILABILITY & DISASTER RECOVERY](#high-availability--disaster-recovery)", "High Availability & Disaster Recovery"),
        ("[GOVERNANCE](#governance)", "Governance"),
        ("[MESSAGING & INTEGRATION](#messaging--integration)", "Messaging & Integration"),
        ("[WELL-ARCHITECTED FRAMEWORK](#well-architected-framework)", "Well-Architected Framework"),
    ]

    def test_all_ten_domain_anchor_links_present(self):
        content = _content()
        for link, domain in self.EXPECTED_ROWS:
            assert link in content, (
                f"Expected anchor link '{link}' for domain '{domain}' in AZ-305 Quick Index"
            )

    def test_table_has_domain_and_section_columns(self):
        content = _content()
        # Find the AZ-305 Quick Index section and check for the column headers
        start = content.index("## AZ-305 Quick Index")
        end = content.index("## AZ-500 Quick Index")
        section = content[start:end]
        assert "| Domain | Section |" in section, (
            "Expected '| Domain | Section |' column headers in ## AZ-305 Quick Index table"
        )


class TestAZ305QuickIndexSeparator:
    """Verify --- separator exists between AZ-305 Quick Index and AZ-500 Quick Index."""

    def test_separator_between_az305_and_az500_quick_index(self):
        content = _content()
        start = content.index("## AZ-305 Quick Index")
        end = content.index("## AZ-500 Quick Index")
        section = content[start:end]
        assert "\n---\n" in section, (
            "Expected '---' separator between ## AZ-305 Quick Index and ## AZ-500 Quick Index"
        )
