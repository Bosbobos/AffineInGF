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
        ([2, 3, 4], [1, 1], [0, 1, 1], 7, 13)
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
    "message, keyA_coeffs, keyB_coeffs, p, n",
    [
        ("test message", [1, 0], [0, 1], 5, 3),  # Простое поле GF(5^3)
        ("hello world", [1, 2], [2, 3], 7, 11),      # Поле GF(7^3)
        ("123456", [1], [2], 3, 2),                   # Поле GF(3^2)
        ("", [1, 1], [0, 1], 5, 8),                # Пустая строка
        ("i love cryptography <3", [15, 1, 0, 7, 8], [4, 6, 7, 0, 1], 17, 10),
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
    assert decoded_message == message
