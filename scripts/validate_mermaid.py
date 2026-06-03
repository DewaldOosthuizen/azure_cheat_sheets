#!/usr/bin/env python3
"""Validate all fenced mermaid blocks in a Markdown file using mmdc."""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


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
        result = subprocess.run(
            [
                "mmdc",
                "--input",
                str(tmp_path),
                "--output",
                str(out_path),
                "--puppeteerConfigFile",
                "/tmp/puppeteer-config.json",
            ],
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

    if len(sys.argv) < 2:
        print("Usage: validate_mermaid.py <markdown-file>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not Path(md_path).is_file():
        print(f"Error: file not found: {md_path}", file=sys.stderr)
        sys.exit(1)
    blocks = extract_mermaid_blocks(md_path)
    print(f"Found {len(blocks)} mermaid diagram(s) in {md_path}")

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
        sys.exit(1)
    else:
        print(f"\nAll {len(blocks)} diagram(s) passed.")


if __name__ == "__main__":
    main()
