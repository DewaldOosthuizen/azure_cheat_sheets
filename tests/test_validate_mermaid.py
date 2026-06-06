"""Tests for issue #42 - error handling and exit-code reporting in validate_mermaid.py."""

import shutil
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
            # mermaid_followed_by_other_language_fence — regex must not bleed across fences
            (
                "```mermaid\ngraph TD\n  A-->B\n```\n\n```python\nprint('hi')\n```",
                1,
                "graph TD\n  A-->B\n",
            ),
            # python_block_with_backtick_string_precedes_mermaid — greedy matching must not
            # capture the Python block as part of the diagram
            (
                '```python\nx = "```"\n```\n\n```mermaid\ngraph TD\n  A-->B\n```',
                1,
                "graph TD\n  A-->B\n",
            ),
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

    def test_import_os_present(self):
        """The script must import os (needed for os.environ.get in PUPPETEER_CONFIG)."""
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
        assert os_imports, "import os must be present for env-var-driven PUPPETEER_CONFIG"

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


class TestExtractMermaidBlocksFileErrors:
    """Tests for extract_mermaid_blocks() file-read error paths."""

    def test_raises_on_permission_error(self, tmp_path):
        md = tmp_path / "locked.md"
        md.write_text("```mermaid\ngraph TD\n  A-->B\n```", encoding="utf-8")
        md.chmod(0o000)
        with pytest.raises(RuntimeError) as excinfo:
            validate_mermaid.extract_mermaid_blocks(str(md))
        md.chmod(0o644)  # restore so pytest can clean up tmp_path
        assert str(md) in str(excinfo.value)

    def test_raises_on_encoding_error(self, tmp_path):
        md = tmp_path / "binary.md"
        md.write_bytes(b"\xff\xfe invalid utf-8")
        with pytest.raises(RuntimeError) as excinfo:
            validate_mermaid.extract_mermaid_blocks(str(md))
        assert str(md) in str(excinfo.value)


class TestRunFileReadErrors:
    """Tests for run() handling RuntimeError raised by extract_mermaid_blocks."""

    def test_run_returns_1_on_runtime_error(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("# test", encoding="utf-8")
        error_msg = f"Cannot read {md}: permission denied"
        with (
            patch("validate_mermaid.Path.is_file", return_value=True),
            patch("validate_mermaid._repo_root", return_value=tmp_path),
            patch(
                "validate_mermaid.extract_mermaid_blocks",
                side_effect=RuntimeError(error_msg),
            ),
        ):
            result = validate_mermaid.run([str(md)])
        assert result == 1

    def test_run_prints_error_to_stderr_on_runtime_error(self, tmp_path, capsys):
        md = tmp_path / "test.md"
        md.write_text("# test", encoding="utf-8")
        error_msg = f"Cannot read {md}: permission denied"
        with (
            patch("validate_mermaid.Path.is_file", return_value=True),
            patch("validate_mermaid._repo_root", return_value=tmp_path),
            patch(
                "validate_mermaid.extract_mermaid_blocks",
                side_effect=RuntimeError(error_msg),
            ),
        ):
            validate_mermaid.run([str(md)])
        captured = capsys.readouterr()
        assert error_msg in captured.err


class TestValidateBlockPuppeteerConfig:
    """Tests for puppeteer config branch in validate_block()."""

    def test_validate_block_appends_puppeteer_config_when_present(self):
        import subprocess

        def _write_svg_and_succeed(cmd, **kwargs):
            input_flag = cmd.index("--input")
            from pathlib import Path as _Path

            out_file = _Path(cmd[input_flag + 1]).with_suffix(".svg")
            out_file.write_bytes(b"<svg>" + b"x" * 200 + b"</svg>")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        with (
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
            patch(
                "validate_mermaid.subprocess.run",
                side_effect=_write_svg_and_succeed,
            ) as mock_run,
        ):
            mock_cfg.exists.return_value = True
            mock_cfg.__str__ = lambda s: "/tmp/puppeteer-config.json"
            ok, _ = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert ok is True
        call_args = mock_run.call_args[0][0]
        assert "--puppeteerConfigFile" in call_args

    def test_validate_block_returns_true_on_success(self):
        import subprocess

        def _write_svg_and_succeed(cmd, **kwargs):
            input_flag = cmd.index("--input")
            from pathlib import Path as _Path

            out_file = _Path(cmd[input_flag + 1]).with_suffix(".svg")
            out_file.write_bytes(b"<svg>" + b"x" * 200 + b"</svg>")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        with (
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
            patch("validate_mermaid.subprocess.run", side_effect=_write_svg_and_succeed),
        ):
            mock_cfg.exists.return_value = False
            ok, stderr = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert ok is True
        assert stderr == ""


class TestParseArgs:
    """Tests for parse_args() in isolation — covers CLI argument parsing."""

    def test_parse_args_returns_namespace_with_md_files(self):
        argv = ["validate_mermaid.py", "docs/cheat_sheets/AZ-305.md"]
        with patch("validate_mermaid.sys.argv", argv):
            args = validate_mermaid.parse_args()
        assert args.md_files == ["docs/cheat_sheets/AZ-305.md"]

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
            result = validate_mermaid.run(["docs/cheat_sheets/AZ-305.md"])
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
            result = validate_mermaid.run(["docs/cheat_sheets/AZ-305.md"])
        assert result == 1

    def test_run_prints_failure_summary(self, capsys):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=_ONE_BLOCK),
            patch("validate_mermaid.validate_block", return_value=(False, "syntax error")),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            validate_mermaid.run(["docs/cheat_sheets/AZ-305.md"])
        captured = capsys.readouterr()
        assert "1 diagram(s) failed" in captured.out


class TestMainZeroBlocks:
    """run() skips files with no mermaid blocks (returns 0) but prints a stderr warning."""

    def test_run_returns_0_when_no_blocks_found(self):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["docs/cheat_sheets/AZ-305.md"])
        assert result == 0

    def test_run_prints_warning_to_stderr_when_no_blocks_found(self, capsys):
        with (
            patch("validate_mermaid.extract_mermaid_blocks", return_value=[]),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            validate_mermaid.run(["docs/cheat_sheets/AZ-305.md"])
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

    def test_run_rejects_path_with_matching_prefix_but_outside_root(self, capsys):
        """A path whose string representation shares a prefix with repo_root but
        resolves to a *different* directory must be rejected.

        Example: root=/tmp/fake-repo-root, path=/tmp/fake-repo-root-extra/file.md
        A naive startswith check would pass because the path string starts with
        the root string.  Path.is_relative_to() correctly rejects it.
        """
        from pathlib import Path
        import tempfile, os

        with tempfile.TemporaryDirectory() as tmp:
            # Create two sibling directories whose names share a prefix.
            repo_root = Path(tmp) / "fake-repo-root"
            sibling   = Path(tmp) / "fake-repo-root-extra"
            repo_root.mkdir()
            sibling.mkdir()
            outside_file = sibling / "file.md"
            outside_file.write_text("# test", encoding="utf-8")

            with patch("validate_mermaid._repo_root", return_value=repo_root):
                result = validate_mermaid.run([str(outside_file)])

        assert result == 1
        captured = capsys.readouterr()
        assert "outside repository root" in captured.err

    def test_run_returns_0_for_valid_path(self, capsys):
        """A path within the repo root must pass the traversal guard."""
        from pathlib import Path

        import scripts.validate_mermaid as vm_mod

        repo_root = Path(vm_mod.__file__).parent.parent.resolve()
        valid_path = str(repo_root / "docs" / "cheat_sheets/AZ-305.md")

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


class TestValidateBlockDegenerateSvg:
    """Tests for degenerate (empty/missing) SVG guard in validate_block()."""

    def test_validate_block_returns_false_on_degenerate_svg(self, tmp_path):
        import subprocess

        def _write_empty_svg_and_succeed(cmd, **kwargs):
            # Derive out_path the same way validate_block does
            input_flag = cmd.index("--input")
            tmp_file = cmd[input_flag + 1]
            out_file = str(tmp_file).replace(".mmd", ".svg")
            from pathlib import Path as _Path

            _Path(out_file).write_bytes(b"")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        with (
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
            patch("validate_mermaid.subprocess.run", side_effect=_write_empty_svg_and_succeed),
        ):
            mock_cfg.exists.return_value = False
            ok, msg = validate_mermaid.validate_block(1, "graph TD\n  A --> B\n")
        assert ok is False
        assert msg == "mmdc produced an empty/degenerate SVG (possible silent render failure)"


class TestRealCheatSheet:
    """Integration tests that read docs/cheat_sheets/AZ-305.md from disk."""

    def test_extracts_nonzero_blocks_from_real_cheat_sheet(self):
        blocks = validate_mermaid.extract_mermaid_blocks("docs/cheat_sheets/AZ-305.md")
        assert len(blocks) > 0, "Expected at least one Mermaid block in the cheat sheet"

    def test_all_blocks_are_non_empty_strings(self):
        blocks = validate_mermaid.extract_mermaid_blocks("docs/cheat_sheets/AZ-305.md")
        for i, b in enumerate(blocks):
            assert isinstance(b, str) and b.strip(), f"Block {i + 1} is empty or not a string"


@pytest.mark.skipif(shutil.which("mmdc") is None, reason="mmdc not installed")
class TestRealCheatSheetIntegration:
    """Integration tests that invoke validate_block against the real cheat sheet."""

    def test_all_diagrams_pass(self):
        blocks = validate_mermaid.extract_mermaid_blocks("docs/cheat_sheets/AZ-305.md")
        assert len(blocks) > 0, "Expected at least one Mermaid block in the cheat sheet"
        for i, block in enumerate(blocks):
            ok, err = validate_mermaid.validate_block(i, block)
            assert ok, f"Diagram {i + 1} failed: {err}"


class TestMainMultiFile:
    """Tests for run() when called with more than one Markdown file."""

    def test_run_validates_second_file_when_first_has_no_blocks(self, capsys):
        with (
            patch(
                "validate_mermaid.extract_mermaid_blocks",
                side_effect=[[], ["graph TD\n  A --> B\n"]],
            ),
            patch("validate_mermaid.validate_block", return_value=(True, "")),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["empty.md", "docs/cheat_sheets/AZ-305.md"])
        assert result == 0

    def test_run_returns_1_when_second_file_has_failing_diagram(self):
        with (
            patch(
                "validate_mermaid.extract_mermaid_blocks",
                side_effect=[
                    ["graph TD\n  A --> B\n"],
                    ["graph TD\n  A --> B\n"],
                ],
            ),
            patch(
                "validate_mermaid.validate_block",
                side_effect=[(True, ""), (False, "syntax error")],
            ),
            patch("validate_mermaid.Path.is_file", return_value=True),
        ):
            result = validate_mermaid.run(["file1.md", "file2.md"])
        assert result == 1


class TestExpandSnippetErrors:
    """Tests for _expand_snippet() OSError/UnicodeDecodeError → RuntimeError path (lines 82-83)."""

    def test_expand_snippet_raises_on_missing_file(self, tmp_path):
        block = '--8<-- "diagrams/missing.mmd"'
        with pytest.raises(RuntimeError, match="Cannot read snippet file"):
            validate_mermaid._expand_snippet(block, tmp_path)

    def test_expand_snippet_raises_on_permission_error(self, tmp_path):
        mmd = tmp_path / "diagrams" / "locked.mmd"
        mmd.parent.mkdir(parents=True)
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        mmd.chmod(0o000)
        block = '--8<-- "diagrams/locked.mmd"'
        try:
            with pytest.raises(RuntimeError, match="Cannot read snippet file"):
                validate_mermaid._expand_snippet(block, tmp_path)
        finally:
            mmd.chmod(0o644)

    def test_expand_snippet_returns_none_for_non_directive(self, tmp_path):
        result = validate_mermaid._expand_snippet("graph TD\n  A --> B\n", tmp_path)
        assert result is None


class TestExtractMermaidBlocksExpandSnippetsFalse:
    """Tests for extract_mermaid_blocks(expand_snippets=False) early-return path (lines 113-114)."""

    def test_returns_raw_blocks_without_expansion(self, tmp_path):
        md = tmp_path / "test.md"
        directive = '--8<-- "diagrams/networking/foo.mmd"'
        md.write_text(f"```mermaid\n{directive}\n```\n", encoding="utf-8")
        blocks = validate_mermaid.extract_mermaid_blocks(str(md), expand_snippets=False)
        assert len(blocks) == 1
        assert directive in blocks[0]


class TestExtractMermaidBlocksSnippetRuntimeError:
    """Tests for RuntimeError re-raise in extract_mermaid_blocks (lines 123-124)."""

    def test_reraises_runtime_error_from_snippet(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text('```mermaid\n--8<-- "diagrams/missing.mmd"\n```\n', encoding="utf-8")
        with pytest.raises(RuntimeError, match="Cannot read snippet file"):
            validate_mermaid.extract_mermaid_blocks(str(md), snippet_base=tmp_path)


class TestExtractMermaidBlocksCustomSnippetBase:
    """Tests for the snippet_base parameter (new code path) in extract_mermaid_blocks."""

    def test_custom_snippet_base_resolves_correctly(self, tmp_path):
        (tmp_path / "diagrams").mkdir()
        mmd = tmp_path / "diagrams" / "test.mmd"
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        md = tmp_path / "docs" / "cheat_sheets" / "doc.md"
        md.parent.mkdir(parents=True)
        md.write_text('```mermaid\n--8<-- "diagrams/test.mmd"\n```\n', encoding="utf-8")
        blocks = validate_mermaid.extract_mermaid_blocks(str(md), snippet_base=tmp_path)
        assert len(blocks) == 1
        assert "graph TD" in blocks[0]


class TestValidateMmdFile:
    """Tests for _validate_mmd_file() — lines 166-187 and 213-214 via run()."""

    def test_validate_mmd_file_returns_0_on_pass(self, tmp_path):
        import subprocess

        def _write_svg_and_succeed(cmd, **kwargs):
            from pathlib import Path as _Path

            out = _Path(cmd[cmd.index("--input") + 1]).with_suffix(".svg")
            out.write_bytes(b"<svg>" + b"x" * 200 + b"</svg>")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        mmd = tmp_path / "test.mmd"
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        with (
            patch("validate_mermaid.subprocess.run", side_effect=_write_svg_and_succeed),
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
        ):
            mock_cfg.exists.return_value = False
            result = validate_mermaid._validate_mmd_file(str(mmd), tmp_path)
        assert result == 0

    def test_validate_mmd_file_returns_1_on_fail(self, tmp_path):
        import subprocess

        def _fail(cmd, **kwargs):
            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="err")

        mmd = tmp_path / "test.mmd"
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        with (
            patch("validate_mermaid.subprocess.run", side_effect=_fail),
            patch("validate_mermaid.PUPPETEER_CONFIG") as mock_cfg,
        ):
            mock_cfg.exists.return_value = False
            result = validate_mermaid._validate_mmd_file(str(mmd), tmp_path)
        assert result == 1

    def test_validate_mmd_file_returns_1_when_not_found(self, tmp_path, capsys):
        result = validate_mermaid._validate_mmd_file(str(tmp_path / "missing.mmd"), tmp_path)
        assert result == 1
        assert "file not found" in capsys.readouterr().err

    def test_validate_mmd_file_returns_1_outside_repo_root(self, tmp_path):
        other = tmp_path / "outside" / "test.mmd"
        other.parent.mkdir(parents=True)
        other.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = validate_mermaid._validate_mmd_file(str(other), repo_root)
        assert result == 1

    def test_validate_mmd_file_returns_1_on_read_error(self, tmp_path, capsys):
        mmd = tmp_path / "locked.mmd"
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        mmd.chmod(0o000)
        try:
            result = validate_mermaid._validate_mmd_file(str(mmd), tmp_path)
        finally:
            mmd.chmod(0o644)
        assert result == 1
        assert "Cannot read" in capsys.readouterr().err

    def test_run_dispatches_mmd_file_to_validate_mmd_file(self, tmp_path):
        mmd = tmp_path / "test.mmd"
        mmd.write_text("graph TD\n  A --> B\n", encoding="utf-8")
        with (
            patch("validate_mermaid._repo_root", return_value=tmp_path),
            patch("validate_mermaid._validate_mmd_file", return_value=0) as mock_validate,
        ):
            result = validate_mermaid.run([str(mmd)])
        mock_validate.assert_called_once()
        assert result == 0


class TestMainBodyCoverage:
    """Tests for main() body — lines 260-261 (parse + sys.exit(run(...)))."""

    def test_main_calls_run_and_exits_with_its_return_value(self):
        with (
            patch("validate_mermaid.shutil.which", return_value="/usr/bin/mmdc"),
            patch("validate_mermaid.parse_args") as mock_parse,
            patch("validate_mermaid.run", return_value=0) as mock_run,
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_parse.return_value.md_files = ["dummy.md"]
            validate_mermaid.main()
        mock_run.assert_called_once_with(["dummy.md"])
        assert exc_info.value.code == 0
