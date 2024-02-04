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
                "じゅうにまんさんせんよんひゃくごじゅうろく",
                "かける",
                "ななひゃくはちじゅうきゅう",
                "いこーる",
                "きゅうせんななひゃくよんじゅうまんろくせんななひゃくはちじゅうよん",
            ]
        )
        assert result == tobe
