# sympy-reading

![Coverage](https://raw.githubusercontent.com/kitsuyui/octocov-central/main/badges/kitsuyui/sympy-reading/coverage.svg)

Convert a small subset of SymPy expressions into Japanese readings.

## Installation

```sh
pip install sympy-reading
```

## Usage

```python
import sympy
from sympy_reading import to_reading

# Single integer
print(to_reading(sympy.Integer(3)))
# => さん

# Equation: wrap in sympy.evaluate(False) to preserve the unevaluated form
with sympy.evaluate(False):
    eq = sympy.Eq(sympy.Add(11, 22), 33)
    print(to_reading(eq))
    # => じゅういち たす にじゅうに いこーる さんじゅうさん

# Multiplication
with sympy.evaluate(False):
    eq = sympy.Eq(sympy.Mul(2, 3, 4), 24)
    print(to_reading(eq))
    # => に かける さん かける よん いこーる にじゅうよん
```

> **Note:** Always wrap `Add` and `Mul` expressions in `sympy.evaluate(False)`
> (or pass `evaluate=False` to the constructor). Without it, SymPy evaluates
> the expression before `to_reading()` can inspect the operator, so the
> structure is lost.

## Supported expression scope

This package currently supports a narrow, explicit subset:

- non-negative SymPy integer constants;
- `sympy.Add` and `sympy.Mul` expressions whose operands are recursively in
  the supported subset;
- `sympy.Eq` equations whose left and right sides are recursively in the
  supported subset.

`Add` is read as infix `たす`, `Mul` is read as infix `かける`, and `Eq` is
read as `いこーる`.

Unsupported expressions raise `NotImplementedError`, including symbols,
negative integers, rationals, floats, functions, powers, inequalities, and
operators other than `Add` and `Mul`.
