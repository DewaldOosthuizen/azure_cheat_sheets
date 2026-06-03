#!/usr/bin/env python3
"""Validate all fenced mermaid blocks in a Markdown file using mmdc."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_default_puppeteer_config = Path(tempfile.gettempdir()) / "puppeteer-config.json"
PUPPETEER_CONFIG = Path(os.environ.get("PUPPETEER_CONFIG_FILE", str(_default_puppeteer_config)))


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate fenced Mermaid blocks in Markdown files using mmdc."
    )
    parser.add_argument("md_files", nargs="+", help="Markdown file(s) to validate")
    return parser.parse_args()


def run(md_paths: list[str]) -> int:
    """Orchestrate extraction and validation. Returns exit code (0/1/2)."""
    repo_root = _repo_root()
    for md_path in md_paths:
        if not Path(md_path).is_file():
            print(f"Error: file not found: {md_path}", file=sys.stderr)
            return 1
        resolved = Path(md_path).resolve()
        if not str(resolved).startswith(str(repo_root) + "/") and resolved != repo_root:
            print(f"Error: path outside repository root: {md_path}", file=sys.stderr)
            return 1
        blocks = extract_mermaid_blocks(md_path)
        print(f"Found {len(blocks)} mermaid diagram(s) in {md_path}")
        if not blocks:
            print("WARNING: no mermaid blocks found — check fence syntax.", file=sys.stderr)
            return 2
        failed = 0
        for i, block in enumerate(blocks, start=1):
            ok, stderr = validate_block(i, block)
            if ok:
                print(f"  Diagram {i}: PASS")
            else:
                print(f"  Diagram {i}: FAIL")
                if stderr:
                    print(stderr)
                failed += 1
        if failed:
            print(f"\n{failed} diagram(s) failed validation.")
            return 1
        print(f"\nAll {len(blocks)} diagram(s) passed.")
    return 0


def main():
    # Guard: verify mmdc is available before proceeding; exit early with clear message
    if shutil.which("mmdc") is None:
        print(
            "ERROR: mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        sys.exit(2)
    args = parse_args()
    sys.exit(run(args.md_files))


if __name__ == "__main__":
    main()
