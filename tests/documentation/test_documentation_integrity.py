"""Test suite for verifying documentation integrity."""

import os
import re
from pathlib import Path

import pytest


class DocIntegrityChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(
            os.path.dirname(os.path.dirname(os.path.dirname(project_root)))
        )
        self.docs_dir = self.project_root / "docs"

    def _read_markdown_file(self, path: Path) -> str:
        """Read markdown file content."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {path}")
            return ""

    def _extract_sections(self, content: str) -> dict:
        """Extract markdown sections by headers."""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("#"):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line.lstrip("#").strip()
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()
        return sections

    def check_privacy_emphasis(self) -> bool:
        """Check that privacy is emphasized in all main docs."""
        main_docs = [
            self.docs_dir / "README.md",
            self.docs_dir / "architecture.md",
            self.docs_dir / "development.md",
            self.docs_dir / "project.md",
        ]

        privacy_keywords = ["privacy", "secure", "local", "protection"]
        for doc in main_docs:
            content = self._read_markdown_file(doc)
            if not any(keyword in content.lower() for keyword in privacy_keywords):
                return False
        return True

    def check_documentation_structure(self) -> bool:
        """Verify the documentation structure."""
        required_files = [
            self.docs_dir / "README.md",
            self.docs_dir / "architecture.md",
            self.docs_dir / "development.md",
            self.docs_dir / "project.md",
        ]
        return all(f.exists() for f in required_files)

    def check_feature_alignment(self) -> bool:
        """Check feature alignment across documentation."""
        readme = self._read_markdown_file(self.docs_dir / "README.md")
        project = self._read_markdown_file(self.docs_dir / "project.md")

        readme_features = set(re.findall(r"- (.*)", readme))
        project_features = set(re.findall(r"- (.*)", project))

        return bool(readme_features & project_features)  # Should have some overlap

    def check_architecture_implementation(self) -> bool:
        """Verify architecture components have implementation."""
        arch_doc = self._read_markdown_file(self.docs_dir / "architecture.md")
        components = re.findall(r"### (\w+)", arch_doc)

        src_dir = self.project_root / "src"
        for component in components:
            if not any(
                Path(root).glob(f"*{component}*.py") for root, _, _ in os.walk(src_dir)
            ):
                return False
        return True


def test_privacy_emphasis():
    """Test that privacy is emphasized in all documentation."""
    checker = DocIntegrityChecker(__file__)
    assert checker.check_privacy_emphasis(), "Privacy not sufficiently emphasized"


def test_documentation_structure():
    """Test that documentation structure is correct."""
    checker = DocIntegrityChecker(__file__)
    assert checker.check_documentation_structure(), "Documentation structure incorrect"


def test_feature_alignment():
    """Test that features are aligned across documentation."""
    checker = DocIntegrityChecker(__file__)
    assert checker.check_feature_alignment(), "Features not aligned across docs"


def test_architecture_implementation():
    """Test that architecture components have corresponding implementation."""
    checker = DocIntegrityChecker(__file__)
    assert (
        checker.check_architecture_implementation()
    ), "Missing component implementation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
