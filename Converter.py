import galois_field as gf
import numpy as np

def BinaryIntoElementInGFpn(bin: str, GFpn: gf.GFpn) -> gf.ElementInGFpn:
    coeffs = []
    num = int(bin, 2)
    p = GFpn.p
    while num:
        coeffs.append(num % p)
        num //= p

    return gf.ElementInGFpn(coeffs[::-1], p, GFpn.mod_poly)

def ElementInGFpnIntoBinary(elem: gf.ElementInGFpn) -> str:
    res = 0
    coeffs = elem.coeffs
    for i in range(len(coeffs)):
        res += coeffs[i] * elem.p**(len(coeffs) - i - 1)

    return bin(res)[2:]
