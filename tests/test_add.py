"""
Unit tests for add().

You write these on the feature/add branch in Lab 02.

Each test below is a STUB. The line pytest.skip(...) tells pytest
"don't run this one yet", so it shows up as an "s" (skipped) instead of
a failure. To write a test, replace its pytest.skip(...) line with the
real check. The docstring under each test says what to check.
"""

import pytest

from calculator import add


def test_add_two_positives() -> None:
    """2 + 3 is 5."""
    pytest.skip("Lab 02: write this test")


def test_add_negatives() -> None:
    """-4 + -6 is -10."""
    pytest.skip("Lab 02: write this test")


def test_add_zero() -> None:
    """Adding 0 changes nothing: 7 + 0 is 7."""
    pytest.skip("Lab 02: write this test")


def test_add_floats() -> None:
    """0.1 + 0.2 is 0.3 - compare with pytest.approx (notebook Section 4)."""
    pytest.skip("Lab 02: write this test")
