from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED_TRACKED_FILES = frozenset(
    {
        ".env.example",
        ".gitignore",
        "CONTRIBUTING.md",
        "LICENSE",
        "README.md",
        "SECURITY.md",
        "assets/README.md",
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
            "gpt-6-astra",
            "store=False",
            "Zero Data Retention",
            "macOS",
            "Windows",
            "Linux",
            "Open Source",
            "English summary",
        ):
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
