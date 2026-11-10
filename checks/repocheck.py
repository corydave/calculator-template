"""
repocheck.py - the engine behind this repository's lab checkers.

Chapter 08's labs happen in a real git repository, so these checkers
look at your repo the way a teammate would:

  - Which BRANCHES and TAGS exist, and how they connect.
  - What each branch's latest COMMIT holds. The checkers read your
    commits, not the files open in your editor, so commit your work
    before you check it.
  - Whether your TESTS pass, and whether they would catch a bug. For
    that, a checker swaps in a deliberately broken version of a
    function (a "mutant") and runs your tests again. Good tests FAIL
    on the broken version.

You never need to edit this file. Each check_labNN.py uses it.
"""

from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ElementTree

TICK = "✓"     # ✓
CROSS = "✗"    # ✗

# How long one pytest run may take before we give up on it, in seconds.
PYTEST_TIME_LIMIT = 60

# The line each stub starts with, so we can tell an unbuilt function.
STUB_TEXT = 'raise NotImplementedError("{name}() is built on'


class CheckFailed(Exception):
    """Raised by a check, with a hint for the learner."""


# ── git helpers ──────────────────────────────────────────────────────────────

def git(*args: str) -> tuple[int, str]:
    """Run one git command in the current folder; return (exit code, output)."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def ref_exists(ref: str) -> bool:
    """True if a branch, tag, or commit called `ref` exists."""
    code, _ = git("rev-parse", "--verify", "--quiet", ref + "^{commit}")
    return code == 0


def branch_exists(name: str) -> bool:
    """True if a LOCAL branch called `name` exists."""
    code, _ = git("show-ref", "--verify", "--quiet", "refs/heads/" + name)
    return code == 0


def tag_exists(name: str) -> bool:
    code, _ = git("show-ref", "--verify", "--quiet", "refs/tags/" + name)
    return code == 0


def contains(older: str, newer: str) -> bool:
    """True if commit `older` is in `newer`'s history (newer has its work)."""
    code, _ = git("merge-base", "--is-ancestor", older, newer)
    return code == 0


def commits_between(base: str, tip: str) -> int:
    """How many commits `tip` has that `base` doesn't."""
    code, out = git("rev-list", "--count", f"{base}..{tip}")
    return int(out) if code == 0 else 0


def all_branches() -> list[str]:
    code, out = git("branch", "--format=%(refname:short)")
    return out.split() if code == 0 else []


def near_misses(name: str) -> list[str]:
    """Existing branches that look like a misspelling of `name`."""
    squash = lambda s: re.sub(r"[^a-z]", "", s.lower())
    return [b for b in all_branches() if b != name and squash(b) == squash(name)]


def file_at(ref: str, path: str) -> str | None:
    """The text of `path` in commit `ref`, or None if it isn't there."""
    code, out = git("show", f"{ref}:{path}")
    return out if code == 0 else None


# ── exporting a commit so it can be tested ───────────────────────────────────

def export(ref: str) -> str:
    """
    Copy the files of commit `ref` into a fresh temporary folder, and
    return the folder's path. Your working folder is never touched.
    """
    folder = tempfile.mkdtemp(prefix="check-")
    data = subprocess.run(["git", "archive", "--format=tar", ref], capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        # Only extract ordinary files and folders inside our temp folder.
        safe = [m for m in archive.getmembers()
                if (m.isfile() or m.isdir()) and not m.name.startswith(("/", ".."))
                and ".." not in m.name.split("/")]
        archive.extractall(folder, members=safe)
    return folder


def add_mutant(folder: str, code: str) -> None:
    """
    Break one function on purpose, by adding a new definition to the END
    of calculator.py. A later def replaces an earlier one, so your tests
    get the broken version whichever way you wrote yours.
    """
    with open(os.path.join(folder, "calculator.py"), "a", encoding="utf-8") as fh:
        fh.write("\n\n# --- added by the checker: a deliberately broken version ---\n")
        fh.write(code.strip() + "\n")


# ── running pytest ───────────────────────────────────────────────────────────

class PytestResult:
    """What happened when pytest ran: each test's outcome, and the summary."""

    def __init__(self, outcomes: dict[str, str], output: str, crashed: bool):
        self.outcomes = outcomes      # test name -> "passed", "failed", "skipped", "error"
        self.output = output          # everything pytest printed
        self.crashed = crashed        # True if pytest couldn't run at all

    def count(self, outcome: str, file: str = "") -> int:
        return sum(1 for name, o in self.outcomes.items() if o == outcome and file in name)

    def names(self, outcome: str, file: str = "") -> list[str]:
        return [name for name, o in self.outcomes.items() if o == outcome and file in name]


def run_pytest(folder: str, *paths: str) -> PytestResult:
    """Run pytest on `paths` inside `folder`, and collect every test's outcome."""
    report = os.path.join(folder, ".report.xml")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={report}", *paths],
            cwd=folder, capture_output=True, text=True, env=env, timeout=PYTEST_TIME_LIMIT)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return PytestResult({}, "pytest took longer than a minute and was stopped.", True)
    outcomes: dict[str, str] = {}
    if os.path.exists(report):
        for case in ElementTree.parse(report).getroot().iter("testcase"):
            name = case.get("classname", "").replace(".", "/") + ".py::" + case.get("name", "")
            outcome = "passed"
            for child in case:
                if child.tag in ("failure", "error", "skipped"):
                    outcome = {"failure": "failed", "error": "error", "skipped": "skipped"}[child.tag]
            outcomes[name] = outcome
    crashed = not outcomes and "no tests ran" not in output
    return PytestResult(outcomes, output, crashed)


def pytest_installed() -> bool:
    code = subprocess.run([sys.executable, "-c", "import pytest"], capture_output=True).returncode
    return code == 0


# ── reusable checks ──────────────────────────────────────────────────────────

def need_branch(name: str) -> None:
    """Fail with a helpful hint if branch `name` doesn't exist."""
    if branch_exists(name):
        return
    misses = near_misses(name)
    if misses:
        raise CheckFailed(f"There's no branch called {name}, but there is {misses[0]}. Branch names "
                          f"must match exactly. Rename it with: git branch -m {misses[0]} {name}")
    if name == "main":
        raise CheckFailed("There's no branch called main. Did you make the repository from the "
                          "calculator template? (Lab 01, Step 1)")
    if name == "dev":
        raise CheckFailed("There's no branch called dev yet. Make it from main with: git switch -c dev main")
    raise CheckFailed(f"There's no branch called {name} yet. Make it with: git branch {name} dev")


def need_built(branch: str, name: str, lab: str) -> str:
    """
    Fail unless `branch` has commits of its own, and its latest commit has
    a working (not stub) version of function `name`. Returns the exported
    folder for further testing.
    """
    need_branch(branch)
    code = file_at(branch, "calculator.py") or ""
    if STUB_TEXT.format(name=name) in code:
        if commits_between("dev", branch) == 0:
            raise CheckFailed(f"{branch} has no commits of its own yet. Switch to it (git switch {branch}), "
                              f"do the {lab} steps, then commit: git add . and git commit -m \"...\"")
        raise CheckFailed(f"In the latest commit on {branch}, {name}() is still the stub that raises "
                          "NotImplementedError. Paste in the feature code from the lab, then commit it.")
    return export(branch)


def only_own_stub(branch: str, mine: str, features: list[str]) -> None:
    """A feature branch should build ONLY its own function, so merges stay clean."""
    code = file_at(branch, "calculator.py") or ""
    for other in features:
        if other == mine:
            continue
        # The other stubs must still be there, unchanged, unless that feature is
        # already merged in (then this branch may have it from dev).
        if STUB_TEXT.format(name=other) not in code and not contains(f"feature/{other}", branch):
            raise CheckFailed(f"{branch} also changed {other}(). Each feature branch should build only "
                              f"its own function - otherwise merging the branches into dev will conflict. "
                              f"Put {other}() back to its stub on this branch (copy it from dev).")


def tests_all_pass(folder: str, path: str, at_least: int, what: str) -> PytestResult:
    """Run one test file; fail unless every test passes and none is skipped."""
    result = run_pytest(folder, path)
    if result.crashed:
        tail = "\n      ".join(result.output.strip().splitlines()[-6:])
        raise CheckFailed(f"pytest couldn't run {path}. The end of its output was:\n      {tail}")
    skipped = result.names("skipped", path)
    failed = result.names("failed", path) + result.names("error", path)
    if failed:
        short = ", ".join(n.split("::")[-1] for n in failed)
        raise CheckFailed(f"These tests in {path} fail: {short}. Run  python -m pytest {path} -v  "
                          "to see why. (Is the expected value right? Floats need pytest.approx.)")
    if skipped:
        short = ", ".join(n.split("::")[-1] for n in skipped)
        raise CheckFailed(f"These tests in {path} are still skipped: {short}. Replace each "
                          "pytest.skip(...) line with the real check.")
    passed = result.count("passed", path)
    if passed < at_least:
        raise CheckFailed(f"Only {passed} test(s) in {path} ran. {what}")
    return result


def tests_catch(folder_maker, path: str, mutant: str, bug: str, hint: str) -> None:
    """Fail if the tests in `path` still PASS when `mutant` replaces a function."""
    folder = folder_maker()
    try:
        add_mutant(folder, mutant)
        result = run_pytest(folder, path)
        if result.crashed:
            return     # the broken code crashed the test run: that counts as caught
        if result.count("failed", path) + result.count("error", path) == 0:
            raise CheckFailed(f"Your tests still pass when {bug}. {hint}")
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def no_conflict_markers(ref: str) -> None:
    code, out = git("grep", "-n", "-E", "^(<<<<<<<|>>>>>>>|=======$)", ref, "--", "*.py")
    if code == 0 and out:
        first = out.splitlines()[0].split(":", 1)[1]
        raise CheckFailed(f"Conflict markers are still in a commit on {ref} ({first.split(':')[0]}). "
                          "Delete the <<<<<<<, =======, and >>>>>>> lines, keep the right code, "
                          "then git add the file and commit.")


def need_annotated_tag(name: str, on: str) -> None:
    if not tag_exists(name):
        raise CheckFailed(f"There's no tag called {name} yet. On {on}, run: "
                          f"git tag -a {name} -m \"Release {name[1:]}\"")
    code, kind = git("cat-file", "-t", name)
    if kind != "tag":
        raise CheckFailed(f"{name} is a lightweight tag. Releases get ANNOTATED tags, with a message. "
                          f"Replace it: git tag -d {name}, then git tag -a {name} -m \"Release {name[1:]}\" "
                          f"on the right commit.")


# ── the runner ───────────────────────────────────────────────────────────────

def run_checks(title: str, checks: list) -> None:
    """Run each check function in order and print a tick or a cross for each."""
    print(f"Checking {title}\n")
    code, _ = git("rev-parse", "--is-inside-work-tree")
    if code != 0:
        print("  This folder isn't a git repository. Run the checker from the top folder of your")
        print("  calculator repo, like this:  python checks/check_lab01.py")
        sys.exit(1)
    if not pytest_installed():
        print("  pytest isn't installed yet. Run this first:  pip install -r requirements.txt")
        sys.exit(1)
    _, status = git("status", "--porcelain", "--untracked-files=no")
    if status:
        print("  Note: you have changes that aren't committed yet. The checks read your COMMITS,")
        print("  so commit first (git add . then git commit -m \"...\") if you want them checked.\n")

    passed = 0
    for check in checks:
        description = (check.__doc__ or check.__name__).strip().splitlines()[0]
        try:
            check()
        except CheckFailed as problem:
            print(f"  {CROSS} {description}")
            print(f"      {problem}")
        except Exception as problem:          # a surprise: report it, don't crash
            print(f"  {CROSS} {description}")
            print(f"      The check itself hit an error: {type(problem).__name__}: {problem}")
        else:
            print(f"  {TICK} {description}")
            passed += 1
    print()
    if passed == len(checks):
        print(f"All {len(checks)} checks passed. Nice work!")
        sys.exit(0)
    print(f"{passed} of {len(checks)} checks passed. Each {CROSS} has a hint underneath it.")
    print(f"Start with the FIRST {CROSS}: one mistake often causes several, so fixing")
    print("it may clear the others too. Then run the checker again.")
    sys.exit(1)
