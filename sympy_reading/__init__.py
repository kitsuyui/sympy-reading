# TODO: Support more complex expressions
# TODO: Support other languages

from types import MappingProxyType

from sympy import Add, Eq, Expr, Integer, Mul

__all__ = ["to_reading"]

DIGIT_READING = MappingProxyType(
    {
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
    },
)

SCALE_READING_1 = (
    "じゅう",
    "ひゃく",
    "せん",
)

SCALE_READING_2 = (
    "",
    "まん",
    "おく",
    "ちょう",
    "けい",
    "がい",
    "じょ",
    "じょう",
    "こう",
    "かん",
    "せい",
    "さい",
    "ごく",
    "ごうがしゃ",
    "あそうぎ",
    "なゆた",
    "ふかしぎ",
    "むりょうたいすう",
)

OPERATOR_READING = MappingProxyType(
    {
        Add: "たす",
        Mul: "かける",
    },
)


def digit_to_japanese(digit_str: str) -> str:
    """
    Converts a digit string to its Japanese reading.
    """
    return DIGIT_READING[digit_str]


def scale_onbin_1(reading: str, nth: int) -> str:
    if nth == 1:
        if reading == "さん":
            return "さんびゃく"
        if reading == "ろく":
            return "ろっぴゃく"
        if reading == "はち":
            return "はっぴゃく"
    if nth == 2:
        if reading == "さん":
            return "さんぜん"
        if reading == "はち":
            return "はっせん"

    scale = SCALE_READING_1[nth]
    return f"{reading}{scale}"


def scale_onbin_2(reading: str, nth: int) -> str:
    if not reading:
        return ""

    if nth == 3:
        if reading[-2:] == "いち":
            return reading[:-2] + "いっちょう"
        if reading[-2:] == "はち":
            return reading[:-2] + "はっちょう"
        if reading[-3:] == "じゅう":
            return reading[:-3] + "じゅっちょう"
    if nth == 4:
        if reading[-2:] == "いち":
            return reading[:-2] + "いっけい"
        if reading[-2:] == "ろく":
            return reading[:-2] + "ろっけい"
        if reading[-2:] == "はち":
            return reading[:-2] + "はっけい"
        if reading[-3:] == "じゅう":
            return reading[:-3] + "じゅっけい"

    scale = SCALE_READING_2[nth]
    return f"{reading}{scale}"


def scale_reading_1_japanese(digit_str: str, nth: int) -> str:
    reading = "" if digit_str == "1" else digit_to_japanese(digit_str)

    return scale_onbin_1(reading, nth)


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
            return digits_to_japanese(digits_str[1:], top=False)
        reading = scale_reading_1_japanese(digits_str[0], len(digits_str) - 2)
        return f"{reading}{digits_to_japanese(digits_str[1:], top=False)}"

    if len(digits_str) > len(SCALE_READING_2) * 4:
        raise NotImplementedError(
            f"digits_to_japanese supports integers up to "
            f"{len(SCALE_READING_2) * 4} digits "
            f"(< 10^{len(SCALE_READING_2) * 4}); "
            f"got {len(digits_str)} digits.",
        )

    # Split the digits into groups of 4 from right to left
    digits_array: list[str] = []
    for i in range(0, len(digits_str), 4):
        cut = digits_str[-(i + 4) : len(digits_str) - i]
        if cut:
            digits_array.insert(0, cut)

    readings = []
    for i, digits in enumerate(digits_array):
        nth = len(digits_array) - i - 1
        base = digits_to_japanese(digits, top=False)
        reading = scale_onbin_2(base, nth)
        readings.append(reading)

    return "".join(readings)


def component_to_reading(component: Integer | type[Add] | type[Mul]) -> str:
    """
    Convert a supported leaf component or operator class.

    Supported components are non-negative integers and the Add/Mul operator
    classes used while recursively reading supported expressions.
    """
    for op_class, reading in OPERATOR_READING.items():
        if component is op_class:
            return reading
    if component.is_Integer and component >= 0:
        return digits_to_japanese(str(component))
    raise NotImplementedError(
        f"Unrecognized expr: {component}, type: {type(component)}",
    )


def expr_to_reading(expr: Add | Integer | Mul) -> str:
    """
    Convert a supported SymPy expression into its Japanese reading.

    Supported expressions are non-negative integers and Add/Mul expressions
    whose operands are also supported. Other SymPy expressions raise
    NotImplementedError.

    For commutative operations (Add, Mul), arguments are sorted by their
    string representation to produce a stable, version-independent output
    order that does not depend on SymPy's internal canonical ordering.
    """

    # Create the Japanese reading for the expression
    if expr.args:  # TODO: Currently support only infix notation
        op = component_to_reading(expr.func)
        # Sort by str() for stable output independent of SymPy version.
        sorted_args = sorted(expr.args, key=str)
        readings = [expr_to_reading(arg) for arg in sorted_args]
        return f" {op} ".join(readings)

    if expr.is_Integer:
        return component_to_reading(expr)

    raise NotImplementedError(f"Unrecognized expr: {expr}, type: {type(expr)}")


def equation_to_reading(eq: Eq) -> str:
    """
    Convert a SymPy equation into its Japanese reading.
    """
    # Extract the left and right sides of the equation
    # Create the Japanese reading for both sides
    left_reading = expr_to_reading(eq.lhs)
    right_reading = expr_to_reading(eq.rhs)
    # Combine both readings with the equals sign
    return f"{left_reading} いこーる {right_reading}"


def to_reading(expr: Add | Eq | Integer | Mul) -> str:
    """
    Convert the supported SymPy subset into a Japanese reading.

    Supported inputs are non-negative integers, Add/Mul expressions whose
    operands are supported, and Eq equations whose sides are supported.
    Unsupported expressions raise NotImplementedError.
    """
    if isinstance(expr, Eq):
        return equation_to_reading(expr)
    if isinstance(expr, Expr):
        return expr_to_reading(expr)
    raise NotImplementedError(f"Unrecognized expr: {expr}, type: {type(expr)}")
