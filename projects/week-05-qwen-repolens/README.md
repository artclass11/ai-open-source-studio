# RepoLens — Local AI Repository Auditor

> Understand a codebase in minutes — privately, locally, and with evidence.

RepoLens uses **Qwen/Qwen3.5-4B** from Hugging Face to inspect a local repository and optionally a UI/architecture screenshot. It produces a structured engineering report with architecture, key files, risks, and concrete next steps.

The model runs locally through Hugging Face Transformers. No hosted LLM API is required.

## Why Qwen3.5-4B?

Qwen3.5-4B is an Apache-2.0 model on Hugging Face with a unified vision-language architecture. Its model card documents native 262K context, local Transformers/vLLM/SGLang usage, and multimodal support.

Model: https://huggingface.co/Qwen/Qwen3.5-4B

## Quick start

Requires Python 3.10+.

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
repolens inspect /path/to/repository
repolens inspect /path/to/repository --question "Where is authentication implemented?"
repolens inspect /path/to/repository --image ui.png
~~~

The first run downloads the model into the normal Hugging Face cache. A GPU is strongly recommended for practical inference; CPU execution is possible but substantially slower.

Use `--format json` for machine-readable output.

## Safety and privacy

RepoLens is intentionally local-first:

- skips common credential and secret files
- never uploads repository files by itself
- reports relative paths rather than absolute filesystem paths
- limits file size and total context
- asks the model to separate observations from uncertainty

A local model can still make mistakes. Treat generated findings as review candidates, not proof.

## Supported inputs

RepoLens scans common source and documentation files including Python, JavaScript/TypeScript, Java/Kotlin, Go, Rust, C/C++, Swift, PHP, Ruby, SQL, Markdown, YAML, JSON, TOML, XML, HTML and CSS.

Binary files, dependency directories, build outputs, VCS metadata, secrets, and very large files are skipped by default.

## License

MIT.
