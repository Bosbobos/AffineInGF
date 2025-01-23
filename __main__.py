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

galoisMsg = '''Please choose the operation:
0: Set the field
1: Add polynomials
2: Multiply polynomials
3: Find a primitive element
4: Decompose group element
'''

def GetGFpn() -> gf.GFpn:
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

def GaloisMode():
    field = GetGFpn()
    primitive = field.random_primitive_elm()
    print(f'Field: {field}')
    while True:
        op = int(input(galoisMsg))

        if op == 0:
            field = GetGFpn()
            print(f'Field: {field}')

        elif op == 1:
            poly1 = list(map(int, input("Enter first polynomial (coefficients): ").split()))
            poly2 = list(map(int, input("Enter second polynomial (coefficients): ").split()))

            print(f"Sum: {field.elm(poly1) + field.elm(poly2)}")

        elif op == 2:
            poly1 = list(map(int, input("Enter first polynomial (coefficients): ").split()))
            poly2 = list(map(int, input("Enter second polynomial (coefficients): ").split()))

            print(f"Product: {field.elm(poly1) * field.elm(poly2)}")

        elif op == 3:
            print(f"Primitive element: {primitive}")

        elif op == 4:
            element = field.elm(list(map(int, input("Enter polynomial (coefficients): ").split())))
            i = 1
            prim = primitive
            while prim != element:
                prim *= primitive
                i += 1
            print(f"{element} = ({primitive}) ** {i}")

        elif op == -1:
            break

if __name__ == '__main__':
    func = int(input(msg))
    if func == 0:
        exit()
    if func == 1:
        AffineMode()
    if func == 2:
        GaloisMode()