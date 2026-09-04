# Contributing

## Before contributing

Review the repository's security policy and confirm that your contribution uses synthetic data only. Do not include secrets, credentials, personal data, internal paths, or customer data.

## Content rules

- Use synthetic data in examples, tests, screenshots, and documentation.
- Link to primary sources for factual claims.
- State the exact license for each dependency and model used.
- Never commit secrets, credentials, API keys, or tokens.

## Verification

Run the following commands before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile examples/openai_responses_masked.py
python3 examples/openai_responses_masked.py --dry-run
git diff --check
```

## Pull requests

Describe the user-facing change, cite relevant primary sources, list dependency and model licenses, and include the verification results. Keep pull requests focused and remove any sensitive data before submission.
