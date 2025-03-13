from typing import List
import string

# Найти 10 самых длинных слов, состоящих из наибольшего количества уникальных символов.
def get_longest_diverse_words(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return []

    words = text.split()
    # Сортируем слова по длине и количеству уникальных символов (в обратном порядке)
    sorted_words = sorted(words, key=lambda word: (len(set(word)), len(word)), reverse=True)

    return sorted_words[:10]

# Найти самый редкий символ в документе.
def get_rarest_char(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return ''

    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1

    if not char_counts:
        return ''

    rarest_char = min(char_counts, key=char_counts.get)
    return rarest_char

# Подсчитать количество знаков препинания в документе.
def count_punctuation_chars(file_path: str) -> int:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return 0

    punctuation_count = 0
    for char in text:
        if char in string.punctuation:
            punctuation_count += 1

    return punctuation_count

# Подсчитать количество не-ASCII символов в документе.
def count_non_ascii_chars(file_path: str) -> int:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return 0

    non_ascii_count = 0
    for char in text:
        if ord(char) > 127:  # ASCII символы имеют код от 0 до 127
            non_ascii_count += 1

    return non_ascii_count

# Найти самый часто встречающийся не-ASCII символ в документе.
def get_most_common_non_ascii_char(file_path: str) -> str: 
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return ''

    non_ascii_chars = {}
    for char in text:
        if ord(char) > 127:
            non_ascii_chars[char] = non_ascii_chars.get(char, 0) + 1

    if not non_ascii_chars:
        return ''

    most_common_char = max(non_ascii_chars, key=non_ascii_chars.get)
    return most_common_char


print(get_longest_diverse_words('data.txt'))

print(get_rarest_char('data.txt'))

print(count_punctuation_chars('data.txt'))

print(count_non_ascii_chars('data.txt'))

print(get_most_common_non_ascii_char('data.txt')) 