"""Tests for issue #42, #62, and #120 - validate_mermaid.py."""

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
            patch(
                "validate_mermaid.sys.argv",
                ["validate_mermaid.py", "/nonexistent/path.md"],
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code == 1

    def test_main_prints_error_to_stderr_when_file_missing(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch(
                "validate_mermaid.sys.argv",
                ["validate_mermaid.py", "/nonexistent/path.md"],
            ),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "file not found" in captured.err
        assert "/nonexistent/path.md" in captured.err


class TestExtractMermaidBlocks:
    """Parametrised tests for _extract_from_text() helper."""

    @pytest.mark.parametrize(
        "text,expected_count,expected_content",
        [
            # single_block
            ("```mermaid\ngraph TD\n  A --> B\n```", 1, "graph TD\n  A --> B\n"),
            # multiple_blocks
            (
                "```mermaid\ngraph TD\n  A-->B\n```\n\n```mermaid\ngraph LR\n  C-->D\n```",
                2,
                None,
            ),
            # no_blocks
            ("# Heading\nSome text.", 0, None),
            # non_mermaid_fence
            ("```python\nprint('hi')\n```", 0, None),
            # trailing_whitespace_fence
            ("```mermaid   \ngraph TD\n  A-->B\n```", 1, None),
            # crlf_line_endings
            ("```mermaid\r\ngraph TD\r\n  A-->B\r\n```", 1, None),
        ],
    )
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
            node
            for node in ast.walk(tree)
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


_DUMMY_ARGV = ["validate_mermaid.py", "docs/AZ-305_CheatSheet.md"]
_ONE_BLOCK = ["graph TD\n  A --> B\n"]


class TestExtractMermaidBlocksFromFile:
    """Tests for extract_mermaid_blocks() reading from a real file."""

    def test_extract_reads_file_and_returns_blocks(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("```mermaid\ngraph TD\n  A --> B\n```\n", encoding="utf-8")
        result = validate_mermaid.extract_mermaid_blocks(str(md))
        assert len(result) == 1
        assert "graph TD" in result[0]


class TestValidateBlockPuppeteerConfig:
    """Tests for puppeteer config branch in validate_block()."""

    def test_validate_block_appends_puppeteer_config_when_present(self):
        import subprocess

        success_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with (
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
            patch("validate_mermaid.subprocess.run", return_value=success_result) as mock_run,
        ):
            mock_cfg.exists.return_value = True
            mock_cfg.__str__ = lambda s: "/tmp/puppeteer-config.json"
            ok, _ = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert ok is True
        call_args = mock_run.call_args[0][0]
        assert "--puppeteerConfigFile" in call_args

    def test_validate_block_returns_true_on_success(self):
        import subprocess

        success_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with (
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
            patch("validate_mermaid.subprocess.run", return_value=success_result),
        ):
            mock_cfg.exists.return_value = False
            ok, stderr = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert ok is True
        assert stderr == ""


class TestMainNoArgv:
    """main() exits non-zero with usage message when no markdown argument is given.

    After the argparse refactor (issue #120), argparse handles missing required
    positional args and prints usage to stderr, exiting with code 2.
    """

    def test_main_exits_nonzero_when_no_argv(self):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", ["validate_mermaid.py"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code != 0

    def test_main_prints_usage_to_stderr_when_no_argv(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", ["validate_mermaid.py"]),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        # argparse writes usage/error to stderr
        assert "usage" in captured.err.lower() or "error" in captured.err.lower()


class TestMainHappyPath:
    """main() exits 0 (no SystemExit) when all diagrams pass."""

    def test_main_does_not_raise_when_all_diagrams_pass(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", _DUMMY_ARGV),
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
        ):
            validate_mermaid.main()  # must not raise
        captured = capsys.readouterr()
        assert "passed" in captured.out.lower()


class TestMainAggregateFail:
    """main() exits 1 when one or more diagrams fail."""

    def test_main_exits_1_when_diagram_fails(self):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", _DUMMY_ARGV),
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(False, "syntax error")),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code == 1

    def test_main_prints_failure_summary(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", _DUMMY_ARGV),
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(False, "syntax error")),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "issue" in captured.out.lower() or "fail" in captured.out.lower()


class TestMainZeroBlocks:
    """main() exits non-zero with a stderr warning when no mermaid blocks are found."""

    def test_main_exits_nonzero_when_no_blocks_found(self):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", _DUMMY_ARGV),
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code != 0

    def test_main_prints_warning_to_stderr_when_no_blocks_found(self, capsys):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.sys.argv", _DUMMY_ARGV),
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "no mermaid blocks found" in captured.err


# ---- issue #120: multi-file support ----


class TestMultiFileHappyPath:
    """main() accepts multiple files and exits 0 when all pass."""

    def test_main_passes_two_valid_files(self, tmp_path, capsys):
        md1 = tmp_path / "a.md"
        md2 = tmp_path / "b.md"
        md1.write_text("```mermaid\ngraph TD\n  A --> B\n```\n", encoding="utf-8")
        md2.write_text("```mermaid\ngraph LR\n  C --> D\n```\n", encoding="utf-8")
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch(
                "validate_mermaid.sys.argv",
                ["validate_mermaid.py", str(md1), str(md2)],
            ),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
            patch(
                "validate_mermaid.Path.__new__",
                side_effect=lambda cls, *a, **kw: object.__new__(cls),
            ),
        ):
            # Patch repo_root resolution so tmp_path is treated as repo root
            with patch.object(
                validate_mermaid.Path(__file__).parent.parent.__class__,
                "resolve",
                return_value=tmp_path,
            ):
                validate_mermaid.main()  # must not raise
        captured = capsys.readouterr()
        assert "passed" in captured.out.lower()


class TestMultiFileOneBad:
    """main() exits 1 and reports the bad file when one of many files fails."""

    def test_main_exits_1_with_one_invalid_file(self, tmp_path):
        md_good = tmp_path / "good.md"
        md_good.write_text("```mermaid\ngraph TD\n  A --> B\n```\n", encoding="utf-8")
        bad_path = str(tmp_path / "missing.md")
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch(
                "validate_mermaid.sys.argv",
                ["validate_mermaid.py", str(md_good), bad_path],
            ),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.main()
        assert exc_info.value.code == 1

    def test_main_reports_bad_file_in_stderr(self, tmp_path, capsys):
        md_good = tmp_path / "good.md"
        md_good.write_text("```mermaid\ngraph TD\n  A --> B\n```\n", encoding="utf-8")
        bad_path = str(tmp_path / "missing.md")
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch(
                "validate_mermaid.sys.argv",
                ["validate_mermaid.py", str(md_good), bad_path],
            ),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
            pytest.raises(SystemExit),
        ):
            validate_mermaid.main()
        captured = capsys.readouterr()
        assert "missing.md" in captured.err
