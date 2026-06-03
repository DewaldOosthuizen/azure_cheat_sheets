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
    """Tests for file-existence guard in run()."""

    def test_run_returns_1_when_file_missing(self):
        result = validate_mermaid.run(["/nonexistent/path.md"])
        assert result == 1

    def test_run_prints_error_to_stderr_when_file_missing(self, capsys):
        validate_mermaid.run(["/nonexistent/path.md"])
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
            ("```mermaid\ngraph TD\n  A-->B\n```\n\n```mermaid\ngraph LR\n  C-->D\n```", 2, None),
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
    """Tests for issue #62 — pathlib usage in validate_block() and run()."""

    def test_validate_block_unlinks_tmp_via_pathlib(self):
        """Cleanup must use Path.unlink, not os.unlink."""
        import inspect

        import validate_mermaid as vm

        src = inspect.getsource(vm.validate_block)
        assert "os.unlink" not in src, "validate_block must not use os.unlink"
        assert "os.path.exists" not in src, "validate_block must not use os.path.exists"
        assert "unlink(missing_ok=True)" in src

    def test_main_uses_pathlib_is_file(self):
        """run() must check the markdown file via Path.is_file(), not os.path.isfile()."""
        import inspect

        import validate_mermaid as vm

        src = inspect.getsource(vm.run)
        assert "os.path.isfile" not in src, "run() must not use os.path.isfile"
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


class TestParseArgs:
    """Tests for parse_args() in isolation — covers CLI argument parsing."""

    def test_parse_args_returns_namespace_with_md_files(self):
        argv = ["validate_mermaid.py", "docs/AZ-305_CheatSheet.md"]
        with patch("validate_mermaid.sys.argv", argv):
            args = validate_mermaid.parse_args()
        assert args.md_files == ["docs/AZ-305_CheatSheet.md"]

    def test_parse_args_exits_2_when_no_positional_argument(self):
        with (
            patch("validate_mermaid.sys.argv", ["validate_mermaid.py"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            validate_mermaid.parse_args()
        assert exc_info.value.code == 2


class TestMainHappyPath:
    """run() returns 0 when all diagrams pass."""

    def test_run_returns_0_when_all_diagrams_pass(self, capsys):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["docs/AZ-305_CheatSheet.md"])
        assert result == 0
        captured = capsys.readouterr()
        assert "All 1 diagram(s) passed" in captured.out


class TestMainAggregateFail:
    """run() returns 1 when one or more diagrams fail."""

    def test_run_returns_1_when_diagram_fails(self):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(False, "syntax error")),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["docs/AZ-305_CheatSheet.md"])
        assert result == 1

    def test_run_prints_failure_summary(self, capsys):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(False, "syntax error")),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            validate_mermaid.run(["docs/AZ-305_CheatSheet.md"])
        captured = capsys.readouterr()
        assert "1 diagram(s) failed" in captured.out


class TestMainZeroBlocks:
    """run() returns 2 with a stderr warning when no mermaid blocks are found."""

    def test_run_returns_2_when_no_blocks_found(self):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["docs/AZ-305_CheatSheet.md"])
        assert result == 2

    def test_run_prints_warning_to_stderr_when_no_blocks_found(self, capsys):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            validate_mermaid.run(["docs/AZ-305_CheatSheet.md"])
        captured = capsys.readouterr()
        assert "no mermaid blocks found" in captured.err


class TestTraversalGuard:
    """Tests for issue #126 - path traversal / shell-injection guard in run()."""

    def test_run_returns_1_on_path_traversal(self, capsys):
        """Path resolving outside repo root must be rejected with return code 1."""
        from pathlib import Path

        original_resolve = Path.resolve

        def fake_resolve(self, strict=False):
            if str(self) == "/etc/passwd":
                return Path("/etc/passwd")
            return original_resolve(self, strict=strict)

        with (
            patch.object(Path, "is_file", return_value=True),
            patch.object(Path, "resolve", fake_resolve),
            patch("validate_mermaid._repo_root", return_value=Path("/tmp/fake-repo-root")),
        ):
            result = validate_mermaid.run(["/etc/passwd"])
        assert result == 1
        captured = capsys.readouterr()
        assert "outside repository root" in captured.err

    def test_run_returns_0_for_valid_path(self, capsys):
        """A path within the repo root must pass the traversal guard."""
        from pathlib import Path

        import scripts.validate_mermaid as vm_mod

        repo_root = Path(vm_mod.__file__).parent.parent.resolve()
        valid_path = str(repo_root / "docs" / "AZ-305_CheatSheet.md")

        with (
            patch.object(Path, "is_file", return_value=True),
            patch(
                "validate_mermaid.extract_mermaid_blocks",
                return_value=["graph TD\n  A --> B\n"],
            ),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
        ):
            result = validate_mermaid.run([valid_path])
        assert result == 0
        captured = capsys.readouterr()
        assert "outside repository root" not in captured.err


class TestRealCheatSheet:
    """Integration tests that read docs/AZ-305_CheatSheet.md from disk."""

    def test_extracts_nonzero_blocks_from_real_cheat_sheet(self):
        blocks = validate_mermaid.extract_mermaid_blocks("docs/AZ-305_CheatSheet.md")
        assert len(blocks) > 0, "Expected at least one Mermaid block in the cheat sheet"

    def test_all_blocks_are_non_empty_strings(self):
        blocks = validate_mermaid.extract_mermaid_blocks("docs/AZ-305_CheatSheet.md")
        for i, b in enumerate(blocks):
            assert isinstance(b, str) and b.strip(), f"Block {i + 1} is empty or not a string"
