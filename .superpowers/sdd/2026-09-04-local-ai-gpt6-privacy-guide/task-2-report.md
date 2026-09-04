# Task 2 report: Safe masked Responses API example

## Implementation

- Added `examples/openai_responses_masked.py` with the required
  `build_payload`, `assert_raw_markers_absent`, and `main` interfaces.
- The payload uses `OPENAI_MODEL` (default `gpt-6-astra`), `store=False`, and
  only the supplied masked synthetic context.
- `--dry-run` prints JSON and performs no API import or network request.
- `--send` is explicitly opt-in, requires `OPENAI_API_KEY`, and imports the
  OpenAI SDK only at send time.
- Added `examples/README.md` documenting dry-run verification, opt-in live
  sending, synthetic pre-masked input, production safeguards, and the limits
  of `store=False`.
- Added `tests/test_openai_responses_masked.py` with the prescribed three
  offline tests.

## TDD evidence

RED command (after writing the tests and before implementation):

```text
$ python3 -m unittest tests/test_openai_responses_masked.py -v
test_openai_responses_masked (unittest.loader._FailedTest.test_openai_responses_masked) ... ERROR
ImportError: Failed to import test module: test_openai_responses_masked
ModuleNotFoundError: No module named 'examples'
Ran 1 test in 0.000s
FAILED (errors=1)
```

The failure was caused by the missing `examples` implementation package.

GREEN command after the minimal implementation:

```text
$ python3 -m unittest tests/test_openai_responses_masked.py -v
test_dry_run_is_offline_and_contains_no_raw_marker ... ok
test_payload_uses_gpt6_responses_shape_without_storage ... ok
test_raw_marker_guard_rejects_leak ... ok
Ran 3 tests in 0.028s
OK
```

## Verification

The task's full offline verification command was run:

```text
$ python3 -m unittest tests/test_openai_responses_masked.py -v
$ python3 -m py_compile examples/openai_responses_masked.py
$ python3 examples/openai_responses_masked.py --dry-run > /tmp/local-ai-gpt6-dry-run.json
$ python3 -m json.tool /tmp/local-ai-gpt6-dry-run.json >/dev/null
$ ! rg -n "SYNTHETIC_RAW_MARKER_DO_NOT_SEND" /tmp/local-ai-gpt6-dry-run.json
exit=0
```

The focused test suite reported 3/3 passing. No package installation, API
call, real key, publication, or push was performed.

## Files changed

- `examples/openai_responses_masked.py`
- `examples/README.md`
- `tests/test_openai_responses_masked.py`
- `.superpowers/sdd/2026-09-04-local-ai-gpt6-privacy-guide/task-2-report.md`

## Self-review

- Confirmed `store` is the boolean `False`, not a string.
- Confirmed the model is sourced from `OPENAI_MODEL` with the required
  `gpt-6-astra` fallback.
- Confirmed raw-marker scanning serializes the complete payload before any
  possible send.
- Confirmed the OpenAI SDK is imported only inside the explicit `--send`
  branch, so dry-run verification remains offline even when the SDK is absent.
- Confirmed empty masked context and question are rejected.
- `git diff --check` completed with no whitespace errors.

## Concerns

- This example assumes its input is already masked synthetic context; it does
  not detect or mask PII.
- The live path is intentionally untested and requires the reader's own SDK,
  API key, and explicit `--send` choice.
- `store=False` alone is not a Zero Data Retention guarantee.
