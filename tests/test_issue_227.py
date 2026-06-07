"""Regression tests for issue #227.

Verifies that:
  - README.md badge URL uses the current repository slug (tech-cheat-sheets-and-notes)
  - README.md badge anchor href uses the current repository slug
  - mkdocs.yml site_url points to the current Vercel site
  - mkdocs.yml repo_name uses the current repository slug
  - mkdocs.yml repo_url uses the current repository slug
  - None of the stale/old slugs remain in either file
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

README = REPO_ROOT / "README.md"
MKDOCS = REPO_ROOT / "mkdocs.yml"

STALE_REPO_SLUG = "DewaldOosthuizen/azure_cheat_sheets"
STALE_SITE_URL = "https://tech-cheat-sheets.vercel.app/"
STALE_REPO_NAME = "DewaldOosthuizen/tech-cheat-sheets"
STALE_REPO_URL = "https://github.com/DewaldOosthuizen/tech-cheat-sheets"

CORRECT_REPO_SLUG = "DewaldOosthuizen/tech-cheat-sheets-and-notes"
CORRECT_SITE_URL = "https://tech-cheat-sheets-and-notes.vercel.app/"
CORRECT_REPO_URL = "https://github.com/DewaldOosthuizen/tech-cheat-sheets-and-notes"


class TestReadmeBadgeUrl:
    """README.md — CI badge image and anchor href must reference the live repo."""

    def test_badge_image_url_is_current(self):
        content = README.read_text()
        expected = (
            "https://github.com/DewaldOosthuizen/tech-cheat-sheets-and-notes"
            "/actions/workflows/lint.yml/badge.svg"
        )
        assert expected in content, (
            f"README.md badge image URL must contain '{expected}'"
        )

    def test_badge_anchor_href_is_current(self):
        content = README.read_text()
        expected = (
            "https://github.com/DewaldOosthuizen/tech-cheat-sheets-and-notes"
            "/actions/workflows/lint.yml)"
        )
        assert expected in content, (
            f"README.md badge anchor href must contain '{expected}'"
        )

    def test_stale_repo_slug_absent_from_readme(self):
        content = README.read_text()
        assert STALE_REPO_SLUG not in content, (
            f"README.md must not reference stale slug '{STALE_REPO_SLUG}'"
        )


class TestMkdocsUrls:
    """mkdocs.yml — site_url, repo_name, and repo_url must use current names."""

    def test_site_url_is_current(self):
        content = MKDOCS.read_text()
        assert f"site_url: {CORRECT_SITE_URL}" in content, (
            f"mkdocs.yml site_url must be '{CORRECT_SITE_URL}'"
        )

    def test_repo_name_is_current(self):
        content = MKDOCS.read_text()
        assert f"repo_name: {CORRECT_REPO_SLUG}" in content, (
            f"mkdocs.yml repo_name must be '{CORRECT_REPO_SLUG}'"
        )

    def test_repo_url_is_current(self):
        content = MKDOCS.read_text()
        assert f"repo_url: {CORRECT_REPO_URL}" in content, (
            f"mkdocs.yml repo_url must be '{CORRECT_REPO_URL}'"
        )

    def test_stale_site_url_absent(self):
        content = MKDOCS.read_text()
        assert STALE_SITE_URL not in content, (
            f"mkdocs.yml must not contain stale site_url '{STALE_SITE_URL}'"
        )

    def test_stale_repo_name_absent(self):
        # Must check full YAML line — the stale slug is a substring of the correct one.
        content = MKDOCS.read_text()
        stale_line = f"repo_name: {STALE_REPO_NAME}\n"
        assert stale_line not in content, (
            f"mkdocs.yml must not contain stale repo_name line '{stale_line.strip()}'"
        )

    def test_stale_repo_url_absent(self):
        # Must check full YAML line — the stale URL is a substring of the correct one.
        content = MKDOCS.read_text()
        stale_line = f"repo_url: {STALE_REPO_URL}\n"
        assert stale_line not in content, (
            f"mkdocs.yml must not contain stale repo_url line '{stale_line.strip()}'"
        )
