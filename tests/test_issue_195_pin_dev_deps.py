"""
Tests for issue #195: Pin Python dev dependency versions in pyproject.toml.

Verifies that:
  - pyproject.toml carries upper-bound caps on all three dev dependencies
  - .github/workflows/lint.yml python-lint job installs via editable install
  - .github/workflows/lint.yml python-test job installs via editable install
  - CONTRIBUTING.md Section 5 directs contributors to pip install -e '.[dev]'
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"
LINT_YML = REPO_ROOT / ".github" / "workflows" / "lint.yml"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"


class TestPyprojectUpperBounds:
    """pyproject.toml dev deps must carry upper-bound caps."""

    def test_pytest_has_upper_bound(self):
        content = PYPROJECT.read_text()
        assert "pytest>=9.0.3,<10" in content, "pytest constraint must include upper bound <10"

    def test_pytest_cov_has_upper_bound(self):
        content = PYPROJECT.read_text()
        assert "pytest-cov>=7.1.0,<8" in content, (
            "pytest-cov constraint must include upper bound <8"
        )

    def test_ruff_has_upper_bound(self):
        content = PYPROJECT.read_text()
        assert "ruff>=0.15.15,<1" in content, "ruff constraint must include upper bound <1"

    def test_no_open_ended_pytest(self):
        content = PYPROJECT.read_text()
        # Line like '"pytest>=9.0.3",' with no upper bound must not exist
        assert not re.search(r'"pytest>=[\d.]+",', content), (
            "pytest must not appear with open-ended lower bound only"
        )

    def test_no_open_ended_pytest_cov(self):
        content = PYPROJECT.read_text()
        assert not re.search(r'"pytest-cov>=[\d.]+",', content), (
            "pytest-cov must not appear with open-ended lower bound only"
        )

    def test_no_open_ended_ruff(self):
        content = PYPROJECT.read_text()
        assert not re.search(r'"ruff>=[\d.]+",', content), (
            "ruff must not appear with open-ended lower bound only"
        )


class TestCIPythonLintJob:
    """.github/workflows/lint.yml python-lint job must use editable install."""

    def test_python_lint_uses_editable_install(self):
        content = LINT_YML.read_text()
        assert "pip install -e '.[dev]'" in content, (
            "python-lint job must install via pip install -e '.[dev]'"
        )

    def test_python_lint_no_inline_ruff_install(self):
        content = LINT_YML.read_text()
        assert 'pip install "ruff>=' not in content, (
            "python-lint job must not contain an inline ruff version pin"
        )


class TestCIPythonTestJob:
    """.github/workflows/lint.yml python-test job must use editable install."""

    def test_python_test_uses_editable_install(self):
        content = LINT_YML.read_text()
        assert "pip install -e '.[dev]'" in content, (
            "python-test job must install via pip install -e '.[dev]'"
        )

    def test_python_test_no_bare_pip_install(self):
        content = LINT_YML.read_text()
        assert "pip install pytest pytest-cov" not in content, (
            "python-test job must not use bare unconstrained pip install"
        )


class TestContributingDevSetup:
    """CONTRIBUTING.md Section 5 must point to the editable install."""

    def test_editable_install_present(self):
        content = CONTRIBUTING.read_text()
        assert "pip install -e '.[dev]'" in content, (
            "CONTRIBUTING.md must document pip install -e '.[dev]' for dev setup"
        )

    def test_bare_pip_install_removed(self):
        content = CONTRIBUTING.read_text()
        assert "pip install ruff pytest" not in content, (
            "CONTRIBUTING.md must not instruct bare 'pip install ruff pytest'"
        )
