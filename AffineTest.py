import pytest
import galois_field as gf
from Affine import *
import Converter
import TextManager as tm

@pytest.mark.parametrize(
    "block_coeffs, keyA_coeffs, keyB_coeffs, p, mod_coeffs, decode, expected_coeffs",
    [
        # Пример 1: Кодирование
        ([3, 1], [2, 0], [1, 1], 5, [1, 0, 0, 2], False, [4, 3]),
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
    keyB = field.elm(keyB_coeffs)

    z = keyA * keyA.inverse()

    # Преобразование
    result = AffineEncodeBlock(block, keyA, keyB, decode)

    decodedResult = AffineEncodeBlock(result, keyA, keyB, not decode)

    # Проверка
    assert result.coeffs == decodedResult.coeffs

@pytest.mark.parametrize(
    "message, keyA_coeffs, keyB_coeffs, p, mod_coeffs",
    [
        ("test message", [1, 0], [0, 1], 5, [1, 0, 0, 2]),  # Простое поле GF(5^3)
        ("hello world", [1, 2], [2, 3], 7, [1, 0, 3]),      # Поле GF(7^3)
        ("123456", [1], [2], 3, [1, 1]),                   # Поле GF(3^2)
        ("", [1, 1], [0, 1], 5, [1, 0, 2]),                # Пустая строка
    ]
)
def test_affine_encode_decode(message, keyA_coeffs, keyB_coeffs, p, mod_coeffs):
    # Настройка поля GF(p^n)
    field = gf.GFpn(p, mod_coeffs)

    # Создание ключей
    keyA = field.elm(keyA_coeffs)
    keyB = field.elm(keyB_coeffs)

    # Кодирование и декодирование
    encoded_message = AffineEncode(field, message, keyA, keyB)
    decoded_message = AffineDecode(field, encoded_message, keyA, keyB)

    # Проверка
    assert decoded_message == message

@pytest.mark.parametrize(
    "message1, message2, keyA_coeffs, keyB_coeffs, p, mod_coeffs",
    [
        ("hello", "world", [1, 0], [0, 1], 5, [1, 0, 0, 2]),  # Разные сообщения, одно поле
        ("abc", "def", [1, 1], [1, 0], 7, [1, 0, 3]),         # Поле GF(7^2)
        ("123", "321", [2], [1], 3, [1, 1]),                 # Поле GF(3^1)
    ]
)
def test_affine_encode_injective(message1, message2, keyA_coeffs, keyB_coeffs, p, mod_coeffs):
    # Настройка поля GF(p^n)
    field = gf.GFpn(p, mod_coeffs)

    # Создание ключей
    keyA = field.elm(keyA_coeffs)
    keyB = field.elm(keyB_coeffs)

    # Кодирование сообщений
    encoded1 = AffineEncode(field, message1, keyA, keyB)
    encoded2 = AffineEncode(field, message2, keyA, keyB)

    # Проверка
    assert encoded1 != encoded2, "Закодированные сообщения для разных входных данных совпадают"

@pytest.mark.parametrize(
    "keyA_coeffs, keyB_coeffs, message, p, mod_coeffs",
    [
        ([0], [0, 1], "test", 5, [1, 0, 2]),  # Нулевой ключ A
        ([0], [0], "test", 7, [1, 0, 3]),     # Оба ключа нулевые
    ]
)
def test_affine_invalid_keys(keyA_coeffs, keyB_coeffs, message, p, mod_coeffs):
    # Настройка поля GF(p^n)
    field = gf.GFpn(p, mod_coeffs)

    # Создание ключей
    keyA = field.elm(keyA_coeffs)
    keyB = field.elm(keyB_coeffs)

    # Проверка на исключение
    with pytest.raises(ValueError, match="Invalid keyA: zero element not allowed"):
        AffineEncode(field, message, keyA, keyB)

    with pytest.raises(ValueError, match="Invalid keyA: zero element not allowed"):
        AffineDecode(field, message, keyA, keyB)
