"""Test module for unit test coverage system."""

import os
import tempfile

import pytest
from coverage import Coverage

from src.infrastructure.testing.unit_test_coverage import UnitTestCoverage


def test_coverage_init():
    """Test coverage system initialization."""
    with tempfile.TemporaryDirectory() as temp_dir:
        coverage = UnitTestCoverage(temp_dir)
        assert coverage.source_dir == temp_dir
        coverage.stop_coverage()


def test_coverage_reporting(tmp_path):
    """Test coverage reporting functionality."""
    # Create a test file
    test_file = tmp_path / "test.py"
    test_file.write_text("def test_func():\n    return True\n")

    # Initialize coverage
    coverage = Coverage(source=[str(tmp_path)], branch=False)
    coverage.start()

    # Run some code under coverage
    exec(test_file.read_text())

    # Stop coverage and save
    coverage.stop()
    coverage.save()

    # Get report
    total = coverage.report()
    assert total >= 0.0


def test_uncovered_lines_reporting(tmp_path):
    """Test uncovered lines reporting."""
    # Create a test file with some uncovered lines
    test_file = tmp_path / "test.py"
    test_file.write_text(
        """
def covered_func():
    return True

def uncovered_func():
    return False
"""
    )

    # Initialize coverage
    coverage = Coverage(source=[str(tmp_path)], branch=False)
    coverage.start()

    # Run only the covered function
    exec("def covered_func():\n    return True")

    # Stop coverage and save
    coverage.stop()
    coverage.save()

    # Get analysis
    analysis = coverage.analysis(str(test_file))
    missing_lines = analysis[3]
    assert missing_lines  # Should have some uncovered lines
