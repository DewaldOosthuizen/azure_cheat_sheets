# DewaldOosthuizen/azure_cheat_sheets — Copilot Instructions

Always reference these instructions first and fall back to search or
bash only when you encounter something that does not match the info here.

---

<!-- graph-tools-start -->

## Code Exploration and Token Efficiency

If `.codegraph/` exists, use CodeGraph tools FIRST for symbol lookup,
context gathering, and call tracing before opening any source files.

```bash
codegraph context "<task description>" -p .
codegraph query "<ClassName or function>" -p .
codegraph affected <changed-files> -p .   # find affected tests
codegraph sync .                          # after any code changes
```

Fall back to grep/file reading only when these tools return insufficient results.

<!-- graph-tools-end -->
