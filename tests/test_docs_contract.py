from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    ".env.example",
    ".gitignore",
    "assets/README.md",
    "docs/architecture.md",
    "docs/open-source-stack.md",
    "docs/openai-api.md",
    "docs/platforms.md",
    "docs/privacy-and-data-masking.md",
    "examples/README.md",
    "examples/openai_responses_masked.py",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
)
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".superpowers",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}


def is_publishable_path(path: Path) -> bool:
    return not any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts)


class DocumentationContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
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

    def test_local_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures: list[str] = []
        for markdown in ROOT.rglob("*.md"):
            if not is_publishable_path(markdown):
                continue
            for target in link_pattern.findall(markdown.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                if not (markdown.parent / file_part).resolve().exists():
                    failures.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])

    def test_repository_contains_no_secret_shaped_values(self) -> None:
        failures: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or not is_publishable_path(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    failures.append(str(path.relative_to(ROOT)))
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
