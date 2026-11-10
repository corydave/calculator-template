"""
check_lab03.py - checks for Lab 03: Edge Cases.

Run it from the top folder of your calculator repo:
    python checks/check_lab03.py

The checker reads your feature/multiply and feature/divide branches,
runs your tests, and runs them again against deliberately broken
versions of multiply() and divide().
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repocheck import (CheckFailed, need_built, only_own_stub, run_checks,  # noqa: E402
                       tests_all_pass, tests_catch)

FEATURES = ["add", "subtract", "multiply", "divide"]


def check_multiply_built() -> None:
    """feature/multiply has a commit that builds multiply()"""
    need_built("feature/multiply", "multiply", "Lab 03")


def check_multiply_alone() -> None:
    """feature/multiply changes only multiply(), so it will merge cleanly"""
    only_own_stub("feature/multiply", "multiply", FEATURES)


def check_multiply_tests_pass() -> None:
    """all of tests/test_multiply.py runs and passes, with all four sign rows"""
    folder = need_built("feature/multiply", "multiply", "Lab 03")
    result = tests_all_pass(folder, "tests/test_multiply.py", 7,
                            "Expect 7: two positives, by zero, four sign rows, and floats.")
    rows = [n for n in result.names("passed") if "[" in n]
    if len(rows) < 4:
        raise CheckFailed(f"The parametrized sign test ran {len(rows)} time(s). It needs four rows: "
                          "(2, 3, 6), (-2, 3, -6), (2, -3, -6), and (-2, -3, 6).")


def check_multiply_catches_bugs() -> None:
    """your multiply() tests catch five kinds of broken multiply()"""
    maker = lambda: need_built("feature/multiply", "multiply", "Lab 03")
    path = "tests/test_multiply.py"
    tests_catch(maker, path, "def multiply(a, b):\n    return a + b",
                "multiply() adds instead", "Check the two-positives test: 3 * 4 should be 12.")
    tests_catch(maker, path, "def multiply(a, b):\n    return a * b if b != 0 else a",
                "multiply() returns a when b is 0", "Check the by-zero test: 9 * 0 should be 0.")
    tests_catch(maker, path, "def multiply(a, b):\n    return abs(a * b)",
                "multiply() never gives a negative answer",
                "Check the mixed-sign rows: -2 * 3 should be -6.")
    tests_catch(maker, path,
                "def multiply(a, b):\n    return -abs(a * b) if (a < 0 or b < 0) else a * b",
                "negative x negative gives a negative",
                "Check the last sign row: -2 * -3 should be 6.")
    tests_catch(maker, path, "def multiply(a, b):\n    return round(a * b)",
                "multiply() rounds to a whole number",
                "Check the floats test: 0.1 * 3 should be about 0.3.")


def check_divide_built() -> None:
    """feature/divide has a commit that builds divide()"""
    need_built("feature/divide", "divide", "Lab 03")


def check_divide_alone() -> None:
    """feature/divide changes only divide(), so it will merge cleanly"""
    only_own_stub("feature/divide", "divide", FEATURES)


def check_divide_tests_pass() -> None:
    """all of tests/test_divide.py runs and passes - nothing skipped"""
    folder = need_built("feature/divide", "divide", "Lab 03")
    tests_all_pass(folder, "tests/test_divide.py", 4,
                   "Write all four: evenly, gives a float, zero by a number, and by zero.")


def check_divide_catches_bugs() -> None:
    """your divide() tests catch four kinds of broken divide(), including the 'friendly' one"""
    maker = lambda: need_built("feature/divide", "divide", "Lab 03")
    path = "tests/test_divide.py"
    tests_catch(maker, path, "def divide(a, b):\n    return a // b",
                "divide() rounds down to a whole number (//)",
                "Check the gives-a-float test: 7 / 2 should be 3.5.")
    tests_catch(maker, path, "def divide(a, b):\n    return b / a if a != 0 else 0.0",
                "divide() divides the wrong way round", "Check the evenly test: 10 / 2 should be 5.")
    tests_catch(maker, path, "def divide(a, b):\n    return float('inf') if b == 0 else a / b",
                "divide(1, 0) returns infinity instead of raising",
                "Check the by-zero test: use  with pytest.raises(ZeroDivisionError):  around divide(1, 0).")
    tests_catch(maker, path, "def divide(a, b):\n    return 0.0 if b == 0 else a / b",
                "divide(1, 0) quietly returns 0",
                "Check the by-zero test: it must expect ZeroDivisionError.")


if __name__ == "__main__":
    run_checks("Lab 03 - Edge Cases",
               [check_multiply_built, check_multiply_alone, check_multiply_tests_pass,
                check_multiply_catches_bugs, check_divide_built, check_divide_alone,
                check_divide_tests_pass, check_divide_catches_bugs])
