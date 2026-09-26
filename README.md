# AI Open Source Studio

A privacy-first open-source studio by [@artclass11](https://github.com/artclass11). Every week, this repository publishes a small, useful AI developer tool with tests, documentation, security checks, and a permissive license.

## How it works

1. The weekly GitHub Actions workflow selects the next project from `projects/catalog.json`.
2. It creates a self-contained project directory from a reviewed template.
3. It runs formatting, tests, dependency, secret, license, and privacy checks.
4. If every gate passes, it commits the project and creates a public GitHub release automatically.
5. If a gate fails, the workflow stops without publishing and records the failure in the Actions log.

The workflow is scheduled for **Sunday at 19:00 IST** (`13:30 UTC`). GitHub Actions schedules can be delayed during load, so the release may appear a few minutes after the target time.

## Principles

- **Useful over flashy:** each project solves one concrete developer or community problem.
- **Privacy by default:** no telemetry, no hidden network calls, no credentials, and no personal data in fixtures.
- **Secure supply chain:** pinned actions, least-privilege permissions, dependency review, secret scanning, and CodeQL.
- **Transparent automation:** each release includes its source, tests, limitations, license, and responsible-use notes.
- **Automatic but bounded:** the catalog contains reviewed project specifications; automation cannot invent arbitrary public content or modify protected policy files.

## Projects

- [`projects/week-01-private-prompt-firewall`](projects/week-01-private-prompt-firewall) — a local Python redaction and prompt-safety utility that removes common secrets and personal identifiers before text is sent to an AI system.

## Local development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e 'projects/week-01-private-prompt-firewall[dev]'
pytest -q
```

## Governance

See [SECURITY.md](SECURITY.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [PRIVACY.md](PRIVACY.md). This repository is provided for educational and developer-productivity use; users remain responsible for validating outputs and complying with applicable laws and policies.
