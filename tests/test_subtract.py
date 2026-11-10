"""
Unit tests for subtract().

You write these on the feature/subtract branch in Lab 02.

Each test below is a STUB: pytest.skip(...) means "don't run this yet".
Replace each pytest.skip(...) line with the real check. The docstring
under each test says what to check.
"""

import pytest

from calculator import subtract


def test_subtract_two_positives() -> None:
    """5 - 2 is 3."""
    pytest.skip("Lab 02: write this test")


def test_subtract_order_matters() -> None:
    """2 - 5 is -3 (not 3: the order of the numbers matters)."""
    pytest.skip("Lab 02: write this test")


def test_subtract_a_negative() -> None:
    """-4 - -6 is 2 (taking away a negative adds)."""
    pytest.skip("Lab 02: write this test")


def test_subtract_floats() -> None:
    """0.3 - 0.1 is 0.2 - compare with pytest.approx."""
    pytest.skip("Lab 02: write this test")
