#!/usr/bin/env python3
"""Validate all fenced mermaid blocks in a Markdown file using mmdc."""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PUPPETEER_CONFIG = Path("/tmp/puppeteer-config.json")


def _repo_root() -> Path:
    """Return the repository root directory (parent of the scripts/ folder)."""
    return Path(__file__).parent.parent.resolve()


def _extract_from_text(text: str) -> list[str]:
    """Extract mermaid diagram sources from a Markdown string.

    The regex tolerates trailing whitespace on the opening fence line
    (e.g. ```mermaid   ) and Windows-style CRLF line endings — both of which
    would silently produce zero matches with the original ``\\n``-only pattern,
    causing CI to exit 0 with no diagrams validated (false green).
    """
    pattern = re.compile(r"```mermaid\s*\r?\n(.*?)```", re.DOTALL)
    return pattern.findall(text)


def extract_mermaid_blocks(md_path):
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    return _extract_from_text(content)


def validate_block(index, diagram_src):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(diagram_src)
    tmp_path = Path(tmp.name)
    out_path = tmp_path.with_suffix(".svg")
    try:
        cmd = ["mmdc", "--input", str(tmp_path), "--output", str(out_path)]
        if PUPPETEER_CONFIG.exists():
            cmd += ["--puppeteerConfigFile", str(PUPPETEER_CONFIG)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return (False, "mmdc timed out after 60 s")
    except FileNotFoundError:
        # Guard against race-condition where mmdc is removed mid-run after the which() check
        return (False, "mmdc binary not found on PATH")
    finally:
        tmp_path.unlink(missing_ok=True)
        out_path.unlink(missing_ok=True)


def main():
    # Guard: verify mmdc is available before proceeding; exit early with clear message
    if shutil.which("mmdc") is None:
        print(
            "ERROR: mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        sys.exit(2)

    parser = argparse.ArgumentParser(
        description="Validate fenced Mermaid blocks in one or more Markdown files."
    )
    parser.add_argument("md_files", nargs="+", help="Markdown file(s) to validate")
    args = parser.parse_args()

    repo_root = _repo_root()

    total_failed = 0
    for md_path in args.md_files:
        if not Path(md_path).is_file():
            print(f"Error: file not found: {md_path}", file=sys.stderr)
            total_failed += 1
            continue
        resolved = Path(md_path).resolve()
        if not str(resolved).startswith(str(repo_root) + "/") and resolved != repo_root:
            print(f"Error: path outside repository root: {md_path}", file=sys.stderr)
            total_failed += 1
            continue
        blocks = extract_mermaid_blocks(md_path)
        print(f"Found {len(blocks)} mermaid diagram(s) in {md_path}")
        if not blocks:
            print(
                f"WARNING: no mermaid blocks found in {md_path} — check fence syntax.",
                file=sys.stderr,
            )
            total_failed += 1
            continue
        for i, block in enumerate(blocks, start=1):
            ok, stderr = validate_block(i, block)
            if ok:
                print(f"  Diagram {i}: PASS")
            else:
                print(f"  Diagram {i}: FAIL")
                if stderr:
                    print(stderr)
                total_failed += 1

    if total_failed:
        print(f"\n{total_failed} issue(s) across all files.")
        sys.exit(1)
    else:
        print("\nAll diagrams passed.")


if __name__ == "__main__":
    main()
