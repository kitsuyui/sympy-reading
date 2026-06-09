from typing import get_args, get_type_hints

import pytest
import sympy

import sympy_reading
from sympy_reading import to_reading


def test_to_reading() -> None:
    with sympy.evaluate(False):
        equation = sympy.Eq(sympy.Add(11, 22), 33)
        result = to_reading(equation)
        assert result == "じゅういち たす にじゅうに いこーる さんじゅうさん"

    with sympy.evaluate(False):
        equation = sympy.Eq(sympy.Mul(123456, 789), 97406784)
        result = to_reading(equation)
        tobe = " ".join(
            [
                "じゅうにまんさんぜんよんひゃくごじゅうろく",
                "かける",
                "ななひゃくはちじゅうきゅう",
                "いこーる",
                "きゅうせんななひゃくよんじゅうまんろくせんななひゃくはちじゅうよん",
            ],
        )
        assert result == tobe


def test_nested_expr() -> None:
    with sympy.evaluate(False):
        equation = sympy.Eq(sympy.Mul(sympy.Mul(2, 3), 4), 24)
        result = to_reading(equation)
        tobe = "に かける さん かける よん いこーる にじゅうよん"
        assert result == tobe


def test_to_reading_with_three_operands() -> None:
    with sympy.evaluate(False):
        equation = sympy.Eq(sympy.Add(1, 2, 3), 6)
        result = to_reading(equation)
        assert result == "いち たす に たす さん いこーる ろく"

    with sympy.evaluate(False):
        equation = sympy.Eq(sympy.Mul(2, 3, 4), 24)
        result = to_reading(equation)
        assert result == "に かける さん かける よん いこーる にじゅうよん"


def test_supported_expression_scope_without_equation() -> None:
    assert to_reading(sympy.Integer(0)) == "ぜろ"

    with sympy.evaluate(False):
        expression = sympy.Add(sympy.Integer(1), sympy.Mul(2, 3))
        result = to_reading(expression)
        assert result == "いち たす に かける さん"


def test_integer_compound_dispatches_as_compound() -> None:
    # Add(1, 2) with evaluate=False satisfies both expr.args (non-empty) and
    # expr.is_integer (True). The args branch must be checked first so the
    # expression is rendered as infix, not passed to component_to_reading.
    with sympy.evaluate(False):
        assert to_reading(sympy.Add(1, 2)) == "いち たす に"
        assert to_reading(sympy.Mul(3, 4)) == "さん かける よん"


def test_to_reading_type_hint_matches_supported_root_scope() -> None:
    hints = get_type_hints(sympy_reading.to_reading)
    accepted_types = set(get_args(hints["expr"]))

    assert accepted_types == {
        sympy.Add,
        sympy.Eq,
        sympy.Integer,
        sympy.Mul,
    }
    assert sympy.Expr not in accepted_types


@pytest.mark.parametrize(
    "expr",
    [
        sympy.Symbol("x"),
        sympy.Symbol("n", integer=True),
        sympy.Rational(1, 2),
        sympy.Integer(-1),
        sympy.Pow(2, 3, evaluate=False),
    ],
)
def test_unsupported_expression_scope(expr) -> None:
    with pytest.raises(NotImplementedError, match="Unrecognized expr"):
        to_reading(expr)


def test_onbin() -> None:
    equation = sympy.Number(8300)
    result = to_reading(equation)
    tobe = "はっせんさんびゃく"
    assert result == tobe

    equation = sympy.Number(3800)
    result = to_reading(equation)
    tobe = "さんぜんはっぴゃく"
    assert result == tobe

    equation = sympy.Number(3600)
    result = to_reading(equation)
    tobe = "さんぜんろっぴゃく"
    assert result == tobe

    equation = sympy.Number(10**12)
    result = to_reading(equation)
    tobe = "いっちょう"
    assert result == tobe

    equation = sympy.Number(6 * 10**12)
    result = to_reading(equation)
    tobe = "ろくちょう"
    assert result == tobe

    equation = sympy.Number(8 * 10**12)
    result = to_reading(equation)
    tobe = "はっちょう"
    assert result == tobe

    equation = sympy.Number(10**13)
    result = to_reading(equation)
    tobe = "じゅっちょう"
    assert result == tobe

    equation = sympy.Number(10**16)
    result = to_reading(equation)
    tobe = "いっけい"
    assert result == tobe

    equation = sympy.Number(6 * 10**16)
    result = to_reading(equation)
    tobe = "ろっけい"
    assert result == tobe

    equation = sympy.Number(8 * 10**16)
    result = to_reading(equation)
    tobe = "はっけい"
    assert result == tobe

    equation = sympy.Number(10**17)
    result = to_reading(equation)
    tobe = "じゅっけい"
    assert result == tobe
