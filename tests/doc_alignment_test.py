"""Test alignment between DEVELOPMENT_FRAMEWORK.md and PROGRESS.md."""

import os
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple


class DocumentAnalyzer:
    def __init__(self, framework_path: str, progress_path: str):
        """Initialize with paths to both documents."""
        self.framework_path = framework_path
        self.progress_path = progress_path
        self.framework_content = self._read_file(framework_path)
        self.progress_content = self._read_file(progress_path)

    def _read_file(self, path: str) -> str:
        """Read file content."""
        with open(path, "r") as f:
            return f.read()

    def extract_features_from_framework(self) -> Dict[str, List[str]]:
        """Extract feature pillars and their sub-features from framework doc."""
        features = {}
        current_pillar = None
        in_feature_section = False

        for line in self.framework_content.split("\n"):
            if "## Feature Pillars" in line:
                in_feature_section = True
                continue
            if in_feature_section and line.startswith("##"):
                break
            if in_feature_section and line.strip():
                if (
                    line.startswith("1.")
                    or line.startswith("2.")
                    or line.startswith("3.")
                    or line.startswith("4.")
                ):
                    current_pillar = re.sub(r"^[0-9\.\s]+", "", line.strip().lower())
                    features[current_pillar] = []
                elif line.strip().startswith("-") and current_pillar:
                    sub_feature = re.sub(r"^[-\s]+", "", line.strip().lower())
                    features[current_pillar].append(sub_feature)

        return features

    def extract_features_from_progress(self) -> Dict[str, Dict[str, any]]:
        """Extract features and their implementation status from progress doc."""
        features = {}
        current_feature = None
        in_feature_section = False

        for line in self.framework_content.split("\n"):
            if (
                "### 1." in line
                or "### 2." in line
                or "### 3." in line
                or "### 4." in line
            ):
                current_feature = re.sub(r"^###\s*[0-9\.\s]+", "", line.strip().lower())
                status_match = re.search(r"\((.*?)\)", line)
                status = status_match.group(1).lower() if status_match else "unknown"
                features[current_feature] = {
                    "status": status,
                    "sub_features": [],
                    "completion": 0,
                }
            elif current_feature and line.strip().startswith("-"):
                sub_feature = re.sub(r"^\[[ x]\]|\d+\.|[-•]", "", line.strip().lower())
                sub_feature = re.sub(r"✅|\(.*\)", "", sub_feature).strip()
                if sub_feature:
                    completed = "✅" in line or "[x]" in line
                    features[current_feature]["sub_features"].append(
                        {"name": sub_feature, "completed": completed}
                    )

        # Calculate completion percentages
        for feature in features.values():
            completed = sum(1 for sf in feature["sub_features"] if sf["completed"])
            total = len(feature["sub_features"])
            feature["completion"] = (completed / total * 100) if total > 0 else 0

        return features

    def extract_timeline(self) -> List[Dict[str, any]]:
        """Extract sprint timeline and dates."""
        sprints = []
        current_sprint = None
        in_sprint_section = False

        for line in self.progress_content.split("\n"):
            if "### Sprint" in line:
                date_match = re.search(r"\((.*?)\)", line)
                if date_match:
                    dates = date_match.group(1)
                    current_sprint = {
                        "name": line.split("(")[0].strip(),
                        "dates": dates,
                        "features": [],
                    }
                    sprints.append(current_sprint)
            elif current_sprint and line.strip().startswith("-"):
                feature = re.sub(r"^\[[ x]\]|\d+\.|[-•]", "", line.strip().lower())
                feature = re.sub(r"✅|\(.*\)", "", feature).strip()
                if feature:
                    current_sprint["features"].append(feature)

        return sprints

    def extract_risks(self) -> List[Dict[str, str]]:
        """Extract risks and their status."""
        risks = []
        in_risk_section = False

        for line in self.progress_content.split("\n"):
            if "## Risk Tracking" in line:
                in_risk_section = True
                continue
            if in_risk_section and line.startswith("##"):
                break
            if in_risk_section and line.strip().startswith(("1.", "2.", "3.")):
                risk = re.sub(r"^[0-9\.\s]+", "", line.strip())
                impact_match = re.search(r"Impact:\s*(.*?)(?=\n|-|$)", line)
                status_match = re.search(r"Status:\s*(.*?)(?=\n|-|$)", line)
                risks.append(
                    {
                        "description": risk,
                        "impact": (
                            impact_match.group(1).strip() if impact_match else "Unknown"
                        ),
                        "status": (
                            status_match.group(1).strip() if status_match else "Unknown"
                        ),
                    }
                )

        return risks


def test_document_alignment():
    """Test suite for document alignment."""
    # Initialize analyzer
    framework_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "DEVELOPMENT_FRAMEWORK.md"
    )
    progress_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "PROGRESS.md"
    )
    analyzer = DocumentAnalyzer(framework_path, progress_path)

    # Test feature alignment
    framework_features = analyzer.extract_features_from_framework()
    progress_features = analyzer.extract_features_from_progress()

    # Check feature presence
    for pillar in framework_features:
        assert (
            pillar in progress_features
        ), f"Feature pillar '{pillar}' missing in progress"
        framework_subs = set(framework_features[pillar])
        progress_subs = set(
            sf["name"] for sf in progress_features[pillar]["sub_features"]
        )
        missing_subs = framework_subs - progress_subs
        assert (
            not missing_subs
        ), f"Sub-features missing in progress for {pillar}: {missing_subs}"

    # Check completion tracking
    for feature, data in progress_features.items():
        assert "completion" in data, f"Completion tracking missing for {feature}"
        assert isinstance(
            data["completion"], (int, float)
        ), f"Invalid completion value for {feature}"
        assert (
            0 <= data["completion"] <= 100
        ), f"Completion percentage out of range for {feature}"

    # Check timeline consistency
    timeline = analyzer.extract_timeline()
    assert timeline, "Timeline information missing"
    for sprint in timeline:
        assert all(
            key in sprint for key in ["name", "dates", "features"]
        ), f"Missing required sprint information in {sprint['name']}"

        # Validate dates
        if "Current" in sprint["name"]:
            dates = sprint["dates"].split("-")
            start_date = datetime.strptime(dates[0].strip(), "%b %d, %Y")
            end_date = datetime.strptime(dates[1].strip(), "%b %d, %Y")
            current_date = datetime.strptime(
                "2024-12-19", "%Y-%m-%d"
            )  # Hardcoded for example
            assert (
                start_date <= current_date <= end_date
            ), f"Current sprint dates ({sprint['dates']}) don't match current date"

    # Check risk tracking
    risks = analyzer.extract_risks()
    assert risks, "Risk tracking information missing"
    for risk in risks:
        assert all(
            key in risk for key in ["description", "impact", "status"]
        ), f"Missing required risk information in {risk['description']}"


if __name__ == "__main__":
    test_document_alignment()
