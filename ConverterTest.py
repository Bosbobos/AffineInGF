import pytest
import galois_field as gf
import numpy as np
from Converter import *

# Тестовые данные для метода BinaryIntoElementInGFpn
@pytest.mark.parametrize(
    "bin_str, p, mod_poly, expected_coeffs",
    [
        ("1011", 2, [1, 0, 1], [1]),
        ("1100", 3, [1, 0, 0, 2], [1, 1, 0]),
        ("0", 2, [1, 1], [0]),
        ("1", 5, [1, 0, 1, 2], [1]),
        ("1011", 2, [1, 1, 1, 1, 1], [1, 0, 1, 1])
    ]
)
def test_BinaryIntoElementInGFpn(bin_str, p, mod_poly, expected_coeffs):
    GFpn = gf.GFpn(p, mod_poly)

    result = BinaryIntoElementInGFpn(bin_str, GFpn)

    assert isinstance(result, gf.ElementInGFpn)
    assert result.coeffs == expected_coeffs
    assert result.p == p
    assert list(result.mod_poly) == mod_poly


# Тестовые данные для метода ElementInGFpnIntoBinary
@pytest.mark.parametrize(
    "expected_bin, p, mod_poly, coeffs",
    [
        ("1", 2, [1, 0, 1], [1]),
        ("1100", 3, [1, 0, 0, 2], [1, 1, 0]),
        ("0", 2, [1, 1], [0]),
        ("1", 5, [1, 0, 1, 2], [1]),
        ("1011", 2, [1, 1, 1, 1, 1], [1, 0, 1, 1])
    ]
)
def test_ElementInGFpnIntoBinary(expected_bin, p, mod_poly, coeffs):
    elem = gf.ElementInGFpn(coeffs, p, mod_poly)

    result = ElementInGFpnIntoBinary(elem)

    assert result == expected_bin
