from symbol import return_stmt

import Affine as aff
import Fields
import galois_field as gf

msg = '''Please choose the program mode:
0: exit
1: Affine cypher
2: Galois field tool
'''

affineMsg = '''Please choose the operation:
0: Set the field and keys
1: Encode message
2: Decode latest message
3: Decode message
'''

def GetGFpn() -> gf.ElementInGFpn:
    p, n = map(int, input('Enter the p and n: ').split())

    return Fields.CreateGFpn(p, n)

def GetKeyA(field: gf.GFpn):
    poly =  list(map(int, input("Enter key A (for example 1 0 3 2 would be x^3 + 3x + 2): ").split()))
    if poly == [0]: raise ValueError('KeyA shouldn\'t be zero')

    return field.elm(poly)

def GetKeyB(field: gf.GFpn):
    poly =  list(map(int, input("Enter key B: ").split()))

    return field.elm(poly)

def GetAllNeededInfo():
    GFpn = GetGFpn()
    keyA = GetKeyA(GFpn)
    keyB = GetKeyB(GFpn)

    return GFpn, keyA, keyB

def AffineMode():
    GFpn, keyA, keyB = GetAllNeededInfo()
    latestEncodedMessage = ''
    while True:
        op = int(input(affineMsg))
        if op == 0:
            GFpn, keyA, keyB = GetAllNeededInfo()
        if op == 1:
            message = input('Please enter the message: ')
            latestEncodedMessage = aff.AffineEncode(GFpn, message, keyA, keyB)
            print(latestEncodedMessage)
        if op == 2:
            decodedMessage = aff.AffineDecode(GFpn, latestEncodedMessage, keyA, keyB)
            print(decodedMessage)
        if op == 3:
            message = input('Please enter the message: ')
            decodedMessage = aff.AffineDecode(GFpn, message, keyA, keyB)
            print(decodedMessage)

if __name__ == '__main__':

    func = int(input(msg))
    if func == 0:
        exit()
    if func == 1:
        AffineMode()
