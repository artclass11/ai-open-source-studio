# Security Policy

## Supported versions

Only the latest release on the `main` branch is supported.

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Use GitHub's private **Report a vulnerability** feature on the repository security page. Include reproduction steps, affected files, impact, and a suggested mitigation where possible.

Do not include secrets, personal data, or live exploit payloads in a report.

## Automation safeguards

The weekly publisher has least-privilege repository permissions, does not use production credentials, runs dependency and secret checks, and stops before release when a gate fails. Release automation must never be used to process private user content.
