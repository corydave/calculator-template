"""
check_lab01.py - checks for Lab 01: Your Calculator Repo.

Run it from the top folder of your calculator repo:
    python checks/check_lab01.py
"""

import os
import sys

# Let this file find repocheck.py, which sits beside it in checks/.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repocheck import CheckFailed, export, file_at, need_branch, run_checks, run_pytest  # noqa: E402

FEATURES = ["add", "subtract", "multiply", "divide"]


def check_main() -> None:
    """there's a main branch with the calculator template on it"""
    need_branch("main")
    if file_at("main", "calculator.py") is None:
        raise CheckFailed("main doesn't have calculator.py. Did you make the repo from the "
                          "calculator template? (Lab 01, Step 1)")


def check_dev() -> None:
    """there's a dev branch"""
    need_branch("dev")


def check_features() -> None:
    """all four feature branches exist: feature/add, feature/subtract, feature/multiply, feature/divide"""
    for name in FEATURES:
        need_branch(f"feature/{name}")


def check_tests_run() -> None:
    """pytest runs on dev, and nothing fails"""
    need_branch("dev")
    folder = export("dev")
    result = run_pytest(folder)
    if result.crashed:
        raise CheckFailed("pytest couldn't run on dev. Try  python -m pytest  yourself to see why.")
    if result.count("failed") or result.count("error"):
        raise CheckFailed("Some tests fail on dev. Run  python -m pytest -v  while on dev to see which.")


if __name__ == "__main__":
    run_checks("Lab 01 - Your Calculator Repo",
               [check_main, check_dev, check_features, check_tests_run])
