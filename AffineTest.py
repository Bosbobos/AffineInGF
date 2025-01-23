import pytest
import galois_field as gf
from Affine import *
from Fields import *

@pytest.mark.parametrize(
    "block_coeffs, keyA_coeffs, keyB_coeffs, p, mod_coeffs, decode, expected_coeffs",
    [
        # Пример 1: Кодирование
        ([3, 1], [2, 0], [1, 1], 5, [1, 0, 2, 1], False, [4, 3]),
        # Пример 3: Кодирование с другими значениями
        ([2, 3, 4], [1, 1], [0, 1, 1], 7, [1, 0, 3], False, [3, 4, 6])
    ]
)
def test_affine_encode_block(block_coeffs, keyA_coeffs, keyB_coeffs, p, mod_coeffs, decode, expected_coeffs):
    # Настройка поля GF(p^n)
    field = gf.GFpn(p, mod_coeffs)

    assert field.is_valid

    # Создание элементов поля
    block = field.elm(block_coeffs)
    keyA = field.elm(keyA_coeffs)
    invKeyA = keyA.inverse()
    keyB = field.elm(keyB_coeffs)

    # Преобразование
    result = AffineEncodeBlock(block, keyA, keyB, decode)

    decodedResult = AffineEncodeBlock(result, invKeyA, keyB, not decode)

    # Проверка
    assert block.coeffs == decodedResult.coeffs

@pytest.mark.parametrize(
    "block_coeffs, keyA_coeffs, keyB_coeffs, p, n",
    [
        # Пример 1: Кодирование
        ([3, 1], [0, 2], [1, 1], 5, 7),
        # Пример 3: Кодирование с другими значениями
        ([2, 3, 4], [1, 1], [0, 1, 1], 7, 13),
        ([1, 1, 1, 7, 4, 2], [1, 0, 0, 0, 0, 0, 8, 21], [5], 3, 7)
    ]
)
def test_affine_encode_block(block_coeffs, keyA_coeffs, keyB_coeffs, p, n):
    # Настройка поля GF(p^n)
    field = CreateGFpn(p, n)

    assert field.is_valid

    # Создание элементов поля
    block = field.elm(block_coeffs)
    keyA = field.elm(keyA_coeffs)
    invKeyA = keyA.inverse()
    keyB = field.elm(keyB_coeffs)

    # Преобразование
    result = AffineEncodeBlock(block, keyA, keyB, False)

    decodedResult = AffineEncodeBlock(result, invKeyA, keyB, True)

    # Проверка
    assert block.coeffs == decodedResult.coeffs

@pytest.mark.parametrize(
    "message, keyA_coeffs, keyB_coeffs, p, n",#109987, 4
    [
        ("i love cryptography <3", [5, 17, 28, 60, 56], [7, 7, 7, 7, 7, 7], 61, 139),
        ("i love cryptography <3", [5, 17, 28, 60, 56], [7, 7, 7, 7, 7, 7], 647, 9),
        ("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 11, 2),
("i love cryptography <3", [1], [1], 11, 2),
("i love cryptography <3", [1], [1], 29, 10),
("i love cryptography <3", [1], [1], 37, 14),
        ("Какой-то текст на русском. Не ожидал такого, да?", [2, 1, 3, 5, 6], [2,2,2,6,5], 7, 5),
        ("test message", [1, 0], [0, 1], 5, 3),  # Простое поле GF(5^3)
        ("hello world", [1, 2], [2, 3], 7, 11),      # Поле GF(7^3)
        ("123456", [1], [2], 3, 2),                   # Поле GF(3^2)
        ("", [1, 1], [0, 1], 5, 8),                # Пустая строка
        ("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 17, 10),
        ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111", [1], [0], 11, 15),
        ('''IT WAS A PLEASURE TO BURN
IT was a special pleasure to see things eaten, to see things blackened and changed. With the
brass nozzle in his fists, with this great python spitting its venomous kerosene upon the world,
the blood pounded in his head, and his hands were the hands of some amazing conductor playing
all the symphonies of blazing and burning to bring down the tatters and charcoal ruins of history.
''', [1, 2, 3, 1], [2, 1, 1, 0], 3, 4),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 11, 10),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 17, 5),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 11, 5),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 7, 10),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 7, 10),
("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 23, 10),
    ]
)
def test_affine_encode_decode(message, keyA_coeffs, keyB_coeffs, p, n):
    # Настройка поля GF(p^n)
    field = CreateGFpn(p, n)

    # Создание ключей
    keyA = field.elm(keyA_coeffs)
    keyB = field.elm(keyB_coeffs)

    # Кодирование и декодирование
    encoded_message = AffineEncode(field, message, keyA, keyB)
    decoded_message = AffineDecode(field, encoded_message, keyA, keyB)

    # Проверка
    assert decoded_message[:len(message)] == message

@pytest.mark.parametrize(
    "message",
    [
        ("test message"),
        ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
        ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
        "1111111111111111111111111111",
        "111111111111",
        "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    ]
)
def test_converter(message):
    binRes = ''
    field = CreateGFpn(p=7, n=11)
    binMsg = tm.string_to_binary(message + '00000')

    blockLen = int(ceil(log2(field.p ** field.mod_poly.order + 1)))
    blockNum = int(ceil(len(binMsg) / blockLen))

    for i in range(blockNum):
        if i == blockNum - 1:
            block = binMsg[i * blockLen:].ljust(blockLen, '0')
        else:
            block = binMsg[i * blockLen : (i + 1) * blockLen]
        blockInGfpn = Converter.BinaryIntoElementInGFpn(block, field)
        encodedBinary = Converter.ElementInGFpnIntoBinary(blockInGfpn).rjust(blockLen, '0')
        binRes += encodedBinary

    res = tm.binary_to_string(binRes)

    assert res[:len(message)] == message