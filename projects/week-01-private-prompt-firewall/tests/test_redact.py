from private_prompt_firewall import redact


def test_redacts_email_and_api_key():
    synthetic_key = "sk-" + "test-1234567890abcdef"
    result = redact(f"Email alice@example.com with token={synthetic_key}")
    assert "alice@example.com" not in result.text
    assert synthetic_key not in result.text
    assert {finding.category for finding in result.findings} == {"email", "openai_key", "secret_assignment"}


def test_does_not_change_safe_text():
    result = redact("Explain how a compiler works.")
    assert result.text == "Explain how a compiler works."
    assert result.findings == ()


def test_redacts_github_token_and_bearer_token():
    synthetic_github_token = "ghp_" + "123456789012345678901234567890"
    result = redact(f"{synthetic_github_token} and Bearer abcdefghijklmnop")
    assert synthetic_github_token not in result.text
    assert "Bearer abcdefghijklmnop" not in result.text
