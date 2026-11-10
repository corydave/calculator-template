# Calculator

A four-function calculator, built by a (pretend) team, one feature branch
at a time. It's the project for CSC 200 Chapter 08: Git branching and
testing with pytest.

## What's in here

```text
calculator/
├── calculator.py        the calculator: add, subtract, multiply, divide, calculate
├── tests/               the tests - pytest runs everything in here
│   ├── test_add.py
│   ├── test_subtract.py
│   ├── test_multiply.py
│   ├── test_divide.py
│   └── test_calculate.py    integration tests (the features working together)
├── checks/              the lab checkers (you don't edit these)
├── pytest.ini           pytest's settings
├── requirements.txt     the packages this project needs (just pytest)
└── .gitignore           files git should never track
```

In Lab 04 you'll add one more file, `.github/workflows/tests.yml`, which
tells GitHub to run the tests every time someone pushes to `dev`.

## The branches

| Branch | What it holds |
|---|---|
| `main` | Released versions only. Every commit here has been tested and tagged. |
| `dev` | The next release, being put together. Features merge in here first. |
| `feature/add`, `feature/subtract`, `feature/multiply`, `feature/divide` | One feature each. Each merges into `dev`, never straight into `main`. |

## Running the tests

```bash
pip install -r requirements.txt     # once, to install pytest
python -m pytest                    # run every test
python -m pytest -v                 # ...with one line per test
python -m pytest tests/test_add.py  # just one file
```

## Checking a lab

From this top folder:

```bash
python checks/check_lab01.py
```

The checkers read your **commits**, so commit your work before you check it.
