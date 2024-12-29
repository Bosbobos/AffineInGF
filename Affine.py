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
    blockLen = int(ceil(log2(field.p ** field.mod_poly.order + 1))) # Цель - подобрать величину блока такую, чтобы в неё поместилось максимальное число, которое можно записать в GFpn
    if not decode: binMsg = tm.string_to_binary(message + ' ' * 10)
    else: binMsg = tm.string_to_binary(message)

    blockNum = int(ceil(len(binMsg) / blockLen))

    if decode: keyA = keyA.inverse()
    binRes = ''
    for i in range(blockNum):
        if i == blockNum - 1:
            block = binMsg[i * blockLen].rjust(blockLen, '0')
        else:
            block = binMsg[i * blockLen : (i + 1) * blockLen]
        blockInGfpn = Converter.BinaryIntoElementInGFpn(block, field)
        encodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, decode)
        encodedBinary = Converter.ElementInGFpnIntoBinary(encodedBlock)
        binRes += encodedBinary.rjust(blockLen, '0')

    res = tm.binary_to_string(binRes)
    return res.split(' '*5)[0]

def AffineDecode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:

    return AffineEncode(field, message, keyA, keyB, True)
