# Tech Cheat Sheets

[![Lint](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml/badge.svg)](https://github.com/DewaldOosthuizen/azure_cheat_sheets/actions/workflows/lint.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/DewaldOosthuizen1)

## Purpose

This repository is an exam-prep reference, not a step-by-step tutorial. The
documents focus on choosing the right Azure service for a requirement and
understanding why that choice fits.

## Repository Structure

- [`AZ-305.md`](azure/cheat_sheets/AZ-305.md) — AZ-305 architect-focused cheat sheet
- [`AZ-104.md`](azure/cheat_sheets/AZ-104.md) — AZ-104 administrator-focused cheat sheet

Each top-level domain section is stored as a shared **section snippet file** under
`docs/azure/files/<section>/<section>.md` (e.g. `docs/azure/files/networking/networking.md`).
Both cheat sheets include the same snippet via `--8<-- "azure/files/<section>/<section>.md"`
directives, keeping domain content in a single place.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](https://github.com/DewaldOosthuizen/azure_cheat_sheets/blob/main/CONTRIBUTING.md) for
the full workflow, including how to pick up an issue, branch naming conventions,
local validation steps, and the pull request process.

## License

This project is licensed under the [`GPL-3.0`](LICENSE).
