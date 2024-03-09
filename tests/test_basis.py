import sympy

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
            ]
        )
        assert result == tobe


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
