import timeit
import hashlib

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    """Алгоритм Боєра-Мура"""
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

def compute_lps(pattern):
    """Обчислення префікс-функції для алгоритму Кнута-Морріса-Пратта"""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """Алгоритм Кнута-Морріса-Пратта"""
    M = len(pattern)
    N = len(text)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

def polynomial_hash(s, base=256, modulus=101):
    """Поліноміальний хеш для алгоритму Рабіна-Карпа"""
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + ord(char)) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
    """Алгоритм Рабіна-Карпа"""
    base = 256
    modulus = 101
    M = len(pattern)
    N = len(text)
    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_hash = polynomial_hash(text[:M], base, modulus)
    h_multiplier = pow(base, M - 1) % modulus

    for i in range(N - M + 1):
        if pattern_hash == current_hash:
            if text[i:i+M] == pattern:
                return i
        if i < N - M:
            current_hash = (current_hash - ord(text[i]) * h_multiplier) % modulus
            current_hash = (current_hash * base + ord(text[i + M])) % modulus
            if current_hash < 0:
                current_hash += modulus
    return -1

with open("стаття 1.txt", "r", encoding="windows-1251") as f:
    text1 = f.read()

with open("стаття 2.txt", "r", encoding="utf-8-sig") as f:
    text2 = f.read()

real_substring1 = "пошук"
real_substring2 = "бази даних"

fake_substring1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
fake_substring2 = "рандомний текст що не існує в наданій статті 2"

def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=5)

def run_tests():
    test_cases = {
        "Стаття 1 (реальний)": (text1, real_substring1),
        "Стаття 1 (вигаданий)": (text1, fake_substring1),
        "Стаття 2 (реальний)": (text2, real_substring2),
        "Стаття 2 (вигаданий)": (text2, fake_substring2),
    }

    for algo_name, algo_func in [
        ("Boyer-Moore", boyer_moore_search),
        ("Knuth-Morris-Pratt", kmp_search),
        ("Rabin-Karp", rabin_karp_search)
    ]:
        print(f"\n{algo_name}:")
        for case, (text, pattern) in test_cases.items():
            time_taken = measure_time(algo_func, text, pattern)
            print(f"  {case}: {time_taken:.6f} секунд")

if __name__ == "__main__":
    run_tests()

#   Висновки у файлі Conclusions.md