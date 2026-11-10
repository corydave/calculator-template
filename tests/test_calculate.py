"""
Integration tests for calculate().

calculate() doesn't do any math itself. It hands the work to add,
subtract, multiply, or divide. A test of calculate() is an INTEGRATION
test: it checks that the pieces work TOGETHER, so it only makes sense
on dev, after the features have been merged in.

You write these on dev in Lab 04. Each test below is a STUB:
pytest.skip(...) means "don't run this yet". Replace each pytest.skip(...)
line with the real check.
"""

import pytest

from calculator import calculate


def test_calculate_add() -> None:
    """calculate("+", 2, 3) is 5."""
    pytest.skip("Lab 04: write this test")


def test_calculate_subtract() -> None:
    """calculate("-", 5, 2) is 3."""
    pytest.skip("Lab 04: write this test")


def test_calculate_multiply() -> None:
    """calculate("*", 3, 4) is 12."""
    pytest.skip("Lab 04: write this test")


# divide() isn't in the first release, so this test stays skipped until
# Lab 05. A reason= shows up in pytest's report, so nobody wonders why.
@pytest.mark.skip(reason="divide ships in v1.1.0 - write this in Lab 05")
def test_calculate_divide() -> None:
    """calculate("/", 7, 2) is 3.5."""
    pytest.skip("Lab 05: write this test")


def test_calculate_unknown_operator() -> None:
    """An operator that isn't +, -, *, or / raises ValueError."""
    pytest.skip("Lab 04: write this test")


def test_calculate_chain() -> None:
    """One result feeds the next: (2 * 3) + 4 is 10."""
    pytest.skip("Lab 04: write this test")
