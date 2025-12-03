import pytest
from goodfractions import Fraction


# Un 'fixture' para proporcionar instancias comunes de Fraction
@pytest.fixture
def f_half():
    return Fraction(1, 2)


@pytest.fixture
def f_third():
    return Fraction(1, 3)


@pytest.fixture
def f_negative():
    return Fraction(-3, 4)


@pytest.fixture
def f_zero():
    return Fraction(0)


# ====================================================================
# TESTS DE INICIALIZACIÓN, SIMPLIFICACIÓN Y PROPIEDADES
# ====================================================================


class TestInitializationAndProperties:

    # --- Tests de Inicialización y Reducción con Enteros ---
    def test_init_int_simple(self):
        """Inicialización simple y numerador/denominador."""
        f = Fraction(3, 4)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_init_int_reduction(self):
        """Reducción de fracciones (10/5 -> 2/1)."""
        f = Fraction(10, 5)
        assert f.numerator == 2
        assert f.denominator == 1

    def test_init_int_negative_numerator(self):
        """Signo negativo en el numerador (-3/4)."""
        f = Fraction(-3, 4)
        assert f.numerator == -3
        assert f.denominator == 4

    def test_init_int_negative_denominator(self):
        """Caso límite: Signo negativo en el denominador (3/-4 -> -3/4)."""
        f = Fraction(3, -4)
        assert f.numerator == -3
        assert f.denominator == 4

    def test_init_int_double_negative(self):
        """Caso límite: Ambos negativos (-3/-4 -> 3/4)."""
        f = Fraction(-3, -4)
        assert f.numerator == 3
        assert f.denominator == 4

    def test_init_int_whole_number(self):
        """Inicialización con solo numerador (entero 5 -> 5/1)."""
        f = Fraction(5)
        assert f.numerator == 5
        assert f.denominator == 1

    # --- Tests de Inicialización con Floats ---
    def test_init_float_simple(self):
        """Inicialización con float (0.5 -> 1/2)."""
        f = Fraction(0.5)
        assert f.numerator == 1
        assert f.denominator == 2

    def test_init_float_three_tenths(self):
        """Inicialización con float exacto (0.3 -> 3/10)."""
        f = Fraction(0.3)
        assert f.numerator == 3
        assert f.denominator == 10

    def test_init_float_complex(self):
        """Inicialización con float en numerador y denominador (0.5 / 0.25 -> 2/1)."""
        f = Fraction(0.5, 0.25)
        assert f.numerator == 2
        assert f.denominator == 1

    # --- Tests de Inicialización Cero y Errores ---
    def test_init_zero(self, f_zero):
        """Caso límite: Inicialización con cero (0/X -> 0/1)."""
        assert f_zero.numerator == 0
        assert f_zero.denominator == 1

    def test_init_zero_division_error(self):
        """Caso límite: Denominador igual a cero."""
        with pytest.raises(ZeroDivisionError):
            Fraction(1, 0)
        with pytest.raises(ZeroDivisionError):
            Fraction(1, 0.0)
        with pytest.raises(ZeroDivisionError):
            Fraction(1, Fraction(0, 5))

    # --- Tests de Propiedades ---
    def test_property_inverse(self, f_half):
        """Propiedad 'inverse' (1/2 -> 2/1)."""
        inv = f_half.inverse
        assert inv.numerator == 2
        assert inv.denominator == 1

    def test_property_inverse_zero_error(self, f_zero):
        """Propiedad 'inverse' caso límite: Invertir cero (0/1)."""
        with pytest.raises(ZeroDivisionError):
            f_zero.inverse

    def test_property_sign(self, f_half, f_negative, f_zero):
        """Propiedad 'sign'."""
        assert f_half.sign == 1
        assert f_negative.sign == -1
        assert f_zero.sign == 0

    def test_repr(self):
        """Método __repr__."""
        f = Fraction(10, 20)
        assert repr(f) == "1/2"


# ====================================================================
# TESTS DE IGUALDAD Y ARITMÉTICA
# ====================================================================


class TestArithmetic:

    # --- Tests de Igualdad (==) ---
    def test_equality_fraction_fraction(self):
        """Igualdad entre fracciones (reducidas o no)."""
        assert Fraction(1, 2) == Fraction(2, 4)
        assert Fraction(-3, 4) == Fraction(3, -4)
        assert Fraction(1, 3) != Fraction(2, 5)

    def test_equality_fraction_int(self):
        """Igualdad con enteros."""
        assert Fraction(6, 3) == 2
        assert 3 == Fraction(12, 4)
        assert Fraction(1, 3) != 1

    def test_equality_fraction_float(self):
        """Igualdad con floats (comprobando conversión correcta)."""
        assert Fraction(1, 2) == 0.5
        assert 0.2 == Fraction(1, 5)
        assert Fraction(3, 1) == 3.0
        # Caso límite donde el float podría no ser exacto, pero la clase lo maneja por string
        assert Fraction(1, 10) == 0.1

    # --- Tests de Suma (+) ---
    def test_add_fraction_fraction(self, f_half, f_third):
        """Suma de fracciones (1/2 + 1/3 = 5/6)."""
        result = f_half + f_third
        assert result.numerator == 5
        assert result.denominator == 6

    def test_add_fraction_int(self, f_half):
        """Suma con entero (1/2 + 1 = 3/2)."""
        assert f_half + 1 == Fraction(3, 2)
        assert 2 + f_half == Fraction(5, 2)  # __radd__

    def test_add_fraction_float(self, f_half):
        """Suma con float (1/2 + 0.5 = 1/1)."""
        assert f_half + 0.5 == Fraction(1, 1)
        assert 0.5 + f_half == Fraction(1, 1)  # __radd__

    # --- Tests de Resta (-) ---
    def test_sub_fraction_fraction(self, f_half, f_third):
        """Resta de fracciones (1/2 - 1/3 = 1/6)."""
        result = f_half - f_third
        assert result.numerator == 1
        assert result.denominator == 6

    def test_sub_fraction_int_rsub(self, f_half):
        """Resta de entero menos fracción (1 - 1/2 = 1/2)."""
        assert 1 - f_half == Fraction(1, 2)  # __rsub__

    def test_sub_limit_self_subtraction(self, f_half):
        """Caso límite: Restarse a sí mismo (debe dar 0/1)."""
        assert f_half - f_half == Fraction(0, 1)

    # --- Tests de Multiplicación (*) ---
    def test_mul_fraction_fraction(self):
        """Multiplicación de fracciones (2/3 * 9/4 = 18/12 = 3/2)."""
        result = Fraction(2, 3) * Fraction(9, 4)
        assert result == Fraction(3, 2)

    def test_mul_fraction_int(self, f_half):
        """Multiplicación por entero (1/2 * 4 = 2/1)."""
        assert f_half * 4 == Fraction(2, 1)
        assert 4 * f_half == Fraction(2, 1)  # __rmul__

    # --- Tests de División (/) ---
    def test_truediv_fraction_fraction(self):
        """División de fracciones (2/3 / 1/4 = 8/3)."""
        result = Fraction(2, 3) / Fraction(1, 4)
        assert result == Fraction(8, 3)

    def test_truediv_int_fraction(self):
        """División de entero por fracción (4 / 2/3 = 6/1)."""
        assert 4 / Fraction(2, 3) == Fraction(6, 1)  # __rtruediv__

    def test_truediv_by_zero(self, f_half):
        """Caso límite: División por cero."""
        with pytest.raises(ZeroDivisionError):
            f_half / 0
        with pytest.raises(ZeroDivisionError):
            f_half / Fraction(0, 5)
