import galois_field as gf
import Converter
import TextManager as tm
from math import log, ceil

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
    #print(decode)
    p = field.p
    n = field.mod_poly.order * len(str(field.p))
    if not decode: message += ' ' * 10
    pMsg = tm.string_to_base_p(message, p)
    #print(pMsg)

    blockNum = int(ceil(len(pMsg) / n))

    if decode: keyA = keyA.inverse()
    pRes = ''
    for i in range(blockNum):
        if i == blockNum - 1:
            block = pMsg[i * n:].ljust(n, '0')
        else:
            block = pMsg[i * n : (i + 1) * n]
        blockInGfpn = Converter.BasePIntoElementInGFPn(block, field)
        encodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, decode)
        encodedBaseP = Converter.ElementInGFPnIntoBaseP(encodedBlock).rjust(n, '0')
        #print(block, blockInGfpn, '|', encodedBlock, encodedBaseP)
        pRes += encodedBaseP

    res = tm.base_p_to_string(pRes, p)
    #print(pRes)
    return res.split(' '*3)[0]

def AffineDecode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:

    return AffineEncode(field, message, keyA, keyB, True)
