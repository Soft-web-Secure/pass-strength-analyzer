import random
import string
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# ================== ЗАПРЕЩЕННЫЕ ШАБЛОНЫ ==================
COMMON_PATTERNS = [
    "qwerty", "zxcvb", "qwer", "zxcv", "qazw", "qazx", "wsxc", "wsxz", "qaze", "qazq", "edcx", "edcv", "wsxq", "wsxe",
    "edcw", "edcr",
    "asdf", "12345", "09876", "87654", "23456", "password"
]


# ================== ПРОВЕРКА КЛАВИАТУРНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ ==================
def has_keyboard_sequence(password):
    """Проверяет наличие последовательностей типа (три в ряд из разных рядов)"""
    lowered = password.lower()

    # Ряды клавиатуры QWERTY
    rows = [
        "`1234567890-=",  # верхний ряд с символами
        "qwertyuiop[]\\",
        "asdfghjkl;'",
        "zxcvbnm,./"
    ]

    # Очищаем ряды для более чистого сравнения (убираем спецсимволы если нужно)
    clean_rows = [
        "1234567890",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    # Проверка горизонтальных последовательностей (3+ символа подряд на одном ряду)
    for row in clean_rows:
        for i in range(len(row) - 2):
            seq = row[i:i + 3]
            if seq in lowered:
                return True
            # Проверка в обратном порядке
            rev_seq = seq[::-1]
            if rev_seq in lowered:
                return True

    # Проверка вертикальных последовательностей (по столбцам)
    # Формируем столбцы с учётом разной длины рядов
    columns = []
    max_len = max(len(r) for r in clean_rows)

    for col in range(max_len):
        column = ""
        for row in clean_rows:
            if col < len(row):
                column += row[col]
        if len(column) >= 3:
            columns.append(column)

    # Проверяем столбцы на наличие 3+ символов подряд
    for col in columns:
        for i in range(len(col) - 2):
            seq = col[i:i + 3]
            if seq in lowered:
                return True
            rev_seq = seq[::-1]
            if rev_seq in lowered:
                return True

    # Специальная проверка для комбинаций упрощённого подбора ряд и столбец)
    special_patterns = []

    # Паттерны по 3 символа из каждого ряда подряд
    for r1 in range(len(clean_rows[0]) - 2):
        for r2 in range(len(clean_rows[1]) - 2):
            for r3 in range(len(clean_rows[2]) - 2):
                # Только если столбцы примерно совпадают (диагональные паттерны)
                if abs(r1 - r2) <= 1 and abs(r2 - r3) <= 1:
                    pattern = (clean_rows[0][r1:r1 + 3] +
                               clean_rows[1][r2:r2 + 3] +
                               clean_rows[2][r3:r3 + 3])
                    if len(pattern) >= 8:
                        special_patterns.append(pattern)

    # Проверяем специальные паттерны
    for pattern in special_patterns:
        if pattern in lowered:
            return True

    # Дополнительная проверка конкретных примеров из задачи
    keyboard_sequences = [
        "qweasdzxc", "qazwsxedc", "poi;lk.,m", "poikjl,m",
        "qwerty", "asdfgh", "zxcvbn", "1qaz2wsx", "qaz123"
    ]

    for seq in keyboard_sequences:
        if seq in lowered:
            return True

    return False


# ================== ПРОВЕРКА ПОВТОРОВ ==================
def has_repeating_pattern(password):
    length = len(password)
    for size in range(1, length // 2 + 1):
        pattern = password[:size]
        if pattern * (length // size) == password:
            return True
    return False


# ================== ПРОВЕРКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ ==================
def has_sequence(password):
    sequences = "abcdefghijklmnopqrstuvwxyz0123456789"
    lowered = password.lower()

    for i in range(len(sequences) - 4):
        seq = sequences[i:i + 5]
        if seq in lowered:
            return True
    return False


# ================== ПРОВЕРКА НА ДАТУ ==================
def contains_date_pattern(password):
    if re.search(r"\d{6,8}", password):
        return True

    if re.search(r"(19|20)\d{2}", password):
        return True

    return False


# ================== ПРОВЕРКА ФОРМАТА ШАБЛОН + ДАТА ==================
def pattern_plus_date(password):
    if re.fullmatch(r".{1,4}\d{6,8}", password):
        return True

    if re.fullmatch(r"\d{6,8}.{1,4}", password):
        return True

    return False


# ================== ОБЯЗАТЕЛЬНЫЕ ТРЕБОВАНИЯ ==================
def meets_basic_requirements(password):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    return has_upper and has_lower and has_digit and has_symbol


# ================== ОСНОВНАЯ ПРОВЕРКА ==================
def check_password_strength(password):
    if not password:
        return 0

    # ❌ Обязательные требования
    if not meets_basic_requirements(password):
        return 1

    lowered = password.lower()

    # ❌ Запрещённые шаблоны
    for pattern in COMMON_PATTERNS:
        if pattern in lowered:
            return 2

    # ❌ Клавиатурные последовательности (НОВАЯ ПРОВЕРКА)
    if has_keyboard_sequence(password):
        return 1

    # ❌ Повтор
    if has_repeating_pattern(lowered):
        return 1

    # ❌ Последовательность
    if has_sequence(lowered):
        return 2

    # ❌ Содержит дату
    if contains_date_pattern(password):
        return 1

    # ❌ Шаблон + дата
    if pattern_plus_date(password):
        return 1

    # ❌ Больше 50% цифр
    digit_ratio = sum(c.isdigit() for c in password) / len(password)
    if digit_ratio > 0.5:
        return 2

    # ================== ОЦЕНКА ==================
    score = 0
    length = len(password)

    if length >= 8:
        score += 2
    if length >= 12:
        score += 2
    if length >= 16:
        score += 2

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 2

    return max(1, min(score, 10))


# ================== КНОПКА ПРОВЕРИТЬ ==================
def check_password():
    password = entry.get()

    if not password:
        result_label.config(text="Введите пароль!", bootstyle="danger")
        return

    strength = check_password_strength(password)

    if strength <= 2:
        style = "danger"
        text = "Очень слабый"
    elif strength <= 4:
        style = "warning"
        text = "Слабый"
    elif strength <= 6:
        style = "info"
        text = "Средний"
    elif strength <= 8:
        style = "primary"
        text = "Хороший"
    else:
        style = "success"
        text = "Отличный"

    result_label.config(
        text=f"{text} — {strength}/10",
        bootstyle=style
    )


# ================== КНОПКА ГЕНЕРАЦИИ ==================
def generate_password():
    length = 16
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if check_password_strength(password) >= 8:
            break

    entry.delete(0, END)
    entry.insert(0, password)

    result_label.config(
        text="Сгенерирован надёжный пароль (8+ уровень)",
        bootstyle="success"
    )


# ================== ИНТЕРФЕЙС ==================
app = ttk.Window(themename="flatly")
app.title("Проверка надёжности пароля")
app.geometry("430x210")
app.resizable(False, False)
app.configure(bg="white")

entry = ttk.Entry(app, font=("Segoe UI", 12), width=35)
entry.pack(pady=20)

button_frame = ttk.Frame(app)
button_frame.pack(pady=10)

ttk.Button(
    button_frame,
    text="Проверить",
    bootstyle="primary",
    width=15,
    command=check_password
).grid(row=0, column=0, padx=10)

ttk.Button(
    button_frame,
    text="Сгенерировать",
    bootstyle="primary",
    width=15,
    command=generate_password
).grid(row=0, column=1, padx=10)

result_label = ttk.Label(app, text="", font=("Segoe UI", 11))
result_label.pack(pady=20)

app.mainloop()