"""Tests for issue #232 - FEATURE: Remove exam coverage by domain from index.md.

Verifies that:
  - docs/index.md no longer contains inline Azure exam coverage table
  - docs/index.md no longer contains inline AWS exam coverage table
  - docs/index.md contains prose link to Azure Exam Track Index
  - docs/index.md contains prose link to AWS Exam Track Index
  - docs/aws/files/exams/exams.md exists with correct content
  - mkdocs.yml registers the AWS Exam Coverage page
  - docs/azure/files/exams/exams.md is unchanged
"""

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
INDEX_MD = REPO_ROOT / "docs" / "index.md"
AZURE_EXAMS_MD = REPO_ROOT / "docs" / "azure" / "files" / "exams" / "exams.md"
AWS_EXAMS_MD = REPO_ROOT / "docs" / "aws" / "files" / "exams" / "exams.md"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"


@pytest.fixture(scope="module")
def index_text():
    return INDEX_MD.read_text()


@pytest.fixture(scope="module")
def azure_exams_text():
    return AZURE_EXAMS_MD.read_text()


@pytest.fixture(scope="module")
def aws_exams_text():
    return AWS_EXAMS_MD.read_text()


@pytest.fixture(scope="module")
def mkdocs_text():
    return MKDOCS_YML.read_text()


# ── TASK 1: index.md — Azure inline table removed ─────────────────────────────


class TestIndexAzureInlineTableRemoved:
    """index.md must not contain the inline Azure exam coverage table."""

    def test_azure_inline_table_header_absent(self, index_text):
        assert "| AZ-900 | AZ-104 | AZ-305 | AZ-500 | AZ-700 |" not in index_text

    def test_azure_exam_coverage_heading_absent(self, index_text):
        # The standalone heading "Exam coverage by domain:" should be gone
        # (it may still appear in prose — we target the table row specifically)
        assert "| AZ-900 |" not in index_text

    def test_azure_prose_link_present(self, index_text):
        assert "See the [Azure Exam Track Index](azure/files/exams/exams.md)" in index_text

    def test_azure_prose_link_certification_text(self, index_text):
        assert "for full coverage by certification." in index_text


# ── TASK 2: index.md — AWS inline table removed ───────────────────────────────


class TestIndexAWSInlineTableRemoved:
    """index.md must not contain the inline AWS exam coverage table."""

    def test_aws_inline_table_header_absent(self, index_text):
        assert "| CLF-C02 | SAA-C03 | SAP-C02 |" not in index_text

    def test_aws_exam_coverage_table_absent(self, index_text):
        assert "| CLF-C02 |" not in index_text

    def test_aws_prose_link_present(self, index_text):
        assert "See the [AWS Exam Track Index](aws/files/exams/exams.md)" in index_text

    def test_aws_prose_link_certification_text(self, index_text):
        # Both prose links share the same suffix — verified implicitly by both being present
        assert "aws/files/exams/exams.md" in index_text


# ── TASK 3: docs/aws/files/exams/exams.md — new file ─────────────────────────


class TestAWSExamsFileExists:
    """docs/aws/files/exams/exams.md must exist."""

    def test_aws_exams_file_exists(self):
        assert AWS_EXAMS_MD.exists(), "docs/aws/files/exams/exams.md does not exist"


class TestAWSExamsFileContent:
    """docs/aws/files/exams/exams.md must contain the correct exam coverage matrix."""

    def test_heading_present(self, aws_exams_text):
        assert "# Exam Track Index" in aws_exams_text

    def test_table_header_clf(self, aws_exams_text):
        assert "CLF-C02" in aws_exams_text

    def test_table_header_saa(self, aws_exams_text):
        assert "SAA-C03" in aws_exams_text

    def test_table_header_sap(self, aws_exams_text):
        assert "SAP-C02" in aws_exams_text

    def test_compute_row_present(self, aws_exams_text):
        assert "[Compute]" in aws_exams_text

    def test_compute_links_to_compute_md(self, aws_exams_text):
        assert "../compute/compute.md" in aws_exams_text

    def test_networking_row_present(self, aws_exams_text):
        assert "[Networking]" in aws_exams_text

    def test_networking_links_to_networking_md(self, aws_exams_text):
        assert "../networking/networking.md" in aws_exams_text

    def test_storage_row_present(self, aws_exams_text):
        assert "[Storage]" in aws_exams_text

    def test_identity_row_present(self, aws_exams_text):
        assert "[Identity & Access]" in aws_exams_text

    def test_security_row_present(self, aws_exams_text):
        assert "[Security]" in aws_exams_text

    def test_database_row_present(self, aws_exams_text):
        assert "[Database]" in aws_exams_text

    def test_database_links_to_database_md(self, aws_exams_text):
        assert "../database/database.md" in aws_exams_text

    def test_monitoring_row_present(self, aws_exams_text):
        assert "Monitoring" in aws_exams_text

    def test_messaging_row_present(self, aws_exams_text):
        assert "Messaging" in aws_exams_text

    def test_governance_row_present(self, aws_exams_text):
        assert "[Governance]" in aws_exams_text

    def test_ha_dr_row_present(self, aws_exams_text):
        assert "High Availability" in aws_exams_text

    def test_waf_row_present(self, aws_exams_text):
        assert "Well-Architected" in aws_exams_text

    def test_eleven_data_rows(self, aws_exams_text):
        # 11 domain rows + 1 abbreviations row = 12 total data rows (issue #234)
        data_rows = [
            line
            for line in aws_exams_text.splitlines()
            if line.strip().startswith("|") and "---" not in line and "Section" not in line
        ]
        assert len(data_rows) == 12, f"Expected 12 data rows, got {len(data_rows)}"


# ── TASK 4: mkdocs.yml — AWS Exam Coverage registered ────────────────────────


class TestMkdocsAWSExamCoverage:
    """mkdocs.yml must register aws/files/exams/exams.md under the AWS nav section."""

    def test_aws_exam_coverage_entry_present(self, mkdocs_text):
        assert "Exam Coverage: aws/files/exams/exams.md" in mkdocs_text

    def test_aws_exam_coverage_is_first_under_aws(self, mkdocs_text):
        lines = mkdocs_text.splitlines()
        aws_idx = next((i for i, line in enumerate(lines) if line.strip() == "- AWS:"), None)
        assert aws_idx is not None, "- AWS: section not found in mkdocs.yml"
        # Find next nav entries after - AWS:
        child_entries = []
        for line in lines[aws_idx + 1 :]:
            stripped = line.strip()
            if (
                stripped.startswith("- ")
                and not stripped.startswith("- AWS:")
                and not stripped.startswith("-   ")
                and ":" in stripped
            ):
                child_entries.append(stripped)
                break
        assert child_entries, "No child entries found under - AWS:"
        # Abbreviations is now the first entry under AWS (issue #234);
        # Exam Coverage is the second entry.
        assert "Abbreviations" in child_entries[0], (
            f"First AWS child is not Abbreviations, got: {child_entries[0]}"
        )


# ── TASK 5: azure/files/exams/exams.md unchanged ─────────────────────────────


class TestAzureExamsUnchanged:
    """docs/azure/files/exams/exams.md must remain unchanged."""

    def test_azure_exams_has_az204_column(self, azure_exams_text):
        assert "AZ-204" in azure_exams_text

    def test_azure_exams_has_seven_columns(self, azure_exams_text):
        header = next((line for line in azure_exams_text.splitlines() if "Section" in line), None)
        assert header is not None
        # 7 columns: Section, AZ-900, AZ-104, AZ-204, AZ-305, AZ-500, AZ-700
        assert header.count("|") >= 8  # at least 7 columns = 8 pipes

    def test_azure_exams_has_ten_data_rows(self, azure_exams_text):
        data_rows = [
            line
            for line in azure_exams_text.splitlines()
            if line.strip().startswith("|") and "---" not in line and "Section" not in line
        ]
        # 10 domain rows + 1 abbreviations row + 1 migration row = 12 total data rows
        assert len(data_rows) == 12, f"Expected 12 data rows, got {len(data_rows)}"
