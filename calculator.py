"""
calculator.py - a four-function calculator, built one feature branch at a time.

Each of the four math functions below starts as a STUB: a placeholder
that raises NotImplementedError until its feature branch fills it in.

    feature/add       builds add()        (Lab 02)
    feature/subtract  builds subtract()   (Lab 02)
    feature/multiply  builds multiply()   (Lab 03)
    feature/divide    builds divide()     (Lab 03)

calculate() at the bottom is already finished. It looks up an operator
like "+" and calls the matching function, so it only works once the
features it needs have been merged into dev.

Every function has TYPE HINTS (a: float, -> float) and a DOCSTRING (the
triple-quoted text under the def line). Python doesn't enforce the type
hints - they're notes for people and tools - but they say what each
function expects and gives back.
"""

from typing import Callable


# ---------------------------------------------------------------------
# Feature 1 - add (built on the feature/add branch)
# ---------------------------------------------------------------------
def add(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum, a + b.
    """
    raise NotImplementedError("add() is built on the feature/add branch")


# ---------------------------------------------------------------------
# Feature 2 - subtract (built on the feature/subtract branch)
# ---------------------------------------------------------------------
def subtract(a: float, b: float) -> float:
    """
    Subtract the second number from the first.

    Args:
        a: The number to subtract from.
        b: The number to take away.

    Returns:
        The difference, a - b. Order matters: subtract(5, 2) is 3,
        but subtract(2, 5) is -3.
    """
    raise NotImplementedError("subtract() is built on the feature/subtract branch")


# ---------------------------------------------------------------------
# Feature 3 - multiply (built on the feature/multiply branch)
# ---------------------------------------------------------------------
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product, a * b. Two negatives make a positive.
    """
    raise NotImplementedError("multiply() is built on the feature/multiply branch")


# ---------------------------------------------------------------------
# Feature 4 - divide (built on the feature/divide branch)
# ---------------------------------------------------------------------
def divide(a: float, b: float) -> float:
    """
    Divide the first number by the second.

    Args:
        a: The number being divided (the numerator).
        b: The number to divide by (the denominator).

    Returns:
        The quotient, a / b. Always a float: divide(7, 2) is 3.5.

    Raises:
        ZeroDivisionError: If b is 0. This is a TEAM DECISION, and
            tests/test_divide.py checks it. Don't change it to return
            something "friendlier" without talking to the team first.
    """
    raise NotImplementedError("divide() is built on the feature/divide branch")


# ---------------------------------------------------------------------
# calculate - already finished. It ties the four features together.
# ---------------------------------------------------------------------

# Each operator symbol maps to the function that does that operation.
# Callable[[float, float], float] is the type hint for "a function that
# takes two floats and gives back a float".
OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(op: str, a: float, b: float) -> float:
    """
    Do one calculation, chosen by its operator symbol.

    Args:
        op: One of "+", "-", "*", or "/".
        a: The first number.
        b: The second number.

    Returns:
        The result of applying the operator to a and b.

    Raises:
        ValueError: If op isn't one of the four operators.
    """
    # Check the operator first, so a typo gets a clear message
    # instead of a confusing KeyError.
    if op not in OPERATIONS:
        raise ValueError(f"unknown operator: {op!r} (use +, -, *, or /)")
    # Look up the function for this operator, then call it.
    operation = OPERATIONS[op]
    return operation(a, b)
