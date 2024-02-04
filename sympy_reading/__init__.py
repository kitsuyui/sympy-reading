# TODO: Support more complex expressions
# TODO: Support other languages
from typing import Union

from sympy import Eq, Expr
import sympy


DIGIT_READING = {
    "0": "ぜろ",
    "1": "いち",
    "2": "に",
    "3": "さん",
    "4": "よん",
    "5": "ご",
    "6": "ろく",
    "7": "なな",
    "8": "はち",
    "9": "きゅう",
}

SCALE_READING_1 = [
    "じゅう",
    "ひゃく",
    "せん",
]

SCALE_READING_2 = [
    "",
    "まん",
    "おく",
    "ちょう",
    "けい",
    "がい",
]

OPERATOR_READING = {
    sympy.core.add.Add: "たす",
    sympy.core.mul.Mul: "かける",
}


def digit_to_japanese(digit_str: str) -> str:
    """
    Converts a digit string to its Japanese reading.
    """
    return DIGIT_READING[digit_str]


def scale_reading_1_japanese(digit_str: str, nth: int) -> str:
    scale = SCALE_READING_1[nth]

    if digit_str == "1":
        reading = ""
    else:
        reading = digit_to_japanese(digit_str)

    return f"{reading}{scale}"


def digits_to_japanese(digits_str: str, top: bool = True) -> str:
    """
    Converts a digit string to its Japanese reading.
    """
    if len(digits_str) == 1:
        if not top and digits_str[0] == "0":
            return ""
        return digit_to_japanese(digits_str)

    if len(digits_str) <= 4:
        if digits_str[0] == "0":
            return digits_to_japanese(digits_str[1:])

        reading = scale_reading_1_japanese(digits_str[0], len(digits_str) - 2)
        return f"{reading}{digits_to_japanese(digits_str[1:], top=False)}"

    #     return scale_reading_1_japanese(digits_str)

    # Split the digits into groups of 4 from right to left
    digits_array = []
    for i in range(0, len(digits_str), 4):
        cut = digits_str[-(i + 4) : len(digits_str) - i]
        if cut:
            digits_array.insert(0, cut)

    readings = []
    for i, digits in enumerate(digits_array):
        scale_reading = SCALE_READING_2[len(digits_array) - i - 1]
        reading = f"{digits_to_japanese(digits)}{scale_reading}"
        readings.append(reading)

    return "".join(readings)


# Convert equation components to their Japanese readings
def component_to_reading(component: Expr) -> str:
    for op_class, reading in OPERATOR_READING.items():
        if component is op_class:
            return reading
    if component.is_integer:
        return digits_to_japanese(str(component))
    raise NotImplementedError(
        f"Unrecognized expr: {component}, type: {type(component)}"
    )


def expr_to_reading(expr: Expr) -> str:
    """
    Converts a SymPy expression into its Japanese reading, including support for multi-digit numbers.
    """

    # Create the Japanese reading for the expression
    if expr.args:  # TODO: Currently support only infix notation
        left = component_to_reading(expr.args[0])
        right = component_to_reading(expr.args[1])
        op = component_to_reading(expr.func)
        return f"{left} {op} {right}"

    if expr.is_integer:
        return component_to_reading(expr)

    raise NotImplementedError(f"Unrecognized expr: {expr}, type: {type(expr)}")


def equation_to_reading(eq: Eq) -> str:
    """
    Converts a SymPy equation into its Japanese reading, including support for multi-digit numbers.
    """
    # Extract the left and right sides of the equation
    # Create the Japanese reading for both sides
    left_reading = expr_to_reading(eq.lhs)
    right_reading = expr_to_reading(eq.rhs)
    # Combine both readings with the equals sign
    full_reading = f"{left_reading} いこーる {right_reading}"
    return full_reading


def to_reading(expr: Union[Eq, Expr]) -> str:
    if isinstance(expr, Eq):
        return equation_to_reading(expr)
    if isinstance(expr, Expr):
        return expr_to_reading(expr)
    raise NotImplementedError(f"Unrecognized expr: {expr}, type: {type(expr)}")
