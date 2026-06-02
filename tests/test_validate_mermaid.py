"""Tests for issue #42 - error handling and exit-code reporting in validate_mermaid.py."""
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, "scripts")
import validate_mermaid


class TestMmdcNotFound:
    """Tests for shutil.which guard in main()."""

    def test_main_exits_with_code_2_when_mmdc_missing(self):
        with (
            patch("validate_mermaid.shutil.which", return_value=None),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code == 2

    def test_main_prints_error_to_stderr_when_mmdc_missing(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value=None),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "mmdc not found" in captured.err
        assert "npm install -g @mermaid-js/mermaid-cli" in captured.err


class TestValidateBlockFileNotFound:
    """Tests for FileNotFoundError handling in validate_block()."""

    def test_validate_block_returns_false_when_mmdc_not_on_path(self):
        with patch("validate_mermaid.subprocess.run", side_effect=FileNotFoundError):
            result = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert result[0] is False
        assert result[1] == "mmdc binary not found on PATH"


class TestValidateBlockTimeout:
    """Tests for subprocess.TimeoutExpired handling in validate_block()."""

    def test_validate_block_returns_false_on_timeout(self):
        import subprocess
        with patch("validate_mermaid.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="mmdc", timeout=60)):
            result = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert result[0] is False
        assert result[1] == "mmdc timed out after 60 s"


class TestMainFileNotFound:
    """Tests for os.path.isfile guard in main()."""

    def test_main_exits_with_code_1_when_file_missing(self):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", ["validate_mermaid.py", "/nonexistent/path.md"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code == 1

    def test_main_prints_error_to_stderr_when_file_missing(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", ["validate_mermaid.py", "/nonexistent/path.md"]),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "file not found" in captured.err
        assert "/nonexistent/path.md" in captured.err
