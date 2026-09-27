from week_02_ai_output_checklist import describe


def test_project_metadata_is_present():
    metadata = describe()
    assert metadata['id'].startswith('week-')
    assert metadata['title']
    assert metadata['summary']
