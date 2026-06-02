#!/usr/bin/env python3
"""Validate all fenced mermaid blocks in a Markdown file using mmdc."""

import os
import re
import shutil
import subprocess
import sys
import tempfile


def extract_mermaid_blocks(md_path):
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
    return pattern.findall(content)


def validate_block(index, diagram_src):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(diagram_src)
        tmp_path = tmp.name
    out_path = tmp_path.replace(".mmd", ".svg")
    try:
        result = subprocess.run(
            [
                "mmdc",
                "--input",
                tmp_path,
                "--output",
                out_path,
                "--puppeteerConfigFile",
                "/tmp/puppeteer-config.json",
            ],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        # Guard against race-condition where mmdc is removed mid-run after the which() check
        return (False, "mmdc binary not found on PATH")
    finally:
        os.unlink(tmp_path)
        if os.path.exists(out_path):
            os.unlink(out_path)


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
