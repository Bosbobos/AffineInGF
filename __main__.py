import Affine as aff
import Fields
import galois_field as gf
import galois

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
3: Find primitive elements
4: Decompose group elements
'''


def GetGFpn() -> gf.ElementInGFpn:
    p, n = map(int, input('Enter the p and n: ').split())
    return Fields.CreateGFpn(p, n)


def GetKeyA(field: gf.GFpn):
    poly = list(map(int, input("Enter key A (for example 1 0 3 2 would be x^3 + 3x + 2): ").split()))
    if poly == [0]: raise ValueError('KeyA shouldn\'t be zero')
    return field.elm(poly)


def GetKeyB(field: gf.GFpn):
    poly = list(map(int, input("Enter key B: ").split()))
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


import galois


def GaloisMode():
    p, n = map(int, input('Enter the p and n for Galois Field: ').split())
    field = galois.GF(p ** n)
    print(f'Field: {field}')
    while True:
        op = int(input(galoisMsg))

        if op == 0:
            p, n = map(int, input('Enter the p and n for Galois Field: ').split())
            # Используем galois.GF(p ** n), чтобы создать поле Галуа
            field = galois.GF(p ** n)  # Это поле Галуа с характеристикой p и степенью n
            print(f'Field: {field}')

        elif op == 1:
            # Вводим коэффициенты полиномов для операции сложения
            poly1 = list(map(int, input("Enter first polynomial (coefficients): ").split()))
            poly2 = list(map(int, input("Enter second polynomial (coefficients): ").split()))
            poly1 = galois.Poly(poly1, field)
            poly2 = galois.Poly(poly2, field)
            sum_result = poly1 + poly2
            print(f"Sum: {sum_result}")

        elif op == 2:
            # Вводим коэффициенты полиномов для операции умножения
            poly1 = list(map(int, input("Enter first polynomial (coefficients): ").split()))
            poly2 = list(map(int, input("Enter second polynomial (coefficients): ").split()))
            poly1 = galois.Poly(poly1, field)
            poly2 = galois.Poly(poly2, field)
            mul_result = poly1 * poly2
            print(f"Multiplication: {mul_result}")

        elif op == 3:
            # Получаем примитивные элементы поля
            field.repr('poly')
            primitive_elements = field.primitive_elements
            print(f"Primitive elements: {primitive_elements}")
            field.repr('int')
        elif op == 4:
            # Разлагаем элементы группы по степеням генератора
            field.repr('poly')
            generator = field.primitive_element
            print("Decomposed group elements:")
            for i in range(field.order):
                print(i, generator**i)
            field.repr('int')
        elif op == -1:
            break


if __name__ == '__main__':
    func = int(input(msg))
    if func == 0:
        exit()
    elif func == 1:
        AffineMode()
    elif func == 2:
        GaloisMode()
