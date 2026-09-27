"""A transparent starter module for this reviewed weekly project."""

PROJECT_ID = 'week-02-ai-output-checklist'
PROJECT_TITLE = 'AI Output Checklist'
PROJECT_SUMMARY = 'A local checklist runner that flags missing citations, uncertainty labels, and unsafe claims in generated text.'

def describe() -> dict[str, str]:
    return {"id": PROJECT_ID, "title": PROJECT_TITLE, "summary": PROJECT_SUMMARY}
