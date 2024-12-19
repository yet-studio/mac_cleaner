"""Test suite for verifying coherence between documentation files."""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest


class DocsCoherenceChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(
            os.path.dirname(os.path.dirname(os.path.dirname(project_root)))
        )
        self.docs_dir = self.project_root / "docs"
        self.readme_path = self.project_root / "README.md"

    def _read_markdown_file(self, path: Path) -> str:
        """Read markdown file content."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {path}")
            return ""

    def _extract_sections(self, content: str) -> Dict[str, str]:
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

    def _extract_components(self, content: str) -> Set[str]:
        """Extract components from markdown content."""
        components = set()
        lines = content.split("\n")
        in_components_section = False

        for line in lines:
            if line.startswith("## Core Components"):
                in_components_section = True
                continue
            elif in_components_section and line.startswith("##"):
                in_components_section = False
                continue

            if in_components_section and line.strip().startswith("- **"):
                component = line.split("**")[1].strip().lower()
                components.add(component)
            elif in_components_section and line.strip().startswith("### "):
                component = line.strip("# ").strip().lower()
                components.add(component)

        return components

    def _get_links(self, content: str) -> Set[str]:
        """Extract markdown links."""
        return set(re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content))

    def check_privacy_coherence(self) -> bool:
        """Check privacy emphasis is consistent."""
        docs = {
            "README": self._read_markdown_file(self.docs_dir / "README.md"),
            "Architecture": self._read_markdown_file(self.docs_dir / "architecture.md"),
            "Development": self._read_markdown_file(self.docs_dir / "development.md"),
            "Project": self._read_markdown_file(self.docs_dir / "project.md"),
        }

        privacy_terms = ["privacy", "secure", "local", "protection"]
        doc_privacy_counts = {
            name: sum(term in content.lower() for term in privacy_terms)
            for name, content in docs.items()
        }

        # Each doc should have at least some privacy mentions
        return all(count > 0 for count in doc_privacy_counts.values())

    def check_architecture_alignment(self) -> bool:
        """Check architecture components are consistently referenced."""
        arch_doc = self._read_markdown_file(self.docs_dir / "architecture.md")
        dev_doc = self._read_markdown_file(self.docs_dir / "development.md")

        # Extract components from both docs
        arch_components = self._extract_components(arch_doc)
        dev_components = self._extract_components(dev_doc)

        # Check if all architecture components are in development doc
        return all(component in dev_components for component in arch_components)

    def check_documentation_links(self) -> bool:
        """Check that all documentation links are valid."""
        docs = [
            self.docs_dir / "README.md",
            self.docs_dir / "architecture.md",
            self.docs_dir / "development.md",
            self.docs_dir / "project.md",
        ]

        for doc in docs:
            content = self._read_markdown_file(doc)
            links = self._get_links(content)

            for _, target in links:
                if target.endswith(".md"):
                    target_path = self.docs_dir / target
                    if not target_path.exists():
                        return False
        return True

    def check_readme_references(self) -> bool:
        """Check that README properly references core documentation."""
        readme = self._read_markdown_file(self.docs_dir / "README.md")
        required_refs = ["architecture.md", "development.md", "project.md"]

        links = self._get_links(readme)
        link_targets = {target for _, target in links}

        return all(ref in link_targets for ref in required_refs)


def test_privacy_coherence():
    """Test that privacy emphasis is consistent across documentation."""
    checker = DocsCoherenceChecker(__file__)
    assert checker.check_privacy_coherence(), "Privacy emphasis not consistent"


def test_architecture_alignment():
    """Test that architecture components are consistently referenced."""
    checker = DocsCoherenceChecker(__file__)
    assert checker.check_architecture_alignment(), "Architecture components misaligned"


def test_documentation_links():
    """Test that all documentation links are valid."""
    checker = DocsCoherenceChecker(__file__)
    assert checker.check_documentation_links(), "Invalid documentation links found"


def test_readme_references():
    """Test that README properly references core documentation."""
    checker = DocsCoherenceChecker(__file__)
    assert (
        checker.check_readme_references()
    ), "README missing core documentation references"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
