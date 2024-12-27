import galois_field as gf
from galois_field import GFpn
import Converter
import TextManager as tm

def AffineEncodeBlock(block: gf.ElementInGFpn,
                      keyA: gf.ElementInGFpn, kebB: gf.ElementInGFpn) -> str:
    y = keyA * block + kebB
    return y

def AffineEncode(field: gf.GFpn, message: str, keyA: gf.ElementInGFpn, kebB: gf.ElementInGFpn):
    binMsg = tm.string_to_binary(message)
    binMsg += '0' * len(binMsg) % field.p
    blockLen = field.p
    blockNum = len(binMsg) // blockLen

    res = ''
    for i in range(blockNum):
        block = binMsg[i * blockLen : (i + 1) * blockLen]
        blockInGfpn = Converter.BinaryIntoElementInGFpn(blockInGfpn, GFpn)
        encodedBlock = AffineEncodeBlock(block, keyA, kebB)
        res += Converter.ElementInGFpnIntoBinary(encodedBlock)

    return res
