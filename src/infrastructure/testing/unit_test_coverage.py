"""Unit test coverage system for monitoring test coverage."""

import os
from typing import Dict, List, Optional, Sequence

from coverage import Coverage


class UnitTestCoverage:
    """System for managing unit test coverage."""

    def __init__(self, source_dir: str) -> None:
        """Initialize the coverage system."""
        self.source_dir = source_dir
        self.coverage = Coverage(source=[source_dir], branch=False)
        self.coverage.start()

    def stop_coverage(self) -> None:
        """Stop collecting coverage data."""
        self.coverage.stop()
        self.coverage.save()

    def report_coverage(self) -> float:
        """Generate a coverage report."""
        return self.coverage.report()

    def get_uncovered_lines(self) -> Dict[str, List[int]]:
        """Get lines that are not covered by tests."""
        uncovered: Dict[str, List[int]] = {}
        for filename in self.coverage.get_data().measured_files():
            analysis = self.coverage.analysis(filename)
            if isinstance(analysis[3], Sequence):
                missing_lines = [int(line) for line in analysis[3]]
                if missing_lines:
                    uncovered[filename] = sorted(missing_lines)
        return uncovered
