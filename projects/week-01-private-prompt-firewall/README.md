# Private Prompt Firewall

A small, local-first Python utility that redacts common secrets and personal identifiers before text is pasted into an AI tool or shared with a collaborator.

## Install

```bash
pip install -e '.[dev]'
```

## Use

```bash
printf 'Email me at alice@example.com; token=demo-value' | prompt-firewall
```

The tool writes redacted text to standard output and never sends input over the network. Redaction is heuristic, not guaranteed anonymization; always review the result before sharing.

## API

```python
from private_prompt_firewall import redact

result = redact('Contact alice@example.com or use token=demo-value')
print(result.text)
print(result.findings)
```

Licensed under MIT.
