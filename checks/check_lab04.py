"""
check_lab04.py - checks for Lab 04: Merge and Release.

Run it from the top folder of your calculator repo:
    python checks/check_lab04.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repocheck import (CheckFailed, contains, export, file_at, need_annotated_tag,  # noqa: E402
                       need_branch, run_checks, run_pytest, tests_all_pass, tests_catch)

RELEASED = ["add", "subtract", "multiply"]
WORKFLOW = ".github/workflows/tests.yml"


def check_workflow() -> None:
    """dev has the CI workflow, set to run pytest on pushes to dev"""
    need_branch("dev")
    text = file_at("dev", WORKFLOW)
    if text is None:
        raise CheckFailed(f"dev doesn't have {WORKFLOW}. Create the file (folders and all) from "
                          "Lab 04 Step 1, then commit it on dev.")
    # Ignore comments, then look for the pieces the workflow needs.
    code = "\n".join(line.split("#")[0] for line in text.splitlines())
    missing = [what for what, pattern in [
        ("an  on:  section", r"^on:"),
        ("a  push:  trigger", r"push:"),
        ("the dev branch in its triggers", r"\bdev\b"),
        ("a step that runs pytest", r"pytest"),
        ("the checkout step", r"actions/checkout"),
    ] if not re.search(pattern, code, re.M)]
    if missing:
        raise CheckFailed(f"{WORKFLOW} is missing {missing[0]}. Compare it with Lab 04 Step 1.")


def check_features_in_dev() -> None:
    """feature/add, feature/subtract, and feature/multiply are merged into dev"""
    need_branch("dev")
    for name in RELEASED:
        need_branch(f"feature/{name}")
        if not contains(f"feature/{name}", "dev"):
            raise CheckFailed(f"feature/{name} isn't merged into dev yet. On dev, run: "
                              f"git merge feature/{name} -m \"Merge feature/{name} into dev\"")


def check_integration_tests() -> None:
    """tests/test_calculate.py on dev runs and passes (only the divide test stays skipped)"""
    folder = export("dev")
    result = run_pytest(folder, "tests/test_calculate.py")
    failed = result.names("failed") + result.names("error")
    if result.crashed or failed:
        raise CheckFailed("Some integration tests fail on dev. Run  python -m pytest "
                          "tests/test_calculate.py -v  while on dev to see which.")
    skipped = [n for n in result.names("skipped") if "divide" not in n]
    if skipped:
        short = ", ".join(n.split("::")[-1] for n in skipped)
        raise CheckFailed(f"These integration tests are still skipped: {short}. Only the divide "
                          "test should wait for Lab 05.")
    if result.count("passed") < 5:
        raise CheckFailed("Write all five: add, subtract, multiply, unknown operator, and chain.")


def check_integration_catches_bugs() -> None:
    """your integration tests catch a mixed-up operator table and a silent unknown operator"""
    maker = lambda: export("dev")
    path = "tests/test_calculate.py"
    tests_catch(maker, path, 'OPERATIONS["+"], OPERATIONS["-"] = OPERATIONS["-"], OPERATIONS["+"]',
                "calculate() mixes up + and -", "Check your add and subtract tests use calculate().")
    tests_catch(maker, path,
                "def calculate(op, a, b):\n    return OPERATIONS[op](a, b) if op in OPERATIONS else 0",
                "calculate() quietly returns 0 for an unknown operator",
                "Check the unknown-operator test: use  with pytest.raises(ValueError):")


def check_tag() -> None:
    """there's an annotated tag v1.0.0"""
    need_annotated_tag("v1.0.0", "main")


def check_release_contents() -> None:
    """v1.0.0 has add, subtract, and multiply - but not divide"""
    need_annotated_tag("v1.0.0", "main")
    for name in RELEASED:
        if not contains(f"feature/{name}", "v1.0.0"):
            raise CheckFailed(f"v1.0.0 doesn't include feature/{name}. Merge it into dev, then dev into "
                              "main. Then move the tag: delete it with  git tag -d v1.0.0  (and, if you "
                              "pushed it,  git push origin :refs/tags/v1.0.0 ), and tag main again.")
    if contains("feature/divide", "v1.0.0"):
        raise CheckFailed("v1.0.0 includes feature/divide, but divide is deferred to v1.1.0. Ask your "
                          "instructor for help untangling this one: the release needs to be rebuilt "
                          "without divide.")


def check_release_came_through_dev() -> None:
    """the release reached main through dev (features never merged straight into main)"""
    need_annotated_tag("v1.0.0", "main")
    if not contains("v1.0.0", "main"):
        raise CheckFailed("v1.0.0 isn't on main. Switch to main, merge dev, and tag there.")
    if not contains("v1.0.0", "dev"):
        raise CheckFailed("v1.0.0 has commits that dev doesn't. Features merge into dev FIRST, then "
                          "dev merges into main - never a feature branch straight into main.")
    if not contains("main", "dev"):
        raise CheckFailed("main has a commit that dev doesn't - probably something committed while you "
                          "were on main (your notes?). Nobody commits to main. Bring it into dev so the "
                          "next release can fast-forward:  git switch dev  then  git merge main")


def check_release_tests() -> None:
    """every test in the v1.0.0 release passes (the divide stubs may stay skipped)"""
    need_annotated_tag("v1.0.0", "main")
    folder = export("v1.0.0")
    result = run_pytest(folder)
    if result.crashed or result.count("failed") or result.count("error"):
        raise CheckFailed("Some tests fail in v1.0.0. A release only gets tagged when everything passes.")
    for name in RELEASED:
        tests_all_pass(folder, f"tests/test_{name}.py", 4, "")


if __name__ == "__main__":
    run_checks("Lab 04 - Merge and Release",
               [check_workflow, check_features_in_dev, check_integration_tests,
                check_integration_catches_bugs, check_tag, check_release_contents,
                check_release_came_through_dev, check_release_tests])
