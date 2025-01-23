import itertools
from concurrent.futures import ProcessPoolExecutor
from Fields import CreateGFpn
from Affine import AffineEncode, AffineDecode


def parse_file(filepath, p_start=None, n_start=None):
    """
    Читает значения p и n из файла и ограничивает их начальными значениями p_start и n_start.
    """
    results = {}
    with open(filepath, "r") as file:
        for line in file:
            if line.strip().startswith("["):
                parts = line.strip().split(",")
                p = int(parts[0][1:])  # Первое значение - p
                n = int(parts[1])  # Второе значение - n
                if (p_start is not None and p < p_start) or (n_start is not None and n < n_start):
                    continue
                if p not in results:
                    results[p] = []
                results[p].append(n)
    return results


def check_p_and_ns(p, n_values):
    """
    Проверяет значения n для заданного p и перебирает все возможные ключи.
    """
    for n in n_values:
        try:
            # Настройка поля GF(p^n)
            field = CreateGFpn(p, n)

            # Перебор всех возможных коэффициентов для ключей
            key_combinations = itertools.product(range(p), repeat=n)

            for keyA_coeffs in key_combinations:
                if keyA_coeffs == [0]*n:
                    continue
                for keyB_coeffs in key_combinations:
                    # Создание ключей
                    keyA = field.elm(keyA_coeffs)
                    keyB = field.elm(keyB_coeffs)

                    # Тестовое сообщение
                    message = '''It took me almost a month to create this, but I'm so glad it finally works'''

                    # Кодирование и декодирование
                    encoded_message = AffineEncode(field, message, keyA, keyB)
                    decoded_message = AffineDecode(field, encoded_message, keyA, keyB)

                    # Проверка
                    if decoded_message != message:
                        raise ValueError(f"Decoded message does not match original for p={p}, n={n}."
                                         f"Failed KeyA: {keyA}, KeyB: {keyB}")
        except Exception as e:
            return f"Failed for p={p}, n={n}. Exception: {e}"
    return f"All provided n values work for p={p}."


def test_values_from_file_parallel(filepath, p_start=None, n_start=None, max_workers=4):
    """
    Проверяет значения p и n из файла с ограничением на p_start и n_start.
    Использует параллельную обработку.
    """
    data = parse_file(filepath, p_start, n_start)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_p = {
            executor.submit(check_p_and_ns, p, n_values): p for p, n_values in data.items()
        }

        for future in future_to_p:
            result = future.result()  # Ждем завершения задачи
            print(result)  # Выводим результат сразу после его получения


if __name__ == "__main__":
    # Пример вызова для файла с использованием многопоточности
    file_path = "ConwayPolynomials.txt"
    test_values_from_file_parallel(file_path, p_start=2, n_start=1, max_workers=4)
