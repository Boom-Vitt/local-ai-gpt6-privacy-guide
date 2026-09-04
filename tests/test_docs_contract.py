from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YOUTUBE_HERO = Path("assets/local-ai-hermes-youtube-cover-v3.png")
APPROVED_TRACKED_FILES = frozenset(
    {
        ".env.example",
        ".gitignore",
        "CONTRIBUTING.md",
        "LICENSE",
        "README.md",
        "SECURITY.md",
        "assets/README.md",
        YOUTUBE_HERO.as_posix(),
        "assets/local-ai-gpt6-privacy-hero.png",
        "assets/local-ai-hermes-youtube-cover-v2.png",
        "docs/agent-era-with-hermes.md",
        "docs/architecture.md",
        "docs/open-source-stack.md",
        "docs/openai-api.md",
        "docs/platforms.md",
        "docs/privacy-and-data-masking.md",
        "docs/superpowers/plans/2026-09-04-local-ai-gpt6-privacy-guide.md",
        "docs/superpowers/specs/2026-09-04-local-ai-gpt6-privacy-guide-design.md",
        "examples/README.md",
        "examples/openai_responses_masked.py",
        "tests/test_docs_contract.py",
        "tests/test_openai_responses_masked.py",
    }
)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
)


def tracked_files() -> frozenset[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return frozenset(
        path.decode("utf-8")
        for path in completed.stdout.split(b"\0")
        if path
    )


class DocumentationContractTests(unittest.TestCase):
    def test_tracked_inventory_matches_approved_public_tree(self) -> None:
        self.assertEqual(tracked_files(), APPROVED_TRACKED_FILES)

    def test_every_approved_tracked_file_exists(self) -> None:
        missing = [
            path for path in sorted(APPROVED_TRACKED_FILES) if not (ROOT / path).is_file()
        ]
        self.assertEqual(missing, [])

    def test_readme_has_core_contract(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in (
            "Local-first",
            "Data Masking",
            "GPT-6 Astra",
            "Hermes",
            "gpt-6-astra",
            "docs/agent-era-with-hermes.md",
            "store=False",
            "Zero Data Retention",
            "macOS",
            "Windows",
            "Linux",
            "Open Source",
            "English summary",
        ):
            self.assertIn(phrase, text)

    def test_readme_uses_a_large_widescreen_youtube_hero(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        hero_match = re.search(r"!\[[^\]]*\]\((assets/[^)]+)\)", text)
        self.assertIsNotNone(hero_match)
        self.assertEqual(hero_match.group(1), YOUTUBE_HERO.as_posix())

        data = (ROOT / YOUTUBE_HERO).read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        self.assertGreaterEqual(width, 1280)
        self.assertGreaterEqual(height, 720)
        self.assertAlmostEqual(width / height, 16 / 9, delta=0.002)

    def test_agent_era_article_keeps_the_hermes_privacy_boundary(self) -> None:
        text = (ROOT / "docs/agent-era-with-hermes.md").read_text(encoding="utf-8")
        for phrase in (
            "orchestration layer",
            "deterministic masking/RAG",
            "Human approval",
            "Hermes ไม่ควรเป็นคลังเอกสารดิบ",
            "ขอบเขตความปลอดภัยที่บังคับได้จริง",
            "cost_per_completed_task",
            "ยังไม่ได้ติดตั้ง Local AI",
        ):
            self.assertIn(phrase, text)
        for unsupported_or_copied_marker in (
            "ขอต้อนรับสู่ยุค AGI",
            "════════",
        ):
            self.assertNotIn(unsupported_or_copied_marker, text)

    def test_open_source_stack_covers_hermes_license_and_scope(self) -> None:
        text = (ROOT / "docs/open-source-stack.md").read_text(encoding="utf-8")
        for phrase in ("Hermes Agent", "MIT", "single-tenant"):
            self.assertIn(phrase, text)

    def test_tracked_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        tracked = tracked_files()
        markdown_paths = sorted(
            path for path in tracked if Path(path).suffix.lower() == ".md"
        )
        for relative_path in markdown_paths:
            markdown = ROOT / relative_path
            for target in MARKDOWN_LINK_PATTERN.findall(
                markdown.read_text(encoding="utf-8")
            ):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                resolved = (markdown.parent / file_part).resolve()
                try:
                    tracked_target = resolved.relative_to(ROOT.resolve()).as_posix()
                except ValueError:
                    failures.append(f"{relative_path} -> {target}")
                    continue
                if not resolved.exists() or tracked_target not in tracked:
                    failures.append(f"{relative_path} -> {target}")
        self.assertEqual(failures, [])

    def test_tracked_readable_text_contains_no_secret_shaped_values(self) -> None:
        failures: list[str] = []
        for relative_path in sorted(tracked_files()):
            path = ROOT / relative_path
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    failures.append(relative_path)
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
