# Safe masked Responses API example

Run `--dry-run` to print the masked request payload without making a network
request. This is the only mode used by repository verification.

`--send` is opt-in. It requires the reader to install the OpenAI SDK and
provide `OPENAI_API_KEY` themselves.

The script receives already-masked synthetic context; it is not a PII
detector. Production systems need a local detector, human preview/approval,
second egress scan, bounded retry, and redacted logging.

`store=False` does not grant Zero Data Retention.
