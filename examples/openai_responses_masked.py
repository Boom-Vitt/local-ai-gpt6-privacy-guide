from __future__ import annotations

import argparse
import json
import os
from typing import Any

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-6-astra")
SYNTHETIC_RAW_MARKERS = ("SYNTHETIC_RAW_MARKER_DO_NOT_SEND",)
MASKED_CONTEXT = (
    "ลูกค้า [[PERSON:A1]] ติดต่อผ่าน [[PHONE:B2]] "
    "เรื่องคำสั่งซื้อ [[ORDER:C3]]"
)
QUESTION = "สรุปประเด็นและรายการติดตาม โดยคง token ที่ถูก mask ไว้"


def build_payload(
    masked_context: str,
    question: str,
    model: str = DEFAULT_MODEL,
) -> dict[str, object]:
    if not masked_context.strip() or not question.strip():
        raise ValueError("masked_context and question must not be empty")
    return {
        "model": model,
        "store": False,
        "instructions": (
            "Use only the supplied masked context. Preserve masking tokens. "
            "Do not infer or reconstruct personal data."
        ),
        "input": f"MASKED CONTEXT:\n{masked_context}\n\nQUESTION:\n{question}",
    }


def assert_raw_markers_absent(
    payload: dict[str, object],
    raw_markers: tuple[str, ...],
) -> None:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    leaked = [marker for marker in raw_markers if marker in serialized]
    if leaked:
        raise ValueError("raw synthetic marker detected; refusing egress")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a masked GPT-6 Astra Responses API request."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--send", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_payload(MASKED_CONTEXT, QUESTION)
    assert_raw_markers_absent(payload, SYNTHETIC_RAW_MARKERS)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for --send")

    from openai import OpenAI

    client = OpenAI()
    response: Any = client.responses.create(**payload)
    print(response.output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
