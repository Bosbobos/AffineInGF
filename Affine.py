import galois_field as gf
import Converter
import TextManager as tm

def AffineEncodeBlock(block: gf.ElementInGFpn,
                      keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn,
                      decode: bool) -> str:
    if decode:
        y = (block - keyB) * keyA
    else:
        y = keyA * block + keyB
    return y

def AffineEncode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn,
                 decode: bool = False) -> str:
    binMsg = tm.string_to_binary(message)
    blockLen = field.mod_poly.order
    binMsg += '0' * (len(binMsg) % blockLen)
    blockNum = len(binMsg) // blockLen

    binRes = ''
    for i in range(blockNum):
        block = binMsg[i * blockLen : (i + 1) * blockLen]
        blockInGfpn = Converter.BinaryIntoElementInGFpn(block, field)
        encodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, decode)
        encodedBinary = Converter.ElementInGFpnIntoBinary(encodedBlock)
        binRes += encodedBinary

    res = tm.binary_to_string(binRes)
    return res

def AffineDecode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:
    invKeyA = keyA.inverse()

    return AffineEncode(field, message, invKeyA, keyB, True)
