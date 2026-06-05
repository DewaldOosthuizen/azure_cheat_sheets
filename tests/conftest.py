"""Shared pytest fixtures and helpers for the azure-cheat-sheets test suite."""

from __future__ import annotations

import re
from pathlib import Path

# The PyMdown Snippets base_path as configured in mkdocs.yml.
# Snippet paths inside cheat-sheet files are relative to docs/, e.g.
#   --8<-- "diagrams/networking/az305-decision-flow.mmd"
# resolves to  <repo>/docs/diagrams/networking/az305-decision-flow.mmd
REPO_ROOT = Path(__file__).parent.parent
SNIPPET_BASE = REPO_ROOT / "docs"

_SNIPPET_RE = re.compile(r"""--8<--\s+["']([^"']+)["']""")


def expand_snippets(text: str, base: Path = SNIPPET_BASE) -> str:
    """Replace every --8<-- "path" directive in *text* with the file's content.

    Paths are resolved relative to *base* (default: ``<repo>/docs/``), matching
    the ``base_path`` configured in mkdocs.yml for ``pymdownx.snippets``.

    Directives that reference a missing file are left unexpanded so tests that
    assert on the directive itself are not accidentally broken.
    """

    def _replace(m: re.Match) -> str:
        rel = m.group(1)
        abs_path = (base / rel).resolve()
        try:
            return abs_path.read_text(encoding="utf-8")
        except OSError:
            return m.group(0)  # leave unexpanded on error

    return _SNIPPET_RE.sub(_replace, text)
