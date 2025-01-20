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
                for keyB_coeffs in key_combinations:
                    # Создание ключей
                    keyA = field.elm(keyA_coeffs)
                    keyB = field.elm(keyB_coeffs)

                    # Тестовое сообщение
                    message = '''IT WAS A PLEASURE TO BURN
IT was a special pleasure to see things eaten, to see things blackened and changed. With the
brass nozzle in his fists, with this great python spitting its venomous kerosene upon the world,
the blood pounded in his head, and his hands were the hands of some amazing conductor playing
all the symphonies of blazing and burning to bring down the tatters and charcoal ruins of history.
With his symbolic helmet numbered 451 on his stolid head, and his eyes all orange flame with
the thought of what came next, he flicked the igniter and the house jumped up in a gorging fire
that burned the evening sky red and yellow and black. He strode in a swarm of fireflies. He
wanted above all, like the old joke, to shove a marshmallow on a stick in the furnace, while the
flapping pigeon-winged books died on the porch and lawn of the house. While the books went up
in sparkling whirls and blew away on a wind turned dark with burning.
Montag grinned the fierce grin of all men singed and driven back by flame.
He knew that when he returned to the firehouse, he might wink at himself, a minstrel man, burnt-
corked, in the mirror. Later, going to sleep, he would feel the fiery smile still gripped by his face
muscles, in the dark. It never went away, that. smile, it never ever went away, as long as he
remembered.'''

                    # Кодирование и декодирование
                    encoded_message = AffineEncode(field, message, keyA, keyB)
                    decoded_message = AffineDecode(field, encoded_message, keyA, keyB)

                    # Проверка
                    if decoded_message != message:
                        raise ValueError(f"Decoded message does not match original for p={p}, n={n}.")
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
