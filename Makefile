# Makefile — local CI replication for azure-cheat-sheets
#
# All Python work runs inside a local .venv so nothing touches the system
# Python. The venv is created automatically the first time any Python target
# is invoked.
#
# Targets:
#   make venv              Create .venv and install dev deps (idempotent)
#   make install           Alias for venv + npm ci
#   make markdownlint      Lint Markdown files
#   make mermaid-check     Validate all Mermaid diagrams via mmdc
#   make python-lint       ruff check + ruff format --check
#   make python-lint-fix   Auto-fix safe ruff violations
#   make python-test       pytest with coverage (default venv Python)
#   make python-test-all   pytest across Python 3.11, 3.12, 3.13
#   make link-check        Dead-link check (requires lychee on PATH)
#   make ci                Full pipeline — no link-check (makes live HTTP calls)
#   make ci-full           Full pipeline including link-check
#   make clean             Remove .venv, node_modules, and build artefacts

# ── Configuration ──────────────────────────────────────────────────────────────
# Override on the command line: make python-test PYTHON=python3.12
PYTHON   ?= python3

VENV     := .venv
VENV_BIN := $(VENV)/bin
PY       := $(VENV_BIN)/python
PIP      := $(VENV_BIN)/pip

PUPPETEER_CONFIG_FILE ?= /tmp/puppeteer-config.json

MD_GLOBS         = "docs/**/*.md" "README.md" "AGENTS.md"
LINT_TARGETS     = scripts/ tests/
MD_FILES_VALIDATE = docs/*.md

# ── Phony declarations ─────────────────────────────────────────────────────────
.PHONY: help venv install \
        markdownlint \
        puppeteer-config mermaid-check \
        python-lint python-lint-fix \
        python-test python-test-311 python-test-312 python-test-313 python-test-all \
        link-check \
        ci ci-full \
        clean

# ── Default target ─────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "azure-cheat-sheets — local CI targets"
	@echo ""
	@echo "  make venv              Create .venv and install dev deps (idempotent)"
	@echo "  make install           venv + npm ci"
	@echo "  make markdownlint      Lint Markdown files"
	@echo "  make mermaid-check     Validate Mermaid diagrams"
	@echo "  make python-lint       ruff check + format check (inside .venv)"
	@echo "  make python-lint-fix   Auto-fix safe ruff violations"
	@echo "  make python-test       pytest with coverage (inside .venv)"
	@echo "  make python-test-all   pytest on Python 3.11, 3.12, and 3.13"
	@echo "  make link-check        Dead-link check (requires lychee)"
	@echo "  make ci                Full pipeline except link-check"
	@echo "  make ci-full           Full pipeline including link-check"
	@echo "  make clean             Remove .venv, node_modules, build artefacts"
	@echo ""

# ── Venv bootstrap ────────────────────────────────────────────────────────────
# The sentinel file $(VENV_BIN)/activate is recreated only when pyproject.toml
# changes, keeping re-installs fast during day-to-day work.
$(VENV_BIN)/activate: pyproject.toml
	@echo "--- creating .venv ---"
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip --quiet
	$(PIP) install -e '.[dev]' --quiet
	@touch $(VENV_BIN)/activate

venv: $(VENV_BIN)/activate

# ── Install (Python + Node) ────────────────────────────────────────────────────
install: venv
	npm ci

# ── markdownlint ──────────────────────────────────────────────────────────────
markdownlint:
	@echo "--- markdownlint ---"
	npx markdownlint-cli2 $(MD_GLOBS)

# ── Mermaid check ─────────────────────────────────────────────────────────────
puppeteer-config:
	@echo '{"args":["--no-sandbox","--disable-setuid-sandbox"]}' > $(PUPPETEER_CONFIG_FILE)

mermaid-check: puppeteer-config
	@echo "--- mermaid-check ---"
	npm ci
	npm audit --audit-level=high
	PUPPETEER_CONFIG_FILE=$(PUPPETEER_CONFIG_FILE) \
	  PATH="$(CURDIR)/node_modules/.bin:$(PATH)" \
	  $(PY) scripts/validate_mermaid.py $(MD_FILES_VALIDATE)

# ── Python lint ───────────────────────────────────────────────────────────────
python-lint: venv
	@echo "--- python-lint ---"
	$(VENV_BIN)/ruff check $(LINT_TARGETS)
	$(VENV_BIN)/ruff format --check $(LINT_TARGETS)

python-lint-fix: venv
	@echo "--- python-lint-fix ---"
	$(VENV_BIN)/ruff check --fix $(LINT_TARGETS)
	$(VENV_BIN)/ruff format $(LINT_TARGETS)

# ── Python test ───────────────────────────────────────────────────────────────
# Default: uses the venv created from $(PYTHON) (python3 unless overridden).
python-test: venv
	@echo "--- python-test ($(PY)) ---"
	$(VENV_BIN)/pytest tests/ -v \
	  --cov=scripts --cov-report=term-missing --cov-fail-under=90

# Per-version targets — each builds its own isolated venv in .venv-<ver>.
# Requires the named interpreter to be installed on the host.
.venv-311/bin/activate: pyproject.toml
	python3.11 -m venv .venv-311
	.venv-311/bin/pip install --upgrade pip --quiet
	.venv-311/bin/pip install -e '.[dev]' --quiet
	@touch .venv-311/bin/activate

.venv-312/bin/activate: pyproject.toml
	python3.12 -m venv .venv-312
	.venv-312/bin/pip install --upgrade pip --quiet
	.venv-312/bin/pip install -e '.[dev]' --quiet
	@touch .venv-312/bin/activate

.venv-313/bin/activate: pyproject.toml
	python3.13 -m venv .venv-313
	.venv-313/bin/pip install --upgrade pip --quiet
	.venv-313/bin/pip install -e '.[dev]' --quiet
	@touch .venv-313/bin/activate

python-test-311: .venv-311/bin/activate
	@echo "--- python-test (3.11) ---"
	.venv-311/bin/pytest tests/ -v \
	  --cov=scripts --cov-report=term-missing --cov-fail-under=90

python-test-312: .venv-312/bin/activate
	@echo "--- python-test (3.12) ---"
	.venv-312/bin/pytest tests/ -v \
	  --cov=scripts --cov-report=term-missing --cov-fail-under=90

python-test-313: .venv-313/bin/activate
	@echo "--- python-test (3.13) ---"
	.venv-313/bin/pytest tests/ -v \
	  --cov=scripts --cov-report=term-missing --cov-fail-under=90

python-test-all: python-test-311 python-test-312 python-test-313

# ── Link check ────────────────────────────────────────────────────────────────
link-check:
	@echo "--- link-check ---"
	lychee --verbose --no-progress \
	  --retry-wait-time 5 --max-retries 3 --timeout 30 \
	  docs/**/*.md README.md CONTRIBUTING.md AGENTS.md

# ── Full CI pipeline ──────────────────────────────────────────────────────────
ci: markdownlint mermaid-check python-lint python-test
	@echo ""
	@echo "=== CI passed ==="

ci-full: markdownlint mermaid-check python-lint python-test link-check
	@echo ""
	@echo "=== CI (full, including link-check) passed ==="

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf $(VENV) .venv-311 .venv-312 .venv-313
	rm -rf node_modules
	rm -rf .coverage .coverage.* htmlcov/ .pytest_cache/ .ruff_cache/
	rm -rf *.egg-info dist build
	@echo "--- clean done ---"
