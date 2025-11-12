from __future__ import annotations
from math import gcd

__all__ = ["Fraction"]


def _check_zero(value: RationalLike) -> None:
    _raise: bool = False
    if isinstance(value, (int, float)) and value == 0:
        _raise = True
    elif isinstance(value, Fraction) and value.numerator == 0:
        _raise = True

    if _raise:
        raise ZeroDivisionError("Denominator cannot be zero.")


def _float_to_fraction(value: float) -> tuple[int, int]:
    st = str(value)
    n_zeros = len(st.split(".")[-1])
    num = int(st.replace(".", ""))
    den = 10**n_zeros
    return num, den


def _process_rational_like(value: RationalLike) -> tuple[int, int]:
    if isinstance(value, Fraction):
        return value.numerator, value.denominator
    if isinstance(value, int):
        return value, 1
    if isinstance(value, float):
        return _float_to_fraction(value)

    raise TypeError(f"Unsupported type: {type(value)}")


def _reduce_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    common_divisor = gcd(numerator, denominator)
    num = numerator // common_divisor
    den = denominator // common_divisor
    if (num < 0) and (den < 0):
        num = -num
        den = -den
    return num, den


class Fraction:
    def __init__(self, numerator: RationalLike, denominator: RationalLike = 1) -> None:
        _check_zero(denominator)
        num_a, num_b = _process_rational_like(numerator)
        den_a, den_b = _process_rational_like(denominator)
        self._numerator, self._denominator = _reduce_fraction(num_a * den_b, num_b * den_a)

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    @property
    def inverse(self) -> Fraction:
        return Fraction(self.denominator, self.numerator)

    def __add__(self, other: RationalLike) -> Fraction:
        other_as_fraction = Fraction(other)
        new_numerator = self.numerator * other_as_fraction.denominator + other_as_fraction.numerator * self.denominator
        new_denominator = self.denominator * other_as_fraction.denominator
        return Fraction(new_numerator, new_denominator)

    def __radd__(self, other: RationalLike) -> Fraction:
        return self + other

    def __neg__(self) -> Fraction:
        return Fraction(-self.numerator, self.denominator)

    def __sub__(self, other: RationalLike) -> Fraction:
        return self + Fraction(-other)

    def __rsub__(self, other: RationalLike) -> Fraction:
        return self - other

    def __mul__(self, other: RationalLike) -> Fraction:
        other_as_fraction = Fraction(other)
        new_numerator = self.numerator * other_as_fraction.numerator
        new_denominator = self.denominator * other_as_fraction.denominator
        return Fraction(new_numerator, new_denominator)

    def __rmul__(self, other: RationalLike) -> Fraction:
        return self * other

    def __truediv__(self, other: RationalLike) -> Fraction:
        other_as_fraction = Fraction(other)
        return self * other_as_fraction.inverse

    def __rtruediv__(self, other: RationalLike) -> Fraction:
        return self.inverse * other

    def __repr__(self) -> str:
        return f"{self.numerator}/{self.denominator}"


RationalLike = int | float | Fraction
