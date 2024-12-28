import galois_field as gf
import Converter
import TextManager as tm
from numpy import log2, ceil

def AffineEncodeBlock(block: gf.ElementInGFpn,
                      keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn,
                      decode: bool) -> gf.ElementInGFpn:
    if decode:
        y = (block - keyB) * keyA # KeyA passed into the arguments should already be inversed (for performance)
    else:
        y = keyA * block + keyB
    return y

def AffineEncode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn,
                 decode: bool = False) -> str:
    binMsg = tm.string_to_binary(message)
    blockLen = int(ceil(log2(field.p ** field.mod_poly.order + 1))) # Цель - подобрать величину блока такую, чтобы в неё поместилось максимальное число, которое можно записать в GFpn
    binMsg += '0' * (len(binMsg) % blockLen)
    blockNum = len(binMsg) // blockLen

    binRes = ''
    for i in range(blockNum):
        block = binMsg[i * blockLen : (i + 1) * blockLen]
        blockInGfpn = Converter.BinaryIntoElementInGFpn(block, field)
        encodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, decode)
        encodedBinary = Converter.ElementInGFpnIntoBinary(encodedBlock).rjust(blockLen, '0')
        binRes += encodedBinary

    res = tm.binary_to_string(binRes)
    return res

def AffineDecode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:
    invKeyA = keyA.inverse()

    return AffineEncode(field, message, invKeyA, keyB, True)
