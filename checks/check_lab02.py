"""
check_lab02.py - checks for Lab 02: First Tests.

Run it from the top folder of your calculator repo:
    python checks/check_lab02.py

The checker reads your feature/add and feature/subtract branches, runs
your tests, and then runs them again against deliberately broken
versions of add() and subtract(). Good tests FAIL on broken code.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repocheck import need_built, only_own_stub, run_checks, tests_all_pass, tests_catch  # noqa: E402

FEATURES = ["add", "subtract", "multiply", "divide"]


def check_add_built() -> None:
    """feature/add has a commit that builds add()"""
    need_built("feature/add", "add", "Lab 02")


def check_add_alone() -> None:
    """feature/add changes only add(), so it will merge cleanly"""
    only_own_stub("feature/add", "add", FEATURES)


def check_add_tests_pass() -> None:
    """all of tests/test_add.py runs and passes - nothing skipped"""
    folder = need_built("feature/add", "add", "Lab 02")
    tests_all_pass(folder, "tests/test_add.py", 4,
                   "Write all four: two positives, negatives, zero, and floats.")


def check_add_catches_bugs() -> None:
    """your add() tests catch four kinds of broken add()"""
    maker = lambda: need_built("feature/add", "add", "Lab 02")
    path = "tests/test_add.py"
    tests_catch(maker, path, "def add(a, b):\n    return a - b",
                "add() subtracts instead", "Check the two-positives test: 2 + 3 should be 5.")
    tests_catch(maker, path, "def add(a, b):\n    return abs(a) + abs(b)",
                "add() ignores minus signs", "Check the negatives test: -4 + -6 should be -10.")
    tests_catch(maker, path, "def add(a, b):\n    return a + b if b != 0 else 0",
                "add() gives 0 whenever b is 0", "Check the zero test: 7 + 0 should be 7.")
    tests_catch(maker, path, "def add(a, b):\n    return round(a + b)",
                "add() rounds to a whole number", "Check the floats test: 0.1 + 0.2 should be about 0.3.")


def check_subtract_built() -> None:
    """feature/subtract has a commit that builds subtract()"""
    need_built("feature/subtract", "subtract", "Lab 02")


def check_subtract_alone() -> None:
    """feature/subtract changes only subtract(), so it will merge cleanly"""
    only_own_stub("feature/subtract", "subtract", FEATURES)


def check_subtract_tests_pass() -> None:
    """all of tests/test_subtract.py runs and passes - nothing skipped"""
    folder = need_built("feature/subtract", "subtract", "Lab 02")
    tests_all_pass(folder, "tests/test_subtract.py", 4,
                   "Write all four: two positives, order matters, a negative, and floats.")


def check_subtract_catches_bugs() -> None:
    """your subtract() tests catch four kinds of broken subtract()"""
    maker = lambda: need_built("feature/subtract", "subtract", "Lab 02")
    path = "tests/test_subtract.py"
    tests_catch(maker, path, "def subtract(a, b):\n    return a + b",
                "subtract() adds instead", "Check the two-positives test: 5 - 2 should be 3.")
    tests_catch(maker, path, "def subtract(a, b):\n    return abs(a - b)",
                "subtract() never gives a negative answer",
                "Check the order-matters test: 2 - 5 should be -3.")
    tests_catch(maker, path, "def subtract(a, b):\n    return a - abs(b)",
                "subtract() ignores the minus sign on b",
                "Check the a-negative test: -4 - -6 should be 2.")
    tests_catch(maker, path, "def subtract(a, b):\n    return round(a - b)",
                "subtract() rounds to a whole number",
                "Check the floats test: 0.3 - 0.1 should be about 0.2.")


if __name__ == "__main__":
    run_checks("Lab 02 - First Tests",
               [check_add_built, check_add_alone, check_add_tests_pass, check_add_catches_bugs,
                check_subtract_built, check_subtract_alone, check_subtract_tests_pass,
                check_subtract_catches_bugs])
