import os
import time
import statistics

# 1. Наивный алгоритм поиска подстроки
# Проверяет по буквам каждое слово на сходимость с заданными паролями
def naive_search(text, pattern):

    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    for i in range(n - m + 1):

        match = True

        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break

        if match:
            return i

    return -1


# 2. Алгоритм БМХ (Алгоритм Бойера-Мура-Хорспула)
# Запоминает буквы в исходном слове и где они стоят. Когда начинает сравннение проверяет с последней буквы.
# Если буква не сопадает, то он прыгает на столько, чтобы эта не подходящая буква не мешала.
def bmh_search(text, pattern):

    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0

    if m > n:
        return -1

    shift = {}

    for i in range(m - 1):
        shift[pattern[i]] = m - 1 - i

    # m - длина искомой строки, n - длина текста, i - индекс в тексте, j - индекс в искомой строке
    # m - 1 - i - формула сдвига
    # s - выстречается 2 раза, но присваивается ему значение 9 (послденее)
    # Главная идея: сравнивать символы справа налево и, если найдено несовпадение, сдвигать искомое слово сразу на несколько позиций, а не на одну.

    i = 0

    while i <= n - m:

        j = m - 1

        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            return i

        last_char = text[i + m - 1]
        i += shift.get(last_char, m)

    return -1


# Вывод таблицы сдвигов БМХ
# Сдвиг = m - 1 - i, где: m — длина искомого слова; i — позиция символа, начиная с нуля.
def print_shift_table(pattern):

    m = len(pattern)
    shift = {}

    for i in range(m - 1):
        shift[pattern[i]] = m - 1 - i

    print("\n----------------------------------------------")
    print("Таблица сдвигов БМХ")
    print("----------------------------------------------")
    print("Символ | Сдвиг")
    print("----------------")

    for char, value in shift.items():
        print(f"{repr(char):6} | {value}")

    print(f"Другие | {m}")


# 3. Подготовка текста
def prepare_text(text):

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if not text.endswith("\n"):
        text += "\n"

    return text


# 4. Проверка результата поиска
def check_result(index):
    return index != -1


# 5. Замер времени

# Medium: сбор статистики времени
def measure_time(search_function, text, pattern, repeats=5):

    times = []
    result = -1

    for _ in range(repeats):

        start = time.perf_counter()

        result = search_function(text, pattern)

        end = time.perf_counter()

        times.append(end - start)

    return result, times


# 6. Вывод статистики
def print_statistics(name, result, times):

    print(f"\n{name}")

    if result != -1:
        print("Результат: пароль найден")
        print(f"Индекс первого вхождения: {result}")
    else:
        print("Результат: пароль не найден")

    print(f"Количество запусков: {len(times)}")
    print(f"Минимальное время: {min(times):.8f} сек")
    print(f"Максимальное время: {max(times):.8f} сек")
    print(f"Среднее время: {statistics.mean(times):.8f} сек")


# 7. Главная функция
def main():

    file_path = "SecLists/Passwords/Common-Credentials/Pwdb_top-1000.txt"

    if not os.path.exists(file_path):
        print(f"\nФайл не найден: {file_path}")
        print("Положите файл со списком паролей рядом с программой.")
        return

    password = input("\nВведите пароль для поиска: ").strip()

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    text = prepare_text(text)

    pattern = password + "\n"

    print("\n----------------------------------------------")
    print("Информация о файле")
    print("----------------------------------------------")
    print(f"Размер файла: {os.path.getsize(file_path):,} байт")
    print(f"Размер текста: {len(text):,} символов")
    print(f"Искомый пароль: {password}")

    # Выводим таблицу сдвигов перед замерами времени
    print_shift_table(pattern)

    # Rare: запуск наивного алгоритма
    naive_result, naive_times = measure_time(
        naive_search,
        text,
        pattern
    )

    # Rare: запуск БМХ
    bmh_result, bmh_times = measure_time(
        bmh_search,
        text,
        pattern
    )

    # Проверяем, что результаты одинаковые
    print("\n----------------------------------------------")
    print("Проверка результатов")
    print("----------------------------------------------")

    if check_result(naive_result) == check_result(bmh_result):
        print("Оба алгоритма дали одинаковый результат.")
    else:
        print("Ошибка: результаты алгоритмов отличаются!")

    print_statistics(
        "Наивный алгоритм",
        naive_result,
        naive_times
    )

    print_statistics(
        "БМХ",
        bmh_result,
        bmh_times
    )

    # Medium: сравнение времени поиска
    naive_average = statistics.mean(naive_times)
    bmh_average = statistics.mean(bmh_times)

    print("\n----------------------------------------------")
    print("Сравнение")
    print("----------------------------------------------")

    if bmh_average > 0:
        speedup = naive_average / bmh_average
        print(f"Ускорение БМХ: {speedup:.2f} раз")

    if naive_average < bmh_average:
        print("В данном запуске наивный алгоритм оказался быстрее.")
    else:
        print("В данном запуске БМХ оказался быстрее.")

# Запуск программы

if __name__ == "__main__":
    main()


# ABCWORDXXWORD - исходный текст.
# WORD - искомое слово.
# Шаг 1. Алгоритм берёт участок текста длиной 4 символа, как и искомое слово.
# Шаг 2. Сравнивает символы справа налево.
# Последний символ искомого слова — D.
# Последний символ участка текста — W.
# Они не совпадают. Алгоритм не начинает проверку заново с соседней позиции, а смотрит в таблицу сдвигов.
# Шаг 3. Находит сдвиг для символа W.
# В слове WORD буква W стоит в начале, поэтому сдвиг равен 3.
# Алгоритм передвигает окно на три позиции вправо.
#
# БМХ - Смотрит на последний символ участка текста и использует таблицу, чтобы определить величину сдвига.