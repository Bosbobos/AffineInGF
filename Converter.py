import galois_field as gf
from math import log, ceil
import numpy as np

def ToDecimal(coeffs, base) -> int:
    res = 0
    for i in range(len(coeffs)):
        res += coeffs[i] * base ** (len(coeffs) - i - 1)

    return res

def ToBaseP(num, base) -> [int]:
    coeffs = []
    while num:
        coeffs.append(num % base)
        num //= base

    return coeffs[::-1]

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

    return '0' * (len(elem.mod_poly) - len(elem.coeffs)) * len(str(elem.p)) + res



def ElementInGFPnIntoBaseP1(elem: gf.ElementInGFpn) -> str:
    block_len = ceil(log(ord('Я'), elem.p)) * len(str(elem.p))
    res = ''
    for x in elem.coeffs:
        res += str(x).rjust(len(str(elem.p)), '0')

    return res.rjust(block_len, '0')

def StringIntoBaseP(text: str, field: gf.GFpn) -> str:
    res = ''
    p = field.p
    block_len = ceil(log(ord('Я'), p)) * len(str(p))

    for symbol in text:
        sym_res = []
        x = ord(symbol)
        while x:
            sym_res.append(str(x % p).rjust(len(str(p)), '0'))
            x //= p

        res += ''.join(sym_res[::-1]).rjust(block_len, '0')

    return res

def BasePIntoString(encoded_text: str, field: gf.GFpn) -> str:
    res = ''
    p = field.p
    block_len = ceil(log(ord('Я'), p)) * len(str(p))
    for i in range(0, len(encoded_text), block_len):
        sym_res = 0
        block = encoded_text[i:i + block_len].rjust(block_len, '0')
        for j in range(0, block_len, len(str(p))):
            x = int(block[j: j + len(str(p))])
            sym_res += x * p ** (block_len // len(str(p)) - j // len(str(p)) - 1)

        res += chr(int(sym_res))

    return res

def ElementInGFPnIntoHex(elem: gf.ElementInGFpn) -> str:
    max_val = elem.p ** elem.mod_poly.order
    digit_len = ceil(log(max_val, 16))
    dec = ToDecimal(elem.coeffs, elem.p)
    hexa = ToBaseP(dec, 16)
    return ''.join([x.rjust(digit_len) for x in hexa])

def HexIntoElementInGFPn(hexa: str, field: gf.GFpn) -> gf.ElementInGFpn:
    coeffs = []
    max_field_val = field.p ** field.mod_poly.order
    digit_len = ceil(log(max_field_val, 16))
    for i in range(0, len(hexa), digit_len):
        block = int(hexa[i : i + digit_len])

def GetMessageWithEncodedLen(message: str) -> str:
    i = 0
    l = ''
    while message[i] != '|':
        l += message[i]
        i += 1
    msg = message[i + 1 : i + int(l) + 1]

    return msg