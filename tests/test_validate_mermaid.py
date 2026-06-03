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
        timeout_exc = subprocess.TimeoutExpired(cmd="mmdc", timeout=60)
        with patch("validate_mermaid.subprocess.run", side_effect=timeout_exc):
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


class TestExtractMermaidBlocks:
    """Parametrised tests for _extract_from_text() helper."""

    @pytest.mark.parametrize("text,expected_count,expected_content", [
        # single_block
        ("```mermaid\ngraph TD\n  A --> B\n```", 1, "graph TD\n  A --> B\n"),
        # multiple_blocks
        ("```mermaid\ngraph TD\n  A-->B\n```\n\n```mermaid\ngraph LR\n  C-->D\n```", 2, None),
        # no_blocks
        ("# Heading\nSome text.", 0, None),
        # non_mermaid_fence
        ("```python\nprint('hi')\n```", 0, None),
        # trailing_whitespace_fence
        ("```mermaid   \ngraph TD\n  A-->B\n```", 1, None),
        # crlf_line_endings
        ("```mermaid\r\ngraph TD\r\n  A-->B\r\n```", 1, None),
    ])
    def test_extract(self, text, expected_count, expected_content):
        result = validate_mermaid._extract_from_text(text)
        assert len(result) == expected_count
        if expected_content is not None:
            assert result[0] == expected_content


class TestPathlibRefactor:
    """Tests for issue #62 — pathlib usage in validate_block() and main()."""

    def test_validate_block_unlinks_tmp_via_pathlib(self):
        """Cleanup must use Path.unlink, not os.unlink."""
        import inspect

        import validate_mermaid as vm
        src = inspect.getsource(vm.validate_block)
        assert "os.unlink" not in src, "validate_block must not use os.unlink"
        assert "os.path.exists" not in src, "validate_block must not use os.path.exists"
        assert "unlink(missing_ok=True)" in src

    def test_main_uses_pathlib_is_file(self):
        """main() must check the markdown file via Path.is_file(), not os.path.isfile()."""
        import inspect

        import validate_mermaid as vm
        src = inspect.getsource(vm.main)
        assert "os.path.isfile" not in src, "main() must not use os.path.isfile"
        assert ".is_file()" in src

    def test_import_os_removed(self):
        """The script must not import os after the refactor."""
        import ast
        import inspect

        import validate_mermaid as vm
        source = inspect.getsource(vm)
        tree = ast.parse(source)
        os_imports = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            and any(
                (alias.name == "os" if isinstance(node, ast.Import) else node.module == "os")
                for alias in node.names
            )
        ]
        assert not os_imports, "import os must be removed after pathlib refactor"

    def test_out_path_derived_with_suffix(self):
        """SVG path must be derived with Path.with_suffix, not string.replace."""
        import inspect

        import validate_mermaid as vm
        src = inspect.getsource(vm.validate_block)
        assert '.replace(".mmd"' not in src, "must not use string.replace for suffix"
        assert "with_suffix" in src
