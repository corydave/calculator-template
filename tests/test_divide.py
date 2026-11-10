"""
Unit tests for divide().

You write these on the feature/divide branch in Lab 03.

Each test below is a STUB: pytest.skip(...) means "don't run this yet".
Replace each pytest.skip(...) line with the real check. The docstring
under each test says what to check.
"""

import pytest

from calculator import divide


def test_divide_evenly() -> None:
    """10 / 2 is 5."""
    pytest.skip("Lab 03: write this test")


def test_divide_gives_a_float() -> None:
    """7 / 2 is 3.5, not 3."""
    pytest.skip("Lab 03: write this test")


def test_divide_zero_by_a_number() -> None:
    """0 / 5 is 0."""
    pytest.skip("Lab 03: write this test")


def test_divide_by_zero_raises() -> None:
    """Dividing by 0 raises ZeroDivisionError - the team's decision.

    Use pytest.raises (notebook Section 5).
    """
    pytest.skip("Lab 03: write this test")
