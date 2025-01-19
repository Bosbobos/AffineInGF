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
    n = elem.mod_poly.order
    coeffs = [0]*(n - len(elem.coeffs)) + elem.coeffs
    for i in range(n):
        res += coeffs[i] * elem.p**(n - i - 1)

    return bin(res)[2:]

def BasePIntoElementInGFPn(baseP: str, GFpn: gf.GFpn) -> gf.ElementInGFpn:
    coeffs = []
    p = GFpn.p
    for i in range(0, len(baseP), len(str(p))):
        x = int(baseP[i : i + len(str(p))])
        coeffs.append(x)

    return gf.ElementInGFpn(coeffs, p, GFpn.mod_poly)

def ElementInGFPnIntoBaseP(elem: gf.ElementInGFpn) -> str:
    res = ''
    for x in elem.coeffs:
        res += str(x).rjust(len(str(elem.p)), '0')

    return res
