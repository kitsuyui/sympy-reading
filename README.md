# sympy-reading

![Coverage](https://raw.githubusercontent.com/kitsuyui/octocov-central/main/badges/kitsuyui/sympy-reading/coverage.svg)

Convert a small subset of SymPy expressions into Japanese readings.

## Supported expression scope

This package currently supports a narrow, explicit subset:

- non-negative SymPy integer constants;
- `sympy.Add` and `sympy.Mul` expressions whose operands are recursively in
  the supported subset;
- `sympy.Eq` equations whose left and right sides are recursively in the
  supported subset.

`Add` is read as infix `たす`, `Mul` is read as infix `かける`, and `Eq` is
read as `いこーる`.

Use `sympy.evaluate(False)` or `evaluate=False` when an example must preserve
numeric operators. Otherwise, SymPy may evaluate expressions such as
`sympy.Add(1, 2)` before `to_reading()` sees the `Add` operation.

Unsupported expressions raise `NotImplementedError`, including symbols,
negative integers, rationals, floats, functions, powers, inequalities, and
operators other than `Add` and `Mul`.

## Version Status

This package is currently classified as `Development Status :: 3 - Alpha`.
The API may change without notice.
A stable release will be tagged when the supported expression scope stabilizes and breaking changes become unlikely.
