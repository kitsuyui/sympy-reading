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

## Version Status

This package is currently classified as `Development Status :: 3 - Alpha`.
The API may change without notice.
A stable release will be tagged when the supported expression scope stabilizes and breaking changes become unlikely.

## Development

This repository uses [lefthook](https://lefthook.dev/) to run the same checks as CI
locally, so problems surface before they reach CI.

```sh
# Install dependencies
uv sync

# Install the Git hooks (once; requires lefthook on your PATH)
lefthook install
```

Once installed, the hooks run automatically:

- **pre-commit**: `uv run poe check`
- **pre-push**: `uv run poe check` and `uv run poe test`

You can also run the checks manually:

```sh
uv run poe check
uv run poe test
```

CI still runs the full matrix (see `.github/workflows/`); the hooks only bring that
feedback earlier on your machine.
