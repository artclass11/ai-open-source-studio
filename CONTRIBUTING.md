# Contributing

Thanks for helping improve the studio.

1. Open an issue describing the problem or proposal.
2. Keep changes focused and include tests.
3. Do not add real personal data, credentials, copyrighted datasets, or unreviewed network integrations.
4. Run the local checks before opening a pull request:

```bash
python3 tools/validate_catalog.py
python3 tools/security_checks.py
pytest -q
```

By contributing, you agree that your contribution is provided under the repository license.
