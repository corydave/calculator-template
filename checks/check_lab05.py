"""
check_lab05.py - checks for Lab 05: The Divide Dispute.

Run it from the top folder of your calculator repo:
    python checks/check_lab05.py
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repocheck import (CheckFailed, branch_exists, contains, export, need_annotated_tag,  # noqa: E402
                       need_branch, no_conflict_markers, run_checks, run_pytest)


def check_divide_merged() -> None:
    """feature/divide is merged into dev"""
    need_branch("feature/divide")
    if not contains("feature/divide", "dev"):
        raise CheckFailed("feature/divide isn't merged into dev yet. On dev, run: "
                          "git merge feature/divide -m \"Merge feature/divide into dev\"")


def check_teammate_merged() -> None:
    """the teammate's friendly-divide branch exists, started from v1.0.0, and is merged into dev"""
    if not branch_exists("friendly-divide"):
        raise CheckFailed("There's no friendly-divide branch. Make it from the release: "
                          "git switch -c friendly-divide v1.0.0  (Lab 05 Step 2)")
    if not contains("v1.0.0", "friendly-divide"):
        raise CheckFailed("friendly-divide should start from v1.0.0. Delete it and start again: "
                          "git branch -D friendly-divide, then git switch -c friendly-divide v1.0.0")
    if not contains("friendly-divide", "dev"):
        raise CheckFailed("friendly-divide isn't merged into dev yet (Lab 05 Step 3).")


def check_no_markers() -> None:
    """no conflict markers were left behind on dev"""
    no_conflict_markers("dev")


def check_team_decision() -> None:
    """on dev, divide(1, 0) still raises ZeroDivisionError - the team's decision won"""
    folder = export("dev")
    probe = ("from calculator import divide\n"
             "try:\n    print(divide(1, 0))\nexcept ZeroDivisionError:\n    print('raised')\n")
    result = subprocess.run([sys.executable, "-c", probe], cwd=folder, capture_output=True, text=True)
    answer = (result.stdout or result.stderr).strip().splitlines()[-1:] or ["nothing"]
    if answer[0] != "raised":
        raise CheckFailed(f"On dev, divide(1, 0) gives {answer[0]} instead of raising ZeroDivisionError. "
                          "The teammate's side won the conflict. Put the team's version back, run the "
                          "tests, and commit.")


def check_dev_tests() -> None:
    """every test on dev passes, and nothing is skipped - including calculate's divide test"""
    folder = export("dev")
    result = run_pytest(folder)
    failed = result.names("failed") + result.names("error")
    if result.crashed or failed:
        short = ", ".join(n.split("::")[-1] for n in failed) or "pytest couldn't run"
        raise CheckFailed(f"These tests fail on dev: {short}. CI would show a red X.")
    skipped = result.names("skipped")
    if skipped:
        short = ", ".join(n.split("::")[-1] for n in skipped)
        raise CheckFailed(f"These tests are still skipped on dev: {short}. In Lab 05, remove the "
                          "@pytest.mark.skip line above test_calculate_divide and write the test.")
    if not any("calculate" in n and "divide" in n for n in result.names("passed")):
        raise CheckFailed("There's no passing integration test for divide in tests/test_calculate.py.")


def check_tag() -> None:
    """there's an annotated tag v1.1.0 on main, built on top of v1.0.0"""
    need_annotated_tag("v1.1.0", "main")
    if not contains("v1.1.0", "main"):
        raise CheckFailed("v1.1.0 isn't on main. Switch to main, merge dev, and tag there.")
    if not contains("v1.0.0", "v1.1.0"):
        raise CheckFailed("v1.1.0 should build on v1.0.0 - its history should include the first release.")


def check_release_contents() -> None:
    """v1.1.0 includes divide, the resolved conflict, and passes every test"""
    need_annotated_tag("v1.1.0", "main")
    for ref in ["feature/divide", "friendly-divide"]:
        if branch_exists(ref) and not contains(ref, "v1.1.0"):
            raise CheckFailed(f"v1.1.0 doesn't include {ref}. Merge dev into main, then tag.")
    if not contains("v1.1.0", "dev"):
        raise CheckFailed("v1.1.0 has commits that dev doesn't, so something was committed on main. "
                          "Releases come from dev. Ask your instructor for help moving the tag.")
    no_conflict_markers("v1.1.0")
    result = run_pytest(export("v1.1.0"))
    if result.crashed or result.count("failed") or result.count("error") or result.count("skipped"):
        raise CheckFailed("Not every test passes in v1.1.0. Fix dev first, then merge and tag again.")


if __name__ == "__main__":
    run_checks("Lab 05 - The Divide Dispute",
               [check_divide_merged, check_teammate_merged, check_no_markers, check_team_decision,
                check_dev_tests, check_tag, check_release_contents])
