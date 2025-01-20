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
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:
    #print(decode)
    p = field.p
    n = field.mod_poly.order
    pMsg = Converter.StringIntoBaseP(message, field)
    block_len = len(str(p)) * n
    #print(pMsg)
    blockNum = int(ceil(len(pMsg) / block_len))

    pRes = ''
    for i in range(blockNum):
        if i == blockNum - 1:
            block = pMsg[i * block_len:].ljust(block_len, '0')
        else:
            block = pMsg[i * block_len : (i + 1) * block_len]
        blockInGfpn = Converter.BasePIntoElementInGFPn(block, field)
        encodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, False)
        encodedBaseP = Converter.ElementInGFPnIntoBaseP(encodedBlock).rjust(block_len, '0')
        #print(block, blockInGfpn, '|', encodedBlock, encodedBaseP)
        pRes += encodedBaseP

    #print(pRes)
    return pRes

def AffineDecode(field: gf.GFpn, message: str,
                 keyA: gf.ElementInGFpn, keyB: gf.ElementInGFpn) -> str:
    p = field.p
    n = field.mod_poly.order * len(str(field.p))
    block_len = len(str(p)) * n
    # print(pMsg)
    blockNum = int(ceil(len(message) / block_len))

    pRes = ''
    keyA = keyA.inverse()
    for i in range(blockNum):
        if i == blockNum - 1:
            block = message[i * block_len:].ljust(block_len, '0')
        else:
            block = message[i * block_len: (i + 1) * block_len]
        blockInGfpn = Converter.BasePIntoElementInGFPn(block, field)
        decodedBlock = AffineEncodeBlock(blockInGfpn, keyA, keyB, True)
        decodedBaseP = Converter.ElementInGFPnIntoBaseP(decodedBlock).rjust(n, '0')
        # print(block, blockInGfpn, '|', encodedBlock, encodedBaseP)
        pRes += decodedBaseP

    decoded = Converter.BasePIntoString(pRes, field)
    # print(pRes)
    return decoded
