from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from examples.openai_responses_masked import (  # noqa: E402
    SYNTHETIC_RAW_MARKERS,
    assert_raw_markers_absent,
    build_payload,
)


class MaskedPayloadTests(unittest.TestCase):
    def test_payload_uses_gpt6_responses_shape_without_storage(self) -> None:
        payload = build_payload(
            masked_context="ลูกค้า [[PERSON:A1]] ติดต่อผ่าน [[PHONE:B2]]",
            question="สรุปประเด็นที่ต้องติดตาม",
            model="gpt-6-astra",
        )

        self.assertEqual(payload["model"], "gpt-6-astra")
        self.assertIs(payload["store"], False)
        self.assertIn("[[PERSON:A1]]", str(payload["input"]))
        self.assertIn("[[PHONE:B2]]", str(payload["input"]))

    def test_raw_marker_guard_rejects_leak(self) -> None:
        with self.assertRaises(ValueError):
            assert_raw_markers_absent(
                {"input": "SYNTHETIC_RAW_MARKER_DO_NOT_SEND"},
                SYNTHETIC_RAW_MARKERS,
            )

    def test_dry_run_is_offline_and_contains_no_raw_marker(self) -> None:
        env = os.environ.copy()
        env.pop("OPENAI_MODEL", None)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "examples" / "openai_responses_masked.py"),
                "--dry-run",
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["model"], "gpt-6-astra")
        self.assertIs(payload["store"], False)
        for marker in SYNTHETIC_RAW_MARKERS:
            self.assertNotIn(marker, completed.stdout)

    def test_dry_run_honors_explicit_model_override(self) -> None:
        env = os.environ.copy()
        env["OPENAI_MODEL"] = "synthetic-model-override"
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "examples" / "openai_responses_masked.py"),
                "--dry-run",
            ],
            check=True,
            capture_output=True,
            env=env,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(payload["model"], "synthetic-model-override")


if __name__ == "__main__":
    unittest.main()
