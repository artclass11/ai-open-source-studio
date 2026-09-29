# AI Open Source Studio

A privacy-first open-source studio by [@artclass11](https://github.com/artclass11). Every week, this repository publishes a small, useful AI developer tool with tests, documentation, security checks, and a permissive license.

## Projects

- [projects/week-01-private-prompt-firewall](projects/week-01-private-prompt-firewall) — local redaction and prompt-safety utility.
- [projects/week-05-qwen-repolens](projects/week-05-qwen-repolens) — local repository and screenshot auditor powered by **Qwen/Qwen3.5-4B**, producing architecture notes, evidence-backed risks, and concrete next steps.

## Why the model matters

RepoLens uses the Hugging Face **Qwen/Qwen3.5-4B** model locally. The model is published under Apache-2.0 and supports multimodal input, so the project can combine repository text with an optional screenshot while keeping the application local.

## Automation

The weekly workflow selects reviewed projects from [projects/catalog.json](projects/catalog.json), validates safety and tests, and can publish releases automatically.

The repository follows a privacy-first approach: no telemetry, no hidden network calls, no credentials, and no personal data in fixtures.

## Local development

See the individual project README for each tool's setup and test commands.

## Governance

See [SECURITY.md](SECURITY.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [PRIVACY.md](PRIVACY.md).
